from dataclasses import dataclass
from typing import Any, Dict, List, Sequence

from app.meta.client import MetaGraphClient, iter_data_from_pages


@dataclass(frozen=True)
class MetaObject:
    """Represents a Meta Ads object (campaign, adset, or ad)."""
    id: str
    name: str
    status: str = ""  # effective_status from Meta API (ACTIVE, PAUSED, etc.)


def _list_objects(client: MetaGraphClient, path: str, *, fields: Sequence[str]) -> List[Dict[str, Any]]:
    pages = client.get_paged(path, params={"fields": ",".join(fields), "limit": 5000})
    return list(iter_data_from_pages(pages))


def list_campaigns(client: MetaGraphClient, ad_account_id: str) -> List[MetaObject]:
    rows = _list_objects(client, f"{ad_account_id}/campaigns", fields=["id", "name", "effective_status"])
    items = [
        MetaObject(
            id=r["id"],
            name=r.get("name", r["id"]),
            status=r.get("effective_status", ""),
        )
        for r in rows if "id" in r
    ]
    return sorted(items, key=lambda x: x.name.lower())


def list_adsets(client: MetaGraphClient, ad_account_id: str, *, campaign_ids: Sequence[str] = ()) -> List[MetaObject]:
    params: Dict[str, Any] = {"fields": "id,name,campaign_id,effective_status", "limit": 5000}
    if campaign_ids:
        params["filtering"] = [{"field": "campaign.id", "operator": "IN", "value": list(campaign_ids)}]
    pages = client.get_paged(f"{ad_account_id}/adsets", params=params)
    rows = list(iter_data_from_pages(pages))
    items = [
        MetaObject(
            id=r["id"],
            name=r.get("name", r["id"]),
            status=r.get("effective_status", ""),
        )
        for r in rows if "id" in r
    ]
    return sorted(items, key=lambda x: x.name.lower())


def list_ads(client: MetaGraphClient, ad_account_id: str, *, adset_ids: Sequence[str] = ()) -> List[MetaObject]:
    params: Dict[str, Any] = {"fields": "id,name,adset_id,effective_status", "limit": 5000}
    if adset_ids:
        params["filtering"] = [{"field": "adset.id", "operator": "IN", "value": list(adset_ids)}]
    pages = client.get_paged(f"{ad_account_id}/ads", params=params)
    rows = list(iter_data_from_pages(pages))
    items = [
        MetaObject(
            id=r["id"],
            name=r.get("name", r["id"]),
            status=r.get("effective_status", ""),
        )
        for r in rows if "id" in r
    ]
    return sorted(items, key=lambda x: x.name.lower())


