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


@dataclass
class LeadspediaAdvertiser:
    """Represents a Leadspedia advertiser (buyer)."""
    
    id: str
    name: str
    status: str
    email: Optional[str] = None
    company: Optional[str] = None
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "LeadspediaAdvertiser":
        return cls(
            id=str(data.get("advertiserID") or data.get("id") or ""),
            name=str(data.get("advertiserName") or data.get("name") or ""),
            status=str(data.get("status") or "active"),
            email=data.get("email"),
            company=data.get("company"),
        )


@dataclass
class LeadspediaContract:
    """Represents a Leadspedia lead distribution contract."""
    
    id: str
    name: str
    advertiser_id: str
    advertiser_name: str
    status: str
    price: Decimal
    vertical_id: Optional[str] = None
    vertical_name: Optional[str] = None
    daily_cap: Optional[int] = None
    leads_today: Optional[int] = None
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "LeadspediaContract":
        price_val = data.get("price") or data.get("pricePerLead") or "0"
        try:
            price = Decimal(str(price_val))
        except (InvalidOperation, ValueError):
            price = Decimal("0")
        
        daily_cap = data.get("dailyCap") or data.get("leadsDaily")
        leads_today = data.get("leadsToday") or data.get("todayLeads")
        
        return cls(
            id=str(data.get("contractID") or data.get("id") or ""),
            name=str(data.get("contractName") or data.get("name") or ""),
            advertiser_id=str(data.get("advertiserID") or ""),
            advertiser_name=str(data.get("advertiserName") or ""),
            status=str(data.get("status") or "active"),
            price=price,
            vertical_id=str(data.get("verticalID") or "") if data.get("verticalID") else None,
            vertical_name=data.get("verticalName"),
            daily_cap=int(daily_cap) if daily_cap else None,
            leads_today=int(leads_today) if leads_today else None,
        )


def fetch_advertisers(client: LeadspediaClient, limit: int = 1000) -> List[LeadspediaAdvertiser]:
    """
    Fetch all advertisers (buyers) from Leadspedia.
    
    Args:
        client: Leadspedia API client
        limit: Maximum number of advertisers to fetch (default 1000)
        
    Returns:
        List of LeadspediaAdvertiser objects
    """
    try:
        response = client.get("advertisers/getAll.do", params={"limit": limit})
        
        # API returns: { "response": { "data": [...] } }
        inner_response = response.get("response", {})
        if isinstance(inner_response, dict):
            data = inner_response.get("data", [])
        else:
            data = response.get("data") or []
        
        if isinstance(data, list):
            return [LeadspediaAdvertiser.from_api_response(a) for a in data if isinstance(a, dict)]
    except Exception as e:
        logger.error(f"Failed to fetch advertisers: {e}")
    return []


def fetch_contracts(client: LeadspediaClient, limit: int = 1000) -> List[LeadspediaContract]:
    """
    Fetch all lead distribution contracts from Leadspedia.
    
    Args:
        client: Leadspedia API client
        limit: Maximum number of contracts to fetch (default 1000)
        
    Returns:
        List of LeadspediaContract objects
    """
    try:
        response = client.get("leadDistributionContracts/getAll.do", params={"limit": limit})
        
        # API returns: { "response": { "data": [...] } }
        inner_response = response.get("response", {})
        if isinstance(inner_response, dict):
            data = inner_response.get("data", [])
        else:
            data = response.get("data") or []
        
        if isinstance(data, list):
            return [LeadspediaContract.from_api_response(c) for c in data if isinstance(c, dict)]
    except Exception as e:
        logger.error(f"Failed to fetch contracts: {e}")
    return []


def fetch_advertisers_cached(
    client: LeadspediaClient,
    cache: SqliteCache,
    ttl_seconds: int = 3600,
) -> List[LeadspediaAdvertiser]:
    """Fetch advertisers with caching."""
    cache_key = sha256_key("leadspedia_advertisers")
    cached = cache.get(cache_key, ttl_seconds=ttl_seconds)
    
    if cached:
        try:
            data = json.loads(cached)
            return [LeadspediaAdvertiser(
                id=a["id"], name=a["name"], status=a["status"],
                email=a.get("email"), company=a.get("company")
            ) for a in data]
        except (json.JSONDecodeError, KeyError):
            pass
    
    advertisers = fetch_advertisers(client)
    
    if advertisers:
        cache_data = [{"id": a.id, "name": a.name, "status": a.status, 
                       "email": a.email, "company": a.company} for a in advertisers]
        cache.set(cache_key, json.dumps(cache_data))
    
    return advertisers


def fetch_contracts_cached(
    client: LeadspediaClient,
    cache: SqliteCache,
    ttl_seconds: int = 300,  # 5 min cache - contracts change more often
) -> List[LeadspediaContract]:
    """Fetch contracts with caching."""
    cache_key = sha256_key("leadspedia_contracts")
    cached = cache.get(cache_key, ttl_seconds=ttl_seconds)
    
    if cached:
        try:
            data = json.loads(cached)
            return [LeadspediaContract(
                id=c["id"], name=c["name"], advertiser_id=c["advertiser_id"],
                advertiser_name=c["advertiser_name"], status=c["status"],
                price=Decimal(str(c["price"])), vertical_id=c.get("vertical_id"),
                vertical_name=c.get("vertical_name"), daily_cap=c.get("daily_cap"),
                leads_today=c.get("leads_today")
            ) for c in data]
        except (json.JSONDecodeError, KeyError):
            pass
    
    contracts = fetch_contracts(client)
    
    if contracts:
        cache_data = [{
            "id": c.id, "name": c.name, "advertiser_id": c.advertiser_id,
            "advertiser_name": c.advertiser_name, "status": c.status,
            "price": str(c.price), "vertical_id": c.vertical_id,
            "vertical_name": c.vertical_name, "daily_cap": c.daily_cap,
            "leads_today": c.leads_today
        } for c in contracts]
        cache.set(cache_key, json.dumps(cache_data))
    
    return contracts


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


@dataclass
class ReturnQuery:
    """Query parameters for fetching returned/rejected leads."""
    
    since: date
    until: Optional[date] = None
    campaign_id: Optional[int] = None
    affiliate_id: Optional[int] = None
    vertical_id: Optional[int] = None
    advertiser_id: Optional[int] = None
    contract_id: Optional[int] = None
    status: Optional[str] = None  # Pending, Approved, Rejected, Attempted Contact, Researching
    
    def to_params(self) -> Dict[str, Any]:
        """Convert to API query parameters."""
        params: Dict[str, Any] = {
            "fromDate": self.since.strftime("%Y-%m-%d"),
        }
        if self.until:
            params["toDate"] = self.until.strftime("%Y-%m-%d")
        if self.campaign_id:
            params["campaignID"] = self.campaign_id
        if self.affiliate_id:
            params["affiliateID"] = self.affiliate_id
        if self.vertical_id:
            params["verticalID"] = self.vertical_id
        if self.advertiser_id:
            params["advertiserID"] = self.advertiser_id
        if self.contract_id:
            params["contractID"] = self.contract_id
        if self.status:
            params["status"] = self.status
        return params


def fetch_returns(
    client: LeadspediaClient,
    query: ReturnQuery,
) -> Iterator[Dict[str, Any]]:
    """
    Fetch returned/rejected leads from Leadspedia API.
    
    This endpoint returns leads that have been returned by buyers,
    with status options: Pending, Approved, Rejected, Attempted Contact, Researching.
    
    Args:
        client: Leadspedia API client
        query: Query parameters
        
    Yields:
        Return records as dictionaries
    """
    pages = client.get_paged("leads/getReturns.do", params=query.to_params())
    yield from iter_data_from_pages(pages)


def fetch_delivered_leads(
    client: LeadspediaClient,
    query: LeadQuery,
) -> Iterator[Dict[str, Any]]:
    """
    Fetch delivered leads from Leadspedia API.
    
    This endpoint returns leads that were delivered to buyers,
    including both sold and unsold leads. Useful for tracking
    leads that were posted but not accepted.
    
    Args:
        client: Leadspedia API client
        query: Query parameters (same as LeadQuery)
        
    Yields:
        Delivered lead records as dictionaries
    """
    pages = client.get_paged("leads/getDelivered.do", params=query.to_params())
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
    status: str  # 'sold', 'rejected', 'pending', 'returned', 'unsold'
    revenue: Decimal
    payout: Decimal
    cost: Decimal
    buyer_name: Optional[str]
    contract_name: Optional[str]  # Contract/offer name
    created_at: Optional[datetime]
    sold_at: Optional[datetime]
    delivered_at: Optional[datetime]  # When delivered to buyer
    vertical: Optional[str]
    campaign: Optional[str]  # LP campaign name
    affiliate_id: Optional[str]
    sub_id: Optional[str]  # Often contains tracking info
    return_reason: Optional[str]  # Buyer rejection/return reason (Message Token)
    raw_data: Dict[str, Any]

    @classmethod
    def from_api_response(
        cls, 
        data: Dict[str, Any], 
        from_sold_endpoint: bool = False,
        from_delivered_endpoint: bool = False,
        from_all_endpoint: bool = False,
    ) -> "LeadDisposition":
        """Parse a lead disposition from API response data.
        
        Args:
            data: Raw API response data
            from_sold_endpoint: If True, leads are from getSold.do (all sold)
            from_delivered_endpoint: If True, leads are from getDelivered.do 
                                    (check soldID to determine if sold)
            from_all_endpoint: If True, leads are from getAll.do
                              (check sold/trash/scrubbed fields)
        """
        # Leadspedia field mapping:
        # - sold: "Yes" or "No" (status indicator)
        # - trash: "Yes" or "No" (lead was trashed/rejected)
        # - scrubbed: "Yes" or "No" (lead was scrubbed)
        # - soldID: If present and non-empty, lead was sold
        # - lp_post_response: Buyer rejection message (Message Token)
        # - disposition: Also contains rejection reason
        # - CPL: cost per lead (what affiliate paid)
        # - RPL: revenue per lead (from getAll.do)
        # - price: sale price (from getSold.do)
        # - returned: "Yes" or "No" (return status)
        # - returnReason: Buyer rejection/return reason
        
        # Determine status from Leadspedia fields
        sold_field = str(data.get("sold", "")).lower()
        returned_field = str(data.get("returned", "")).lower()
        trash_field = str(data.get("trash", "")).lower()
        scrubbed_field = str(data.get("scrubbed", "")).lower()
        status_field = data.get("status") or data.get("disposition")
        sold_id = data.get("soldID") or data.get("sold_id")
        
        if from_sold_endpoint:
            # Leads from getSold.do are sold by definition (unless returned)
            if returned_field == "yes":
                status = "returned"
            else:
                status = "sold"
        elif from_delivered_endpoint:
            # Leads from getDelivered.do - check soldID to determine if sold
            if returned_field == "yes":
                status = "returned"
            elif sold_id and str(sold_id).strip():
                status = "sold"
            else:
                status = "unsold"  # Delivered but not sold
        elif from_all_endpoint:
            # Leads from getAll.do - check sold/trash/scrubbed fields
            if returned_field == "yes":
                status = "returned"
            elif sold_field == "yes":
                status = "sold"
            elif trash_field == "yes":
                status = "trashed"  # Rejected/trashed
            elif scrubbed_field == "yes":
                status = "scrubbed"
            else:
                status = "unsold"  # Not sold yet
        elif status_field:
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
        
        # Message Token: lp_post_response contains the buyer rejection/response message
        # This is the primary field for rejection reasons; fallback to returnReason for returned leads
        message_token = (
            data.get("lp_post_response") or 
            data.get("disposition") or
            data.get("returnReason") or 
            data.get("return_reason") or 
            data.get("rejectReason")
        )
        
        return cls(
            lead_id=str(data.get("leadID") or data.get("id") or ""),
            external_id=data.get("externalID") or data.get("sub_id") or data.get("subID"),
            status=status,
            revenue=revenue,
            payout=payout,
            cost=cost,
            buyer_name=data.get("buyerName") or data.get("buyer"),
            contract_name=data.get("contractName") or data.get("contract"),
            created_at=_parse_datetime(data.get("createdOn") or data.get("createdAt") or data.get("created")),
            sold_at=_parse_datetime(data.get("dateSold") or data.get("soldAt") or data.get("soldDate")),
            delivered_at=_parse_datetime(data.get("dateDelivered") or data.get("deliveredAt")),
            vertical=data.get("verticalName") or data.get("vertical"),
            campaign=data.get("campaignName") or data.get("campaign"),
            affiliate_id=str(data.get("affiliateID") or data.get("affiliate_id") or ""),
            sub_id=data.get("subID") or data.get("sub_id") or data.get("subId") or data.get("s1"),
            return_reason=message_token,  # Now uses lp_post_response as primary source
            raw_data=data,
        )

    @property
    def is_sold(self) -> bool:
        """Check if this lead was sold."""
        return self.status in ("sold", "accepted", "approved")

    @property
    def is_rejected(self) -> bool:
        """Check if this lead was rejected/returned/trashed."""
        return self.status in ("rejected", "declined", "returned", "trashed", "scrubbed")

    @property
    def is_unsold(self) -> bool:
        """Check if this lead was not sold (trashed, scrubbed, or pending)."""
        return self.status in ("unsold", "trashed", "scrubbed", "pending")

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

    # Meta attribution properties - extracted from lp_s* custom fields
    # Mapping: lp_s2=Ad Name, lp_s3=Ad Set Name, lp_s4=Campaign Name, lp_s5=Platform
    
    @property
    def meta_campaign_name(self) -> str:
        """Facebook Campaign Name from lp_s4."""
        return str(self.raw_data.get("lp_s4") or self.raw_data.get("s4") or "")
    
    @property
    def meta_adset_name(self) -> str:
        """Facebook Ad Set Name from lp_s3."""
        return str(self.raw_data.get("lp_s3") or self.raw_data.get("s3") or "")
    
    @property
    def meta_ad_name(self) -> str:
        """Facebook Ad Name from lp_s2."""
        return str(self.raw_data.get("lp_s2") or self.raw_data.get("s2") or "")
    
    @property
    def meta_platform(self) -> str:
        """Facebook Platform from lp_s5."""
        return str(self.raw_data.get("lp_s5") or self.raw_data.get("s5") or "")
    
    @property
    def has_meta_attribution(self) -> bool:
        """Check if this lead has Meta campaign attribution."""
        return bool(self.meta_campaign_name)
    
    @property
    def problems(self) -> List[str]:
        """Return list of problem indicators for this lead."""
        issues = []
        if self.is_rejected:
            issues.append("returned")
        if self.is_unsold:
            issues.append("unsold")
        if self.status == "pending":
            issues.append("pending_return")
        if self.revenue > 0 and self.net_revenue < 0:
            issues.append("negative_margin")
        if not self.has_meta_attribution:
            issues.append("no_meta_match")
        if self.return_reason:
            issues.append("has_rejection_reason")
        return issues


def parse_leads_to_dispositions(
    rows: Iterable[Dict[str, Any]],
    from_sold_endpoint: bool = False,
    from_delivered_endpoint: bool = False,
    from_all_endpoint: bool = False,
) -> List[LeadDisposition]:
    """
    Parse raw API lead data into LeadDisposition objects.
    
    Args:
        rows: Raw lead data from API
        from_sold_endpoint: If True, all leads are marked as 'sold' (from getSold.do)
        from_delivered_endpoint: If True, leads are from getDelivered.do
                                 (check soldID to determine if sold/unsold)
        from_all_endpoint: If True, leads are from getAll.do
                          (check sold/trash/scrubbed fields)
        
    Returns:
        List of parsed LeadDisposition objects
    """
    dispositions = []
    for row in rows:
        try:
            disposition = LeadDisposition.from_api_response(
                row, 
                from_sold_endpoint=from_sold_endpoint,
                from_delivered_endpoint=from_delivered_endpoint,
                from_all_endpoint=from_all_endpoint,
            )
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
            # Meta attribution fields
            "meta_campaign": d.meta_campaign_name,
            "meta_adset": d.meta_adset_name,
            "meta_ad": d.meta_ad_name,
            "meta_platform": d.meta_platform,
            "has_meta_match": d.has_meta_attribution,
            "problems": ", ".join(d.problems) if d.problems else "",
        })

    return pd.DataFrame(records)


def leads_to_lead_log_dataframe(dispositions: Sequence[LeadDisposition]) -> pd.DataFrame:
    """
    Convert lead dispositions to a Lead Log DataFrame for granular reporting.
    
    This provides a detailed view suitable for the Lead Log UI, with columns
    optimized for marketing analysis.
    
    Args:
        dispositions: List of LeadDisposition objects
        
    Returns:
        DataFrame with Lead Log data
    """
    if not dispositions:
        return pd.DataFrame()

    records = []
    for d in dispositions:
        # Determine status emoji for quick visual scanning
        status_icon = {
            "sold": "✅",
            "returned": "🔄",
            "rejected": "❌",
            "pending": "⏳",
            "unsold": "⚠️",
            "trashed": "🗑️",
            "scrubbed": "🧹",
        }.get(d.status, "❓")
        
        # Calculate margin for display
        margin_val = float(d.margin) if d.margin is not None else None
        
        records.append({
            "Lead ID": d.lead_id,
            "Status": f"{status_icon} {d.status.title()}",
            "Meta Campaign": d.meta_campaign_name or "—",
            "Ad Set": d.meta_adset_name or "—",
            "Ad": d.meta_ad_name or "—",
            "Buyer": d.buyer_name or "—",
            "Contract": d.contract_name or "—",
            "Revenue": float(d.revenue),
            "Payout": float(d.payout),
            "Margin": float(d.net_revenue),
            "Margin %": margin_val,
            "Created": d.created_at.strftime("%m/%d %H:%M") if d.created_at else "—",
            "Sold": d.sold_at.strftime("%m/%d %H:%M") if d.sold_at else "—",
            "Problems": ", ".join(d.problems) if d.problems else "—",
            "Message Token": d.return_reason or "—",
            "Vertical": d.vertical or "—",
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


@dataclass
class BuyerPerformance:
    """Aggregated performance metrics for a buyer."""
    
    buyer_name: str
    leads_sold: int
    total_revenue: Decimal
    avg_price: Decimal
    pct_of_total: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "buyer_name": self.buyer_name,
            "leads_sold": self.leads_sold,
            "total_revenue": float(self.total_revenue),
            "avg_price": float(self.avg_price),
            "pct_of_total": self.pct_of_total,
        }


def aggregate_by_buyer(dispositions: List[LeadDisposition]) -> List[BuyerPerformance]:
    """
    Aggregate lead dispositions by buyer name.
    
    Args:
        dispositions: List of LeadDisposition objects
        
    Returns:
        List of BuyerPerformance objects sorted by revenue descending
    """
    if not dispositions:
        return []
    
    # Filter to sold leads only
    sold_leads = [d for d in dispositions if d.is_sold]
    if not sold_leads:
        return []
    
    # Aggregate by buyer
    buyer_stats: Dict[str, Dict[str, Any]] = {}
    total_revenue = Decimal("0")
    
    for d in sold_leads:
        buyer = d.buyer_name or "Unknown"
        if buyer not in buyer_stats:
            buyer_stats[buyer] = {"leads": 0, "revenue": Decimal("0")}
        buyer_stats[buyer]["leads"] += 1
        buyer_stats[buyer]["revenue"] += d.revenue
        total_revenue += d.revenue
    
    # Build performance objects
    results = []
    for buyer, stats in buyer_stats.items():
        leads = stats["leads"]
        revenue = stats["revenue"]
        avg_price = revenue / leads if leads > 0 else Decimal("0")
        pct = float(revenue / total_revenue * 100) if total_revenue > 0 else 0.0
        
        results.append(BuyerPerformance(
            buyer_name=buyer,
            leads_sold=leads,
            total_revenue=revenue,
            avg_price=avg_price,
            pct_of_total=pct,
        ))
    
    # Sort by revenue descending
    results.sort(key=lambda x: x.total_revenue, reverse=True)
    return results


def buyer_performance_to_dataframe(performances: List[BuyerPerformance]) -> pd.DataFrame:
    """Convert buyer performance list to DataFrame for display."""
    if not performances:
        return pd.DataFrame(columns=["Buyer", "Leads Sold", "Revenue", "Avg Price", "% of Total"])
    
    data = []
    for p in performances:
        data.append({
            "Buyer": p.buyer_name,
            "Leads Sold": p.leads_sold,
            "Revenue": f"${float(p.total_revenue):,.2f}",
            "Avg Price": f"${float(p.avg_price):,.2f}",
            "% of Total": f"{p.pct_of_total:.1f}%",
        })
    
    return pd.DataFrame(data)

