"""
Leadspedia API integration module.

This module provides client and data fetching capabilities for the Leadspedia API,
enabling revenue tracking and lead disposition data retrieval.
"""

from app.leadspedia.client import LeadspediaClient, LeadspediaApiError
from app.leadspedia.leads import (
    LeadQuery,
    AffiliateClickQuery,
    LeadDisposition,
    LeadspediaAdvertiser,
    LeadspediaContract,
    LeadspediaVertical,
    LeadspediaAffiliate,
    BuyerPerformance,
    fetch_leads,
    fetch_leads_cached,
    fetch_affiliate_clicks,
    aggregate_lead_stats,
    aggregate_by_buyer,
    buyer_performance_to_dataframe,
    fetch_advertisers,
    fetch_advertisers_cached,
    fetch_contracts,
    fetch_contracts_cached,
    fetch_verticals,
    fetch_verticals_cached,
)
from app.leadspedia.matching import (
    MatchedLeadData,
    MatchResult,
    match_meta_to_leadspedia,
    matched_data_to_dataframe,
    fetch_and_match_data_cached,
)

__all__ = [
    "LeadspediaClient",
    "LeadspediaApiError",
    "LeadQuery",
    "AffiliateClickQuery",
    "LeadDisposition",
    "LeadspediaAdvertiser",
    "LeadspediaContract",
    "LeadspediaVertical",
    "LeadspediaAffiliate",
    "BuyerPerformance",
    "fetch_leads",
    "fetch_leads_cached",
    "fetch_affiliate_clicks",
    "aggregate_lead_stats",
    "aggregate_by_buyer",
    "buyer_performance_to_dataframe",
    "fetch_advertisers",
    "fetch_advertisers_cached",
    "fetch_contracts",
    "fetch_contracts_cached",
    "fetch_verticals",
    "fetch_verticals_cached",
    "MatchedLeadData",
    "MatchResult",
    "match_meta_to_leadspedia",
    "matched_data_to_dataframe",
    "fetch_and_match_data_cached",
]

