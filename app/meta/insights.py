from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import json
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence

import pandas as pd

from app.cache.sqlite_cache import SqliteCache, sha256_key
from app.metrics.cpl import compute_cpl, count_leads_from_actions
from app.meta.client import MetaGraphClient, iter_data_from_pages


@dataclass(frozen=True)
class InsightsQuery:
    ad_account_id: str  # act_...
    since: date
    until: date
    level: str = "ad"
    breakdowns: Sequence[str] = ()
    campaign_ids: Sequence[str] = ()
    adset_ids: Sequence[str] = ()
    ad_ids: Sequence[str] = ()

    def to_params(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "level": self.level,
            "time_range": {"since": self.since.isoformat(), "until": self.until.isoformat()},
            "limit": 5000,
            "fields": ",".join(
                [
                    "campaign_id",
                    "campaign_name",
                    "adset_id",
                    "adset_name",
                    "ad_id",
                    "ad_name",
                    "spend",
                    "impressions",
                    "reach",
                    "frequency",
                    "clicks",
                    "ctr",
                    "cpc",
                    "actions",
                    "cost_per_action_type",
                ]
            ),
        }
        if self.breakdowns:
            params["breakdowns"] = ",".join(self.breakdowns)

        filters: List[Dict[str, Any]] = []
        if self.campaign_ids:
            filters.append({"field": "campaign.id", "operator": "IN", "value": list(self.campaign_ids)})
        if self.adset_ids:
            filters.append({"field": "adset.id", "operator": "IN", "value": list(self.adset_ids)})
        if self.ad_ids:
            filters.append({"field": "ad.id", "operator": "IN", "value": list(self.ad_ids)})
        if filters:
            params["filtering"] = filters
        return params


def fetch_insights_rows(client: MetaGraphClient, query: InsightsQuery) -> Iterator[Dict[str, Any]]:
    path = f"{query.ad_account_id}/insights"
    pages = client.get_paged(path, params=query.to_params())
    yield from iter_data_from_pages(pages)


def insights_rows_to_frame(
    rows: Iterable[Dict[str, Any]],
    *,
    lead_action_types: Sequence[str],
) -> pd.DataFrame:
    normalized: List[Dict[str, Any]] = []
    for r in rows:
        spend = r.get("spend")
        actions = r.get("actions")
        leads = count_leads_from_actions(actions, lead_action_types=lead_action_types)
        cpl = compute_cpl(spend, leads)

        out = dict(r)
        out["leads"] = leads
        out["cpl"] = cpl
        normalized.append(out)

    if not normalized:
        return pd.DataFrame()

    df = pd.json_normalize(normalized)

    # Keep a tidy subset of columns (breakdown columns may vary per query).
    # Include IDs for matching with external data sources (e.g., Leadspedia)
    id_cols = [
        "campaign_id",
        "adset_id",
        "ad_id",
    ]
    base_cols = [
        "campaign_name",
        "adset_name",
        "ad_name",
        "spend",
        "leads",
        "cpl",
        "impressions",
        "clicks",
        "ctr",
        "cpc",
        "frequency",
        "reach",
    ]
    present_ids = [c for c in id_cols if c in df.columns]
    present = [c for c in base_cols if c in df.columns]
    # Include breakdown fields if present
    breakdown_cols = [c for c in df.columns if c in ("age", "gender", "publisher_platform", "platform_position", "device_platform")]
    cols = present_ids + breakdown_cols + present
    return df[cols].copy()

def summarize_action_types(rows: Iterable[Dict[str, Any]]) -> pd.DataFrame:
    """
    Returns total action values by action_type across the provided rows.
    Useful to validate which action_type corresponds to Lead Ads submissions.
    """
    totals: Dict[str, float] = {}
    for r in rows:
        actions = r.get("actions")
        if not isinstance(actions, list):
            continue
        for a in actions:
            if not isinstance(a, dict):
                continue
            t = a.get("action_type")
            v = a.get("value")
            if not t:
                continue
            try:
                fv = float(v)
            except Exception:
                continue
            totals[t] = totals.get(t, 0.0) + fv
    if not totals:
        return pd.DataFrame(columns=["action_type", "total_value"])
    df = pd.DataFrame([{"action_type": k, "total_value": v} for k, v in totals.items()])
    return df.sort_values(by="total_value", ascending=False).reset_index(drop=True)


def fetch_insights_frame_cached(
    client: MetaGraphClient,
    cache: SqliteCache,
    query: InsightsQuery,
    *,
    lead_action_types: Sequence[str],
    ttl_seconds: int,
) -> pd.DataFrame:
    """
    Cache only the derived, non-sensitive output (no access tokens).
    """
    key_material = {
        "ad_account_id": query.ad_account_id,
        "since": query.since.isoformat(),
        "until": query.until.isoformat(),
        "level": query.level,
        "breakdowns": list(query.breakdowns),
        "filters": {
            "campaign_ids": list(query.campaign_ids),
            "adset_ids": list(query.adset_ids),
            "ad_ids": list(query.ad_ids),
        },
        "lead_action_types": list(lead_action_types),
    }
    cache_key = sha256_key(json.dumps(key_material, sort_keys=True, separators=(",", ":"), default=str))
    cached = cache.get(cache_key, ttl_seconds=ttl_seconds)
    if cached:
        try:
            return pd.read_json(cached, orient="records")
        except Exception:
            # Fall through to refresh if cache is corrupted/old schema.
            pass

    rows = fetch_insights_rows(client, query)
    df = insights_rows_to_frame(rows, lead_action_types=lead_action_types)
    cache.set(cache_key, df.to_json(orient="records"))
    return df


def fetch_action_type_summary_cached(
    client: MetaGraphClient,
    cache: SqliteCache,
    query: InsightsQuery,
    *,
    ttl_seconds: int,
) -> pd.DataFrame:
    key_material = {
        "kind": "action_type_summary",
        "ad_account_id": query.ad_account_id,
        "since": query.since.isoformat(),
        "until": query.until.isoformat(),
        "level": query.level,
        "breakdowns": list(query.breakdowns),
        "filters": {
            "campaign_ids": list(query.campaign_ids),
            "adset_ids": list(query.adset_ids),
            "ad_ids": list(query.ad_ids),
        },
    }
    cache_key = sha256_key(json.dumps(key_material, sort_keys=True, separators=(",", ":"), default=str))
    cached = cache.get(cache_key, ttl_seconds=ttl_seconds)
    if cached:
        try:
            return pd.read_json(cached, orient="records")
        except Exception:
            pass

    rows = fetch_insights_rows(client, query)
    df = summarize_action_types(rows)
    cache.set(cache_key, df.to_json(orient="records"))
    return df


