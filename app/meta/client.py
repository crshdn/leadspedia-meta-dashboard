from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, Optional
from urllib.parse import urljoin

import requests
from requests import Response
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter


class MetaApiError(RuntimeError):
    def __init__(self, message: str, *, status_code: int | None = None, payload: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


def _encode_graph_params(params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Meta Graph API expects some query params (e.g. time_range, filtering) to be JSON strings.

    `requests` does not JSON-encode dict/list values in the `params=` argument; instead it
    flattens them into repeated keys (e.g. time_range=since&time_range=until), which Meta
    rejects. This helper safely JSON-encodes nested structures.
    """
    out: Dict[str, Any] = {}
    for k, v in (params or {}).items():
        if v is None:
            continue
        if isinstance(v, (dict, list, tuple)):
            out[k] = safe_json_dumps(v)
        else:
            out[k] = v
    return out


@dataclass(frozen=True)
class MetaGraphClient:
    api_version: str
    access_token: str
    session: requests.Session | None = None

    @property
    def base_url(self) -> str:
        # e.g. https://graph.facebook.com/v24.0/
        return f"https://graph.facebook.com/{self.api_version.strip('/')}/"

    def _get_session(self) -> requests.Session:
        return self.session or requests.Session()

    def _raise_for_meta_error(self, resp: Response) -> None:
        try:
            payload = resp.json()
        except Exception:
            payload = None

        if resp.status_code >= 400:
            msg = f"Meta API error HTTP {resp.status_code}"
            if isinstance(payload, dict) and "error" in payload:
                err = payload.get("error") or {}
                msg = f"Meta API error: {err.get('message','unknown')} (type={err.get('type')}, code={err.get('code')})"
            raise MetaApiError(msg, status_code=resp.status_code, payload=payload if isinstance(payload, dict) else None)

    @retry(
        retry=retry_if_exception_type((requests.RequestException, MetaApiError)),
        wait=wait_exponential_jitter(initial=0.5, max=8),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    def get(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = urljoin(self.base_url, path.lstrip("/"))
        query = _encode_graph_params(params)
        query["access_token"] = self.access_token

        resp = self._get_session().get(url, params=query, timeout=30)
        self._raise_for_meta_error(resp)
        return resp.json()

    def get_paged(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Iterator[Dict[str, Any]]:
        """
        Iterate through Graph API paging by following paging.next URLs.
        Returns each page payload (dict).
        """
        first = self.get(path, params=params)
        yield first

        next_url = (first.get("paging") or {}).get("next")
        sess = self._get_session()
        while next_url:
            resp = sess.get(next_url, timeout=30)
            self._raise_for_meta_error(resp)
            payload = resp.json()
            yield payload
            next_url = (payload.get("paging") or {}).get("next")


def iter_data_from_pages(pages: Iterable[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    for page in pages:
        data = page.get("data")
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    yield item


def safe_json_dumps(obj: Any) -> str:
    return json.dumps(obj, separators=(",", ":"), sort_keys=True, ensure_ascii=False)


