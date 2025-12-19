"""
Leadspedia lead data fetching and parsing.

This module provides functions to fetch lead data, affiliate click data,
and revenue reports from the Leadspedia API.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence

import pandas as pd

from app.cache.sqlite_cache import SqliteCache, sha256_key
from app.leadspedia.client import LeadspediaClient, iter_data_from_pages


@dataclass
class LeadspediaVertical:
    """Represents a Leadspedia vertical."""
    
    id: str
    name: str
    status: str
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "LeadspediaVertical":
        return cls(
            id=str(data.get("verticalID") or data.get("id") or ""),
            name=str(data.get("verticalName") or data.get("name") or ""),
            status=str(data.get("status") or "active"),
        )


@dataclass
class LeadspediaAffiliate:
    """Represents a Leadspedia affiliate."""
    
    id: str
    name: str
    status: str
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "LeadspediaAffiliate":
        return cls(
            id=str(data.get("affiliateID") or data.get("id") or ""),
            name=str(data.get("affiliateName") or data.get("name") or ""),
            status=str(data.get("status") or "active"),
        )


def fetch_verticals(client: LeadspediaClient) -> List[LeadspediaVertical]:
    """
    Fetch all verticals from Leadspedia.
    
    Uses the reports/getVerticalsReport.do endpoint with Basic Auth.
    
    Args:
        client: Leadspedia API client
        
    Returns:
        List of LeadspediaVertical objects
    """
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info("fetch_verticals() called")
    
    try:
        # Use the reports endpoint with Basic Auth
        # This endpoint requires fromDate parameter
        
        # Use a wide date range to get all verticals
        from datetime import date, timedelta
        today = date.today()
        # Get data from the last 365 days to capture all active verticals
        from_date = (today - timedelta(days=365)).strftime("%Y-%m-%d")
        to_date = today.strftime("%Y-%m-%d")
        
        params = {
            "fromDate": from_date,
            "toDate": to_date,
        }
        
        response = client.get_with_basic_auth("reports/getVerticalsReport.do", params=params)
        
        
        # The response format may be different for reports endpoint
        # Try multiple possible response structures
        data = response.get("data") or response.get("response") or response.get("verticals") or []
        
        # If response is the data directly (list), use it
        if isinstance(response, list):
            data = response
        
        
        if isinstance(data, list):
            verticals = [LeadspediaVertical.from_api_response(v) for v in data if isinstance(v, dict)]
            return verticals
            
    except Exception as e:
        import traceback
        traceback.print_exc()
    
    return []


def fetch_affiliates(client: LeadspediaClient) -> List[LeadspediaAffiliate]:
    """
    Fetch all affiliates from Leadspedia.
    
    Args:
        client: Leadspedia API client
        
    Returns:
        List of LeadspediaAffiliate objects
    """
    try:
        response = client.get("affiliates/getAll")
        data = response.get("data") or response.get("response") or []
        if isinstance(data, list):
            return [LeadspediaAffiliate.from_api_response(a) for a in data if isinstance(a, dict)]
    except Exception:
        pass
    return []


def fetch_verticals_cached(
    client: LeadspediaClient,
    cache: SqliteCache,
    ttl_seconds: int = 3600,  # 1 hour cache
) -> List[LeadspediaVertical]:
    """Fetch verticals with caching."""
    
    cache_key = sha256_key("leadspedia_verticals")
    cached = cache.get(cache_key, ttl_seconds=ttl_seconds)
    
    if cached:
        try:
            data = json.loads(cached)
            return [LeadspediaVertical(id=v["id"], name=v["name"], status=v["status"]) for v in data]
        except (json.JSONDecodeError, KeyError):
            pass  # Fall through to fetch fresh data
    
    verticals = fetch_verticals(client)
    
    if verticals:
        cache_data = [{"id": v.id, "name": v.name, "status": v.status} for v in verticals]
        cache.set(cache_key, json.dumps(cache_data))
    
    return verticals


@dataclass(frozen=True)
class LeadQuery:
    """Query parameters for fetching leads from Leadspedia."""

    since: date
    until: date
    affiliate_id: Optional[str] = None
    campaign_id: Optional[str] = None
    vertical_id: Optional[str] = None
    status: Optional[str] = None  # 'sold', 'rejected', 'pending', etc.

    def to_params(self) -> Dict[str, Any]:
        """Convert query to API parameters."""
        params: Dict[str, Any] = {
            "fromDate": self.since.strftime("%Y-%m-%d"),
            "toDate": self.until.strftime("%Y-%m-%d"),
        }
        if self.affiliate_id:
            params["affiliateID"] = self.affiliate_id
        if self.campaign_id:
            params["campaignID"] = self.campaign_id
        if self.vertical_id:
            params["verticalID"] = self.vertical_id
        if self.status:
            params["status"] = self.status
        return params


@dataclass(frozen=True)
class AffiliateClickQuery:
    """Query parameters for fetching affiliate click data."""

    since: date
    until: date
    affiliate_id: Optional[str] = None
    offer_id: Optional[str] = None
    sub_id: Optional[str] = None  # Often contains the Meta Lead ID

    def to_params(self) -> Dict[str, Any]:
        """Convert query to API parameters."""
        params: Dict[str, Any] = {
            "fromDate": self.since.strftime("%Y-%m-%d"),
            "toDate": self.until.strftime("%Y-%m-%d"),
        }
        if self.affiliate_id:
            params["affiliateID"] = self.affiliate_id
        if self.offer_id:
            params["offerID"] = self.offer_id
        if self.sub_id:
            params["subID"] = self.sub_id
        return params


def _safe_decimal(value: Any) -> Decimal:
    """Safely convert a value to Decimal, returning 0 on failure."""
    if value is None:
        return Decimal(0)
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return Decimal(0)


def _safe_int(value: Any) -> int:
    """Safely convert a value to int, returning 0 on failure."""
    if value is None:
        return 0
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def _parse_datetime(value: Any) -> Optional[datetime]:
    """Parse datetime from various formats."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        # Try common formats
        for fmt in [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d",
        ]:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
    return None


def fetch_leads(
    client: LeadspediaClient,
    query: LeadQuery,
) -> Iterator[Dict[str, Any]]:
    """
    Fetch leads from Leadspedia API.
    
    Args:
        client: Leadspedia API client
        query: Query parameters
        
    Yields:
        Lead records as dictionaries
    """
    # Note: Leadspedia endpoints require .do suffix
    pages = client.get_paged("leads/getAll.do", params=query.to_params())
    yield from iter_data_from_pages(pages)


def fetch_sold_leads(
    client: LeadspediaClient,
    query: LeadQuery,
) -> Iterator[Dict[str, Any]]:
    """
    Fetch sold leads from Leadspedia API.
    
    This endpoint specifically returns leads that have been sold,
    which is useful for revenue tracking.
    
    Args:
        client: Leadspedia API client
        query: Query parameters
        
    Yields:
        Sold lead records as dictionaries
    """
    pages = client.get_paged("leads/getSold.do", params=query.to_params())
    yield from iter_data_from_pages(pages)


def fetch_affiliate_clicks(
    client: LeadspediaClient,
    query: AffiliateClickQuery,
) -> Iterator[Dict[str, Any]]:
    """
    Fetch affiliate click data from Leadspedia API.
    
    This endpoint returns click-level data which can be matched
    to Meta leads via sub_id or tracking parameters.
    
    Args:
        client: Leadspedia API client
        query: Query parameters
        
    Yields:
        Click records as dictionaries
    """
    pages = client.get_paged("affiliateClicks/getAll", params=query.to_params())
    yield from iter_data_from_pages(pages)


def fetch_lead_report(
    client: LeadspediaClient,
    query: LeadQuery,
) -> Dict[str, Any]:
    """
    Fetch aggregated lead report from Leadspedia.
    
    Returns summary statistics rather than individual leads.
    
    Args:
        client: Leadspedia API client
        query: Query parameters
        
    Returns:
        Report data dictionary
    """
    return client.get("reports/leads", params=query.to_params())


@dataclass
class LeadDisposition:
    """Parsed lead disposition record."""

    lead_id: str
    external_id: Optional[str]  # Meta Lead ID or other external reference
    status: str  # 'sold', 'rejected', 'pending', 'returned'
    revenue: Decimal
    payout: Decimal
    cost: Decimal
    buyer_name: Optional[str]
    created_at: Optional[datetime]
    sold_at: Optional[datetime]
    vertical: Optional[str]
    campaign: Optional[str]
    affiliate_id: Optional[str]
    sub_id: Optional[str]  # Often contains tracking info
    raw_data: Dict[str, Any]

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "LeadDisposition":
        """Parse a lead disposition from API response data."""
        # Leadspedia field mapping:
        # - sold: "Yes" or "No" (status indicator)
        # - CPL: cost per lead (what affiliate paid)
        # - RPL: revenue per lead (from getAll.do)
        # - price: sale price (from getSold.do)
        # - createdOn: creation datetime
        # - dateSold: sold datetime (from getSold.do)
        # - buyerName: buyer name (from getSold.do)
        # - returned: "Yes" or "No" (return status from getSold.do)
        
        # Determine status from Leadspedia fields
        sold_field = str(data.get("sold", "")).lower()
        returned_field = str(data.get("returned", "")).lower()
        status_field = data.get("status") or data.get("disposition")
        
        if status_field:
            status = str(status_field).lower()
        elif returned_field == "yes":
            status = "returned"
        elif sold_field == "yes":
            status = "sold"
        elif sold_field == "no":
            status = "pending"  # Not sold yet
        else:
            status = "unknown"
        
        # Revenue: use price (getSold.do) or RPL (getAll.do)
        revenue = _safe_decimal(
            data.get("price") or 
            data.get("RPL") or 
            data.get("revenue") or 
            data.get("soldPrice")
        )
        
        # Cost: use CPL (cost per lead)
        cost = _safe_decimal(
            data.get("CPL") or 
            data.get("cost") or 
            data.get("leadCost")
        )
        
        # Payout (affiliate payout)
        payout = _safe_decimal(
            data.get("payout") or 
            data.get("affiliatePayout") or
            data.get("PPL")  # Pay per lead
        )
        
        return cls(
            lead_id=str(data.get("leadID") or data.get("id") or ""),
            external_id=data.get("externalID") or data.get("sub_id") or data.get("subID"),
            status=status,
            revenue=revenue,
            payout=payout,
            cost=cost,
            buyer_name=data.get("buyerName") or data.get("buyer") or data.get("contractName"),
            created_at=_parse_datetime(data.get("createdOn") or data.get("createdAt") or data.get("created")),
            sold_at=_parse_datetime(data.get("dateSold") or data.get("soldAt") or data.get("soldDate")),
            vertical=data.get("verticalName") or data.get("vertical"),
            campaign=data.get("campaignName") or data.get("campaign"),
            affiliate_id=str(data.get("affiliateID") or data.get("affiliate_id") or ""),
            sub_id=data.get("subID") or data.get("sub_id") or data.get("subId") or data.get("s1"),
            raw_data=data,
        )

    @property
    def is_sold(self) -> bool:
        """Check if this lead was sold."""
        return self.status in ("sold", "accepted", "approved")

    @property
    def is_rejected(self) -> bool:
        """Check if this lead was rejected."""
        return self.status in ("rejected", "declined", "returned")

    @property
    def is_pending(self) -> bool:
        """Check if this lead is still pending."""
        return self.status in ("pending", "new", "queued")

    @property
    def net_revenue(self) -> Decimal:
        """Calculate net revenue (revenue minus cost/payout)."""
        return self.revenue - self.payout

    @property
    def margin(self) -> Optional[Decimal]:
        """Calculate margin percentage."""
        if self.revenue <= 0:
            return None
        return ((self.revenue - self.payout) / self.revenue) * 100


def parse_leads_to_dispositions(
    rows: Iterable[Dict[str, Any]],
) -> List[LeadDisposition]:
    """
    Parse raw API lead data into LeadDisposition objects.
    
    Args:
        rows: Raw lead data from API
        
    Returns:
        List of parsed LeadDisposition objects
    """
    dispositions = []
    for row in rows:
        try:
            disposition = LeadDisposition.from_api_response(row)
            dispositions.append(disposition)
        except Exception:
            # Skip malformed records
            continue
    return dispositions


def leads_to_dataframe(dispositions: Sequence[LeadDisposition]) -> pd.DataFrame:
    """
    Convert lead dispositions to a pandas DataFrame.
    
    Args:
        dispositions: List of LeadDisposition objects
        
    Returns:
        DataFrame with lead data
    """
    if not dispositions:
        return pd.DataFrame()

    records = []
    for d in dispositions:
        records.append({
            "lead_id": d.lead_id,
            "external_id": d.external_id,
            "status": d.status,
            "revenue": float(d.revenue),
            "payout": float(d.payout),
            "cost": float(d.cost),
            "net_revenue": float(d.net_revenue),
            "margin_pct": float(d.margin) if d.margin is not None else None,
            "is_sold": d.is_sold,
            "buyer_name": d.buyer_name,
            "created_at": d.created_at,
            "sold_at": d.sold_at,
            "vertical": d.vertical,
            "campaign": d.campaign,
            "affiliate_id": d.affiliate_id,
            "sub_id": d.sub_id,
        })

    return pd.DataFrame(records)


def fetch_leads_cached(
    client: LeadspediaClient,
    cache: SqliteCache,
    query: LeadQuery,
    *,
    ttl_seconds: int,
) -> pd.DataFrame:
    """
    Fetch leads with caching.
    
    Args:
        client: Leadspedia API client
        cache: SQLite cache instance
        query: Query parameters
        ttl_seconds: Cache TTL in seconds
        
    Returns:
        DataFrame with lead disposition data
    """
    key_material = {
        "source": "leadspedia_leads",
        "since": query.since.isoformat(),
        "until": query.until.isoformat(),
        "affiliate_id": query.affiliate_id,
        "campaign_id": query.campaign_id,
        "vertical_id": query.vertical_id,
        "status": query.status,
    }
    cache_key = sha256_key(json.dumps(key_material, sort_keys=True, separators=(",", ":")))

    cached = cache.get(cache_key, ttl_seconds=ttl_seconds)
    if cached:
        try:
            return pd.read_json(cached, orient="records")
        except Exception:
            pass

    rows = fetch_leads(client, query)
    dispositions = parse_leads_to_dispositions(rows)
    df = leads_to_dataframe(dispositions)
    
    if not df.empty:
        cache.set(cache_key, df.to_json(orient="records", date_format="iso"))
    
    return df


def aggregate_lead_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate aggregate statistics from lead data.
    
    Args:
        df: DataFrame with lead data
        
    Returns:
        Dictionary of aggregate statistics
    """
    if df.empty:
        return {
            "total_leads": 0,
            "sold_leads": 0,
            "rejected_leads": 0,
            "pending_leads": 0,
            "total_revenue": 0.0,
            "total_payout": 0.0,
            "total_net_revenue": 0.0,
            "sell_through_rate": 0.0,
            "avg_revenue_per_lead": 0.0,
            "avg_revenue_per_sold": 0.0,
        }

    total_leads = len(df)
    sold_leads = df["is_sold"].sum() if "is_sold" in df.columns else 0
    rejected_leads = len(df[df["status"].isin(["rejected", "declined", "returned"])]) if "status" in df.columns else 0
    pending_leads = len(df[df["status"].isin(["pending", "new", "queued"])]) if "status" in df.columns else 0

    total_revenue = df["revenue"].sum() if "revenue" in df.columns else 0.0
    total_payout = df["payout"].sum() if "payout" in df.columns else 0.0
    total_net_revenue = df["net_revenue"].sum() if "net_revenue" in df.columns else total_revenue - total_payout

    sell_through_rate = (sold_leads / total_leads * 100) if total_leads > 0 else 0.0
    avg_revenue_per_lead = total_revenue / total_leads if total_leads > 0 else 0.0
    avg_revenue_per_sold = total_revenue / sold_leads if sold_leads > 0 else 0.0

    return {
        "total_leads": int(total_leads),
        "sold_leads": int(sold_leads),
        "rejected_leads": int(rejected_leads),
        "pending_leads": int(pending_leads),
        "total_revenue": float(total_revenue),
        "total_payout": float(total_payout),
        "total_net_revenue": float(total_net_revenue),
        "sell_through_rate": float(sell_through_rate),
        "avg_revenue_per_lead": float(avg_revenue_per_lead),
        "avg_revenue_per_sold": float(avg_revenue_per_sold),
    }

