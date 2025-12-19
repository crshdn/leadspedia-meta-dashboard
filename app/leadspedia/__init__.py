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
    fetch_leads,
    fetch_leads_cached,
    fetch_affiliate_clicks,
    aggregate_lead_stats,
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
    "fetch_leads",
    "fetch_leads_cached",
    "fetch_affiliate_clicks",
    "aggregate_lead_stats",
    "MatchedLeadData",
    "MatchResult",
    "match_meta_to_leadspedia",
    "matched_data_to_dataframe",
    "fetch_and_match_data_cached",
]

