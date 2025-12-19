"""
Leadspedia API client.

Provides authenticated access to the Leadspedia API for fetching lead data,
affiliate click information, and revenue reports.

API Documentation: https://developer.leadspedia.com/
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterator, Optional
from urllib.parse import urljoin, urlencode

import requests
from requests import Response
from requests.auth import HTTPBasicAuth
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter


class LeadspediaApiError(RuntimeError):
    """Exception raised for Leadspedia API errors."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        payload: dict | None = None,
        error_code: str | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload
        self.error_code = error_code


def _generate_signature(api_key: str, api_secret: str, timestamp: int) -> str:
    """
    Generate HMAC-SHA256 signature for Leadspedia API authentication.
    
    The signature is generated using: HMAC-SHA256(api_secret, api_key + timestamp)
    """
    message = f"{api_key}{timestamp}"
    signature = hmac.new(
        api_secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return signature


@dataclass(frozen=True)
class LeadspediaClient:
    """
    Client for interacting with the Leadspedia API.
    
    Authentication is handled via:
    - HMAC signature for most endpoints (using api_key and api_secret)
    - Basic Auth for report endpoints (using basic_user and basic_pass)
    """

    api_key: str
    api_secret: str
    base_url: str = "https://api.leadspedia.com/core/v2/"
    session: requests.Session | None = None
    timeout: int = 30
    # Separate credentials for Basic Auth (report endpoints)
    basic_user: str | None = None
    basic_pass: str | None = None

    def _get_session(self) -> requests.Session:
        """Get or create a requests session."""
        return self.session or requests.Session()

    def _build_auth_params(self) -> Dict[str, Any]:
        """
        Build authentication parameters for API requests.
        
        Per Leadspedia API docs: All endpoints require api_key and api_secret
        as query parameters (no HMAC signature needed).
        """
        return {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
        }

    def _raise_for_api_error(self, resp: Response) -> None:
        """Check response for API errors and raise appropriate exception."""
        try:
            payload = resp.json()
        except Exception:
            payload = None

        # Leadspedia returns 200 even for errors, check response payload
        if isinstance(payload, dict):
            success = payload.get("success", payload.get("result") == "success")
            if not success:
                error_msg = payload.get("message") or payload.get("error") or "Unknown API error"
                error_code = payload.get("errorCode") or payload.get("code")
                raise LeadspediaApiError(
                    f"Leadspedia API error: {error_msg}",
                    status_code=resp.status_code,
                    payload=payload,
                    error_code=error_code,
                )

        # Check HTTP status code for non-200 responses
        if resp.status_code >= 400:
            msg = f"Leadspedia API HTTP error {resp.status_code}"
            raise LeadspediaApiError(
                msg,
                status_code=resp.status_code,
                payload=payload if isinstance(payload, dict) else None,
            )

    def _get_basic_auth(self) -> HTTPBasicAuth:
        """
        Get HTTPBasicAuth instance for report endpoints.
        
        Uses dedicated Basic Auth credentials if available,
        otherwise falls back to API key/secret.
        """
        user = self.basic_user or self.api_key
        passwd = self.basic_pass or self.api_secret
        return HTTPBasicAuth(user, passwd)

    @retry(
        retry=retry_if_exception_type((requests.RequestException,)),
        wait=wait_exponential_jitter(initial=0.5, max=8),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    def get_with_basic_auth(
        self,
        endpoint: str,
        *,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a GET request using Basic Authentication.
        
        Some Leadspedia endpoints (like reports) use Basic Auth instead of HMAC.
        API Key is used as username, API Secret as password.
        
        Args:
            endpoint: API endpoint path (e.g., 'reports/getVerticalsReport.do')
            params: Optional query parameters
            
        Returns:
            JSON response as dictionary
        """
        url = urljoin(self.base_url, endpoint.lstrip("/"))

        
        resp = self._get_session().get(
            url,
            params=params or {},
            auth=self._get_basic_auth(),
            timeout=self.timeout,
        )
        
        
        self._raise_for_api_error(resp)
        return resp.json()

    @retry(
        retry=retry_if_exception_type((requests.RequestException,)),
        wait=wait_exponential_jitter(initial=0.5, max=8),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    def get(
        self,
        endpoint: str,
        *,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a GET request to the Leadspedia API.
        
        Args:
            endpoint: API endpoint path (e.g., 'leads/getAll')
            params: Optional query parameters
            
        Returns:
            JSON response as dictionary
        """
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        
        # Merge auth params with request params
        query_params = self._build_auth_params()
        if params:
            query_params.update(params)

        
        resp = self._get_session().get(url, params=query_params, timeout=self.timeout)
        
        
        self._raise_for_api_error(resp)
        return resp.json()

    @retry(
        retry=retry_if_exception_type((requests.RequestException,)),
        wait=wait_exponential_jitter(initial=0.5, max=8),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    def post(
        self,
        endpoint: str,
        *,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a POST request to the Leadspedia API.
        
        Args:
            endpoint: API endpoint path
            data: Form data for POST body
            params: Optional query parameters
            
        Returns:
            JSON response as dictionary
        """
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        
        # Auth params go in query string
        query_params = self._build_auth_params()
        if params:
            query_params.update(params)

        resp = self._get_session().post(
            url,
            params=query_params,
            data=data,
            timeout=self.timeout,
        )
        self._raise_for_api_error(resp)
        return resp.json()

    def get_paged(
        self,
        endpoint: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        page_size: int = 500,
        max_pages: int = 100,
    ) -> Iterator[Dict[str, Any]]:
        """
        Iterate through paginated API results.
        
        Leadspedia uses start/limit pagination.
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            page_size: Number of records per page
            max_pages: Maximum pages to fetch (safety limit)
            
        Yields:
            Each page's response dictionary
        """
        params = dict(params or {})
        params["limit"] = page_size
        start = 0

        for _ in range(max_pages):
            params["start"] = start
            page = self.get(endpoint, params=params)
            yield page

            # Check if there are more results
            # Leadspedia nests data under response.data
            response = page.get("response") or {}
            if isinstance(response, dict):
                data = response.get("data") or []
            elif isinstance(response, list):
                data = response
            else:
                data = page.get("data") or []
            
            if not isinstance(data, list) or len(data) < page_size:
                break

            start += page_size


def iter_data_from_pages(pages: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    """
    Extract data items from paginated responses.
    
    Leadspedia response structure:
    {"success":true,"response":{"start":0,"limit":500,"returned":N,"total":N,"data":[...]}}
    
    Args:
        pages: Iterator of page response dictionaries
        
    Yields:
        Individual data items from each page
    """
    for page in pages:
        # Leadspedia nests data under response.data
        response = page.get("response") or {}
        
        # If response is a dict with nested data, extract it
        if isinstance(response, dict):
            data = response.get("data") or []
        elif isinstance(response, list):
            # Fallback if response is directly a list
            data = response
        else:
            # Try top-level data key
            data = page.get("data") or []
        
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    yield item

