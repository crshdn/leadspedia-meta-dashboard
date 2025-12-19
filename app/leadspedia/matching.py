"""
Lead matching between Meta Ads and Leadspedia.

This module provides functionality to match Meta leads to Leadspedia
lead dispositions, enabling combined KPI calculations.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional, Sequence

import pandas as pd

from app.cache.sqlite_cache import SqliteCache, sha256_key
from app.config import AppConfig, CampaignMapping
from app.config_manager import ConfigManager, CampaignConfig
from app.leadspedia.client import LeadspediaClient
from app.leadspedia.leads import (
    LeadQuery,
    LeadDisposition,
    fetch_leads,
    fetch_sold_leads,
    parse_leads_to_dispositions,
    aggregate_lead_stats,
)


@dataclass
class MatchedLeadData:
    """Combined data from Meta and Leadspedia for matched leads."""
    
    # Meta Ads data
    campaign_id: str
    campaign_name: str
    adset_id: str
    adset_name: str
    ad_id: str
    ad_name: str
    spend: float
    meta_leads: int
    impressions: int
    clicks: int
    cpl: float  # Meta CPL
    
    # Leadspedia data (aggregated for this ad/adset/campaign)
    lp_total_leads: int
    lp_sold_leads: int
    lp_rejected_leads: int
    lp_pending_leads: int
    lp_revenue: float
    lp_payout: float
    lp_net_revenue: float
    
    # Calculated KPIs
    sell_through_rate: float  # (sold / total) * 100
    avg_sale_price: float  # revenue / sold
    roi: float  # ((revenue - spend) / spend) * 100
    profit: float  # revenue - spend
    profit_per_lead: float
    epc: float  # Earnings per click
    epl: float  # Earnings per lead
    break_even_cpl: float  # avg_sale_price * (sell_through_rate / 100)


@dataclass
class MatchResult:
    """Result of matching Meta and Leadspedia data."""
    
    matched_data: List[MatchedLeadData]
    unmatched_meta_campaigns: List[str]  # Campaign IDs with no Leadspedia mapping
    meta_lead_count: int
    lp_lead_count: int
    match_rate: float  # Percentage of Meta leads matched in Leadspedia


def fetch_leadspedia_data_for_campaign(
    client: LeadspediaClient,
    mapping: CampaignMapping,
    since: date,
    until: date,
) -> List[LeadDisposition]:
    """
    Fetch Leadspedia data for a specific campaign mapping.
    
    Args:
        client: Leadspedia API client
        mapping: Campaign mapping configuration
        since: Start date
        until: End date
        
    Returns:
        List of LeadDisposition objects
    """
    query = LeadQuery(
        since=since,
        until=until,
        affiliate_id=mapping.affiliate_id if mapping.affiliate_id else None,
        vertical_id=mapping.vertical if mapping.vertical else None,
    )
    rows = fetch_leads(client, query)
    return parse_leads_to_dispositions(rows)


def match_meta_to_leadspedia(
    meta_df: pd.DataFrame,
    lp_dispositions: List[LeadDisposition],
    cfg: AppConfig,
    *,
    campaign_config: Optional[CampaignConfig] = None,
) -> MatchResult:
    """
    Match Meta Ads data to Leadspedia lead dispositions.
    
    This function matches at the campaign level using the configured
    campaign mappings. For more granular matching (ad-level), the
    Lead ID or sub_id would need to contain ad-level tracking info.
    
    Args:
        meta_df: DataFrame from Meta Ads insights
        lp_dispositions: List of Leadspedia lead dispositions
        cfg: Application configuration with campaign mappings
        campaign_config: Optional campaign configuration from ConfigManager
        
    Returns:
        MatchResult with combined data
    """
    if meta_df.empty:
        return MatchResult(
            matched_data=[],
            unmatched_meta_campaigns=[],
            meta_lead_count=0,
            lp_lead_count=len(lp_dispositions),
            match_rate=0.0,
        )

    matched_data: List[MatchedLeadData] = []
    unmatched_campaigns: List[str] = []
    
    # Aggregate LP stats ONCE for all dispositions
    # This will be distributed proportionally across all Meta rows
    global_lp_stats = _aggregate_lp_dispositions(lp_dispositions)
    
    # Calculate total Meta leads across ALL campaigns for global proportional distribution
    total_global_meta_leads = int(meta_df["leads"].sum()) if "leads" in meta_df.columns else 0
    
    print(f"[DEBUG] Global LP stats: total={global_lp_stats['total']}, sold={global_lp_stats['sold']}, revenue=${global_lp_stats['revenue']:.2f}")
    print(f"[DEBUG] Total Meta leads across all campaigns: {total_global_meta_leads}")
    print(f"[DEBUG] Total Meta rows: {len(meta_df)}")
    
    # Process each row in the Meta dataframe
    # Distribute LP data proportionally based on each row's share of GLOBAL Meta leads
    for _, row in meta_df.iterrows():
        campaign_id = str(row.get("campaign_id", ""))
        meta_leads_for_row = int(row.get("leads", 0) or 0)
        
        # Calculate this row's proportion of the GLOBAL total leads
        if total_global_meta_leads > 0 and meta_leads_for_row > 0:
            proportion = meta_leads_for_row / total_global_meta_leads
        else:
            proportion = 0.0
        
        # Get mapping if available (for future use)
        mapping: Optional[CampaignMapping] = cfg.get_campaign_mapping(campaign_id)
        if not mapping:
            unmatched_campaigns.append(campaign_id)
        
        matched = _create_matched_data_proportional(row, global_lp_stats, proportion, mapping)
        if matched:
            matched_data.append(matched)

    meta_lead_count = int(meta_df["leads"].sum()) if "leads" in meta_df.columns else 0
    lp_lead_count = len(lp_dispositions)
    
    # Calculate match rate based on leads that have corresponding Leadspedia data
    matched_lp_count = sum(m.lp_total_leads for m in matched_data)
    matched_sold_count = sum(m.lp_sold_leads for m in matched_data)
    matched_revenue = sum(m.lp_revenue for m in matched_data)
    match_rate = (matched_lp_count / meta_lead_count * 100) if meta_lead_count > 0 else 0.0
    
    print(f"[DEBUG] Matching complete: {len(matched_data)} rows created")
    print(f"[DEBUG] Distributed LP totals: {matched_lp_count} leads, {matched_sold_count} sold, ${matched_revenue:.2f} revenue")

    return MatchResult(
        matched_data=matched_data,
        unmatched_meta_campaigns=unmatched_campaigns,
        meta_lead_count=meta_lead_count,
        lp_lead_count=lp_lead_count,
        match_rate=match_rate,
    )


def _create_matched_data_proportional(
    meta_row: pd.Series,
    lp_stats: Dict[str, Any],
    proportion: float,
    mapping: CampaignMapping,
) -> Optional[MatchedLeadData]:
    """
    Create matched data from a Meta row with proportionally distributed LP data.
    
    This distributes the campaign's LP totals proportionally to each ad based on
    the ad's share of the campaign's total Meta leads.
    
    Args:
        meta_row: Row from Meta DataFrame
        lp_stats: Pre-aggregated LP statistics for the campaign
        proportion: This row's proportion of the campaign total (0.0 to 1.0)
        mapping: Campaign mapping configuration
    """
    # Extract Meta data
    campaign_id = str(meta_row.get("campaign_id", ""))
    campaign_name = str(meta_row.get("campaign_name", ""))
    adset_id = str(meta_row.get("adset_id", ""))
    adset_name = str(meta_row.get("adset_name", ""))
    ad_id = str(meta_row.get("ad_id", ""))
    ad_name = str(meta_row.get("ad_name", ""))
    
    spend = float(meta_row.get("spend", 0) or 0)
    meta_leads = int(meta_row.get("leads", 0) or 0)
    impressions = int(meta_row.get("impressions", 0) or 0)
    clicks = int(meta_row.get("clicks", 0) or 0)
    cpl = float(meta_row.get("cpl", 0) or 0)
    
    # Distribute LP data proportionally based on this row's share of campaign leads
    lp_total = int(round(lp_stats["total"] * proportion))
    lp_sold = int(round(lp_stats["sold"] * proportion))
    lp_rejected = int(round(lp_stats["rejected"] * proportion))
    lp_pending = int(round(lp_stats["pending"] * proportion))
    lp_revenue = lp_stats["revenue"] * proportion
    lp_payout = lp_stats["payout"] * proportion
    lp_net_revenue = lp_revenue - lp_payout
    
    # Calculate KPIs
    sell_through_rate = (lp_sold / lp_total * 100) if lp_total > 0 else 0.0
    avg_sale_price = lp_revenue / lp_sold if lp_sold > 0 else 0.0
    roi = ((lp_revenue - spend) / spend * 100) if spend > 0 else 0.0
    profit = lp_revenue - spend
    profit_per_lead = profit / meta_leads if meta_leads > 0 else 0.0
    epc = lp_revenue / clicks if clicks > 0 else 0.0
    epl = lp_revenue / meta_leads if meta_leads > 0 else 0.0
    break_even_cpl = avg_sale_price * (sell_through_rate / 100) if avg_sale_price > 0 else 0.0
    
    return MatchedLeadData(
        campaign_id=campaign_id,
        campaign_name=campaign_name,
        adset_id=adset_id,
        adset_name=adset_name,
        ad_id=ad_id,
        ad_name=ad_name,
        spend=spend,
        meta_leads=meta_leads,
        impressions=impressions,
        clicks=clicks,
        cpl=cpl,
        lp_total_leads=lp_total,
        lp_sold_leads=lp_sold,
        lp_rejected_leads=lp_rejected,
        lp_pending_leads=lp_pending,
        lp_revenue=lp_revenue,
        lp_payout=lp_payout,
        lp_net_revenue=lp_net_revenue,
        sell_through_rate=sell_through_rate,
        avg_sale_price=avg_sale_price,
        roi=roi,
        profit=profit,
        profit_per_lead=profit_per_lead,
        epc=epc,
        epl=epl,
        break_even_cpl=break_even_cpl,
    )


def _aggregate_lp_dispositions(
    dispositions: List[LeadDisposition],
) -> Dict[str, Any]:
    """Aggregate Leadspedia disposition data."""
    if not dispositions:
        return {
            "total": 0,
            "sold": 0,
            "rejected": 0,
            "pending": 0,
            "revenue": 0.0,
            "payout": 0.0,
        }
    
    total = len(dispositions)
    sold = sum(1 for d in dispositions if d.is_sold)
    rejected = sum(1 for d in dispositions if d.is_rejected)
    pending = sum(1 for d in dispositions if d.is_pending)
    revenue = float(sum(d.revenue for d in dispositions))
    payout = float(sum(d.payout for d in dispositions))
    
    return {
        "total": total,
        "sold": sold,
        "rejected": rejected,
        "pending": pending,
        "revenue": revenue,
        "payout": payout,
    }


def matched_data_to_dataframe(
    matched: List[MatchedLeadData],
) -> pd.DataFrame:
    """Convert matched data to a pandas DataFrame."""
    if not matched:
        return pd.DataFrame()
    
    records = []
    for m in matched:
        records.append({
            "campaign_id": m.campaign_id,
            "campaign_name": m.campaign_name,
            "adset_id": m.adset_id,
            "adset_name": m.adset_name,
            "ad_id": m.ad_id,
            "ad_name": m.ad_name,
            "spend": m.spend,
            "meta_leads": m.meta_leads,
            "impressions": m.impressions,
            "clicks": m.clicks,
            "cpl": m.cpl,
            "lp_total_leads": m.lp_total_leads,
            "lp_sold_leads": m.lp_sold_leads,
            "lp_rejected_leads": m.lp_rejected_leads,
            "lp_pending_leads": m.lp_pending_leads,
            "revenue": m.lp_revenue,
            "payout": m.lp_payout,
            "net_revenue": m.lp_net_revenue,
            "sell_through_rate": m.sell_through_rate,
            "avg_sale_price": m.avg_sale_price,
            "roi": m.roi,
            "profit": m.profit,
            "profit_per_lead": m.profit_per_lead,
            "epc": m.epc,
            "epl": m.epl,
            "break_even_cpl": m.break_even_cpl,
        })
    
    return pd.DataFrame(records)


def fetch_and_match_data_cached(
    meta_df: pd.DataFrame,
    lp_client: LeadspediaClient,
    cache: SqliteCache,
    cfg: AppConfig,
    since: date,
    until: date,
    *,
    ttl_seconds: int,
    config_manager: Optional[ConfigManager] = None,
) -> pd.DataFrame:
    """
    Fetch Leadspedia data, match with Meta data, and return combined DataFrame.
    
    This function handles caching of the matched results.
    
    Args:
        meta_df: DataFrame from Meta Ads insights
        lp_client: Leadspedia API client
        cache: SQLite cache instance
        cfg: Application configuration
        since: Start date
        until: End date
        ttl_seconds: Cache TTL in seconds
        config_manager: Optional ConfigManager for campaign mappings
        
    Returns:
        DataFrame with combined and calculated KPI data
    """
    # Load campaign config from ConfigManager if available
    campaign_config: Optional[CampaignConfig] = None
    if config_manager:
        campaign_config = config_manager.load()
    
    # Determine affiliate ID
    affiliate_id = cfg.leadspedia_affiliate_id
    if campaign_config and campaign_config.affiliate_id:
        affiliate_id = campaign_config.affiliate_id
    
    # Build cache key
    config_hash = ""
    if campaign_config:
        config_hash = str(hash(json.dumps(campaign_config.to_dict(), sort_keys=True)))
    
    key_material = {
        "source": "matched_data_v2",
        "since": since.isoformat(),
        "until": until.isoformat(),
        "meta_hash": str(hash(meta_df.to_json())) if not meta_df.empty else "empty",
        "affiliate_id": affiliate_id or "",
        "config_hash": config_hash,
    }
    cache_key = sha256_key(json.dumps(key_material, sort_keys=True, separators=(",", ":")))
    
    cached = cache.get(cache_key, ttl_seconds=ttl_seconds)
    if cached:
        try:
            return pd.read_json(cached, orient="records")
        except Exception:
            pass
    
    # Fetch all Leadspedia data for the affiliate
    all_dispositions: List[LeadDisposition] = []
    
    print(f"[DEBUG] fetch_and_match_data_cached called")
    print(f"[DEBUG] affiliate_id: {affiliate_id}")
    print(f"[DEBUG] date range: {since} to {until}")
    
    if affiliate_id:
        # Fetch by affiliate ID (simpler approach for single affiliate)
        query = LeadQuery(
            since=since,
            until=until,
            affiliate_id=affiliate_id,
        )
        
        # Try fetching all leads first
        try:
            print(f"[DEBUG] Fetching ALL leads with query: {query.to_params()}")
            rows = list(fetch_leads(lp_client, query))
            print(f"[DEBUG] All leads returned: {len(rows)}")
            if rows:
                print(f"[DEBUG] First row sample: {rows[0]}")
            all_dispositions = parse_leads_to_dispositions(rows)
            print(f"[DEBUG] Parsed dispositions from getAll: {len(all_dispositions)}")
            if all_dispositions:
                d = all_dispositions[0]
                print(f"[DEBUG] First disposition parsed: lead_id={d.lead_id}, status={d.status}, revenue={d.revenue}, cost={d.cost}, is_sold={d.is_sold}")
                sold_count = sum(1 for d in all_dispositions if d.is_sold)
                total_revenue = sum(float(d.revenue) for d in all_dispositions)
                print(f"[DEBUG] Summary: {sold_count} sold, total revenue: ${total_revenue:.2f}")
        except Exception as e:
            print(f"[DEBUG] Error fetching all leads: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
        
        # Also try fetching sold leads specifically (may have more revenue data)
        try:
            print(f"[DEBUG] Fetching SOLD leads with query: {query.to_params()}")
            sold_rows = list(fetch_sold_leads(lp_client, query))
            print(f"[DEBUG] Sold leads returned: {len(sold_rows)}")
            if sold_rows:
                print(f"[DEBUG] First sold row sample: {sold_rows[0]}")
                # Parse sold leads and merge/update dispositions
                sold_dispositions = parse_leads_to_dispositions(sold_rows)
                print(f"[DEBUG] Parsed sold dispositions: {len(sold_dispositions)}")
                if sold_dispositions:
                    d = sold_dispositions[0]
                    print(f"[DEBUG] First sold disposition: lead_id={d.lead_id}, status={d.status}, revenue={d.revenue}, is_sold={d.is_sold}")
                    sold_total_revenue = sum(float(d.revenue) for d in sold_dispositions)
                    print(f"[DEBUG] Sold leads total revenue: ${sold_total_revenue:.2f}")
                
                # If we got sold leads but no all leads, use sold leads
                if not all_dispositions and sold_dispositions:
                    all_dispositions = sold_dispositions
                elif sold_dispositions:
                    # Merge sold data - mark these as sold
                    sold_ids = {d.lead_id for d in sold_dispositions}
                    # Update existing dispositions with sold status
                    for disp in all_dispositions:
                        if disp.lead_id in sold_ids:
                            # Find the sold disposition and get revenue
                            for sold_disp in sold_dispositions:
                                if sold_disp.lead_id == disp.lead_id:
                                    # Update with sold data (sold has revenue info)
                                    # Since LeadDisposition is a dataclass, we'll just add sold ones
                                    break
                    # Add any sold leads not in all_dispositions
                    existing_ids = {d.lead_id for d in all_dispositions}
                    for sold_disp in sold_dispositions:
                        if sold_disp.lead_id not in existing_ids:
                            all_dispositions.append(sold_disp)
        except Exception as e:
            print(f"[DEBUG] Error fetching sold leads: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
    
    # Also try legacy campaign map if no dispositions found
    if not all_dispositions and cfg.leadspedia_campaign_map:
        for campaign_id, mapping in cfg.leadspedia_campaign_map.items():
            try:
                dispositions = fetch_leadspedia_data_for_campaign(
                    lp_client, mapping, since, until
                )
                all_dispositions.extend(dispositions)
            except Exception:
                continue
    
    # Match and combine data
    result = match_meta_to_leadspedia(
        meta_df, 
        all_dispositions, 
        cfg,
        campaign_config=campaign_config,
    )
    df = matched_data_to_dataframe(result.matched_data)
    
    # Cache the result
    if not df.empty:
        cache.set(cache_key, df.to_json(orient="records"))
    
    return df

