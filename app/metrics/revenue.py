"""
Revenue and profitability KPI calculations.

This module provides functions to calculate revenue-related KPIs
from combined Meta Ads and Leadspedia data.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional, Sequence

import pandas as pd


def _safe_decimal(value: Any) -> Decimal:
    """Safely convert a value to Decimal."""
    if value is None:
        return Decimal(0)
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return Decimal(0)


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert a value to float."""
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


@dataclass
class RevenueKPIs:
    """Calculated revenue and profitability KPIs."""
    
    # Core financial metrics
    total_spend: float
    total_revenue: float
    total_payout: float
    net_revenue: float  # revenue - payout
    gross_profit: float  # revenue - spend
    net_profit: float  # net_revenue - spend (if payout is cost to you)
    
    # ROI metrics
    roas: float  # Return on Ad Spend: revenue / spend
    roi_pct: float  # ROI percentage: ((revenue - spend) / spend) * 100
    profit_margin_pct: float  # (gross_profit / revenue) * 100
    
    # Lead metrics
    total_meta_leads: int
    total_lp_leads: int
    sold_leads: int
    rejected_leads: int
    pending_leads: int
    unsold_leads: int  # total - sold
    
    # Rate metrics
    sell_through_rate: float  # (sold / total) * 100
    rejection_rate: float  # (rejected / total) * 100
    conversion_rate: float  # (sold / meta_leads) * 100 (if different)
    
    # Per-unit metrics
    cpl: float  # Cost per lead (Meta spend / leads)
    rpl: float  # Revenue per lead
    ppl: float  # Profit per lead
    avg_sale_price: float  # revenue / sold_leads
    
    # Click efficiency
    epc: float  # Earnings per click
    cpc: float  # Cost per click
    
    # Break-even analysis
    break_even_cpl: float  # Max CPL to break even
    break_even_sell_rate: float  # Min sell rate to break even at current CPL
    
    # Health indicators
    is_profitable: bool
    margin_vs_target: float  # Actual ROI vs target ROI
    sell_rate_vs_target: float  # Actual sell rate vs target

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "total_spend": self.total_spend,
            "total_revenue": self.total_revenue,
            "total_payout": self.total_payout,
            "net_revenue": self.net_revenue,
            "gross_profit": self.gross_profit,
            "net_profit": self.net_profit,
            "roas": self.roas,
            "roi_pct": self.roi_pct,
            "profit_margin_pct": self.profit_margin_pct,
            "total_meta_leads": self.total_meta_leads,
            "total_lp_leads": self.total_lp_leads,
            "sold_leads": self.sold_leads,
            "rejected_leads": self.rejected_leads,
            "pending_leads": self.pending_leads,
            "unsold_leads": self.unsold_leads,
            "sell_through_rate": self.sell_through_rate,
            "rejection_rate": self.rejection_rate,
            "conversion_rate": self.conversion_rate,
            "cpl": self.cpl,
            "rpl": self.rpl,
            "ppl": self.ppl,
            "avg_sale_price": self.avg_sale_price,
            "epc": self.epc,
            "cpc": self.cpc,
            "break_even_cpl": self.break_even_cpl,
            "break_even_sell_rate": self.break_even_sell_rate,
            "is_profitable": self.is_profitable,
            "margin_vs_target": self.margin_vs_target,
            "sell_rate_vs_target": self.sell_rate_vs_target,
        }


def calculate_revenue_kpis(
    df: pd.DataFrame,
    *,
    target_roi: float = 20.0,
    target_sell_rate: float = 95.0,
) -> RevenueKPIs:
    """
    Calculate revenue KPIs from combined Meta + Leadspedia DataFrame.
    
    Expected columns:
    - spend: Ad spend from Meta
    - meta_leads: Lead count from Meta
    - revenue: Total revenue from Leadspedia
    - payout: Total payout/cost from Leadspedia
    - lp_sold_leads: Sold lead count from Leadspedia
    - lp_rejected_leads: Rejected lead count from Leadspedia
    - lp_pending_leads: Pending lead count from Leadspedia
    - lp_total_leads: Total lead count from Leadspedia
    - clicks: Click count from Meta
    
    Args:
        df: Combined data DataFrame
        target_roi: Target ROI percentage for comparison
        target_sell_rate: Target sell-through rate for comparison
        
    Returns:
        RevenueKPIs dataclass with all calculated metrics
    """
    if df.empty:
        return _empty_kpis(target_roi, target_sell_rate)
    
    # Core aggregations
    total_spend = _safe_float(df["spend"].sum()) if "spend" in df.columns else 0.0
    total_revenue = _safe_float(df["revenue"].sum()) if "revenue" in df.columns else 0.0
    total_payout = _safe_float(df["payout"].sum()) if "payout" in df.columns else 0.0
    
    # Lead counts
    total_meta_leads = int(df["meta_leads"].sum()) if "meta_leads" in df.columns else 0
    total_lp_leads = int(df["lp_total_leads"].sum()) if "lp_total_leads" in df.columns else 0
    sold_leads = int(df["lp_sold_leads"].sum()) if "lp_sold_leads" in df.columns else 0
    rejected_leads = int(df["lp_rejected_leads"].sum()) if "lp_rejected_leads" in df.columns else 0
    pending_leads = int(df["lp_pending_leads"].sum()) if "lp_pending_leads" in df.columns else 0
    unsold_leads = total_lp_leads - sold_leads
    
    # Click count
    total_clicks = int(df["clicks"].sum()) if "clicks" in df.columns else 0
    
    # Financial calculations
    net_revenue = total_revenue - total_payout
    gross_profit = total_revenue - total_spend
    net_profit = net_revenue - total_spend
    
    # ROI calculations
    roas = total_revenue / total_spend if total_spend > 0 else 0.0
    roi_pct = ((total_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0.0
    profit_margin_pct = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0.0
    
    # Rate calculations
    sell_through_rate = (sold_leads / total_lp_leads * 100) if total_lp_leads > 0 else 0.0
    rejection_rate = (rejected_leads / total_lp_leads * 100) if total_lp_leads > 0 else 0.0
    conversion_rate = (sold_leads / total_meta_leads * 100) if total_meta_leads > 0 else 0.0
    
    # Per-unit metrics
    cpl = total_spend / total_meta_leads if total_meta_leads > 0 else 0.0
    rpl = total_revenue / total_meta_leads if total_meta_leads > 0 else 0.0
    ppl = gross_profit / total_meta_leads if total_meta_leads > 0 else 0.0
    avg_sale_price = total_revenue / sold_leads if sold_leads > 0 else 0.0
    
    # Click efficiency
    epc = total_revenue / total_clicks if total_clicks > 0 else 0.0
    cpc = total_spend / total_clicks if total_clicks > 0 else 0.0
    
    # Break-even analysis
    # Break-even CPL = avg_sale_price * sell_through_rate
    break_even_cpl = avg_sale_price * (sell_through_rate / 100) if avg_sale_price > 0 else 0.0
    # Break-even sell rate = CPL / avg_sale_price (what sell rate is needed at current CPL)
    break_even_sell_rate = (cpl / avg_sale_price * 100) if avg_sale_price > 0 else 0.0
    
    # Health indicators
    is_profitable = gross_profit > 0
    margin_vs_target = roi_pct - target_roi
    sell_rate_vs_target = sell_through_rate - target_sell_rate
    
    return RevenueKPIs(
        total_spend=round(total_spend, 2),
        total_revenue=round(total_revenue, 2),
        total_payout=round(total_payout, 2),
        net_revenue=round(net_revenue, 2),
        gross_profit=round(gross_profit, 2),
        net_profit=round(net_profit, 2),
        roas=round(roas, 2),
        roi_pct=round(roi_pct, 2),
        profit_margin_pct=round(profit_margin_pct, 2),
        total_meta_leads=total_meta_leads,
        total_lp_leads=total_lp_leads,
        sold_leads=sold_leads,
        rejected_leads=rejected_leads,
        pending_leads=pending_leads,
        unsold_leads=unsold_leads,
        sell_through_rate=round(sell_through_rate, 2),
        rejection_rate=round(rejection_rate, 2),
        conversion_rate=round(conversion_rate, 2),
        cpl=round(cpl, 2),
        rpl=round(rpl, 2),
        ppl=round(ppl, 2),
        avg_sale_price=round(avg_sale_price, 2),
        epc=round(epc, 4),
        cpc=round(cpc, 4),
        break_even_cpl=round(break_even_cpl, 2),
        break_even_sell_rate=round(break_even_sell_rate, 2),
        is_profitable=is_profitable,
        margin_vs_target=round(margin_vs_target, 2),
        sell_rate_vs_target=round(sell_rate_vs_target, 2),
    )


def _empty_kpis(target_roi: float, target_sell_rate: float) -> RevenueKPIs:
    """Return an empty/zero KPIs object."""
    return RevenueKPIs(
        total_spend=0.0,
        total_revenue=0.0,
        total_payout=0.0,
        net_revenue=0.0,
        gross_profit=0.0,
        net_profit=0.0,
        roas=0.0,
        roi_pct=0.0,
        profit_margin_pct=0.0,
        total_meta_leads=0,
        total_lp_leads=0,
        sold_leads=0,
        rejected_leads=0,
        pending_leads=0,
        unsold_leads=0,
        sell_through_rate=0.0,
        rejection_rate=0.0,
        conversion_rate=0.0,
        cpl=0.0,
        rpl=0.0,
        ppl=0.0,
        avg_sale_price=0.0,
        epc=0.0,
        cpc=0.0,
        break_even_cpl=0.0,
        break_even_sell_rate=0.0,
        is_profitable=False,
        margin_vs_target=-target_roi,
        sell_rate_vs_target=-target_sell_rate,
    )


def calculate_kpis_by_dimension(
    df: pd.DataFrame,
    dimension: str,
    *,
    target_roi: float = 20.0,
    target_sell_rate: float = 95.0,
) -> Dict[str, RevenueKPIs]:
    """
    Calculate KPIs grouped by a specific dimension (e.g., campaign, ad set, ad).
    
    Args:
        df: Combined data DataFrame
        dimension: Column name to group by (e.g., 'campaign_name', 'adset_name')
        target_roi: Target ROI percentage
        target_sell_rate: Target sell-through rate
        
    Returns:
        Dictionary mapping dimension values to their KPIs
    """
    if df.empty or dimension not in df.columns:
        return {}
    
    result = {}
    for value in df[dimension].unique():
        subset = df[df[dimension] == value]
        result[str(value)] = calculate_revenue_kpis(
            subset,
            target_roi=target_roi,
            target_sell_rate=target_sell_rate,
        )
    
    return result


def identify_problem_areas(
    df: pd.DataFrame,
    *,
    min_spend: float = 50.0,
    target_roi: float = 20.0,
    target_sell_rate: float = 95.0,
) -> pd.DataFrame:
    """
    Identify ads/campaigns with performance issues.
    
    Returns a DataFrame of problem areas with diagnosis.
    
    Args:
        df: Combined data DataFrame
        min_spend: Minimum spend to consider for analysis
        target_roi: Target ROI percentage
        target_sell_rate: Target sell-through rate
        
    Returns:
        DataFrame with problem areas and diagnosis
    """
    if df.empty:
        return pd.DataFrame()
    
    # Filter to rows with sufficient spend
    analysis_df = df[df["spend"] >= min_spend].copy() if "spend" in df.columns else df.copy()
    
    if analysis_df.empty:
        return pd.DataFrame()
    
    problems = []
    
    for idx, row in analysis_df.iterrows():
        issues = []
        severity = "info"
        
        # Check sell-through rate
        sell_rate = _safe_float(row.get("sell_through_rate", 100))
        if sell_rate < target_sell_rate:
            issues.append(f"Low sell-through: {sell_rate:.1f}% (target: {target_sell_rate}%)")
            severity = "warning" if sell_rate >= target_sell_rate - 10 else "critical"
        
        # Check ROI
        roi = _safe_float(row.get("roi", 0))
        if roi < target_roi:
            issues.append(f"Low ROI: {roi:.1f}% (target: {target_roi}%)")
            if roi < 0:
                severity = "critical"
            elif severity != "critical":
                severity = "warning"
        
        # Check for negative profit
        profit = _safe_float(row.get("profit", 0))
        if profit < 0:
            issues.append(f"Negative profit: ${profit:.2f}")
            severity = "critical"
        
        # Check for high rejection rate
        rejection_rate = _safe_float(row.get("rejection_rate", 0))
        if rejection_rate > 10:  # More than 10% rejection
            issues.append(f"High rejection: {rejection_rate:.1f}%")
            if severity != "critical":
                severity = "warning"
        
        # Check CPL vs break-even
        cpl = _safe_float(row.get("cpl", 0))
        break_even = _safe_float(row.get("break_even_cpl", float("inf")))
        if cpl > break_even and break_even > 0:
            issues.append(f"CPL ${cpl:.2f} exceeds break-even ${break_even:.2f}")
            severity = "critical"
        
        if issues:
            problems.append({
                "campaign_name": row.get("campaign_name", ""),
                "adset_name": row.get("adset_name", ""),
                "ad_name": row.get("ad_name", ""),
                "spend": row.get("spend", 0),
                "revenue": row.get("revenue", 0),
                "profit": profit,
                "roi": roi,
                "sell_through_rate": sell_rate,
                "issues": "; ".join(issues),
                "severity": severity,
            })
    
    if not problems:
        return pd.DataFrame()
    
    result_df = pd.DataFrame(problems)
    # Sort by severity (critical first) then by profit (most negative first)
    severity_order = {"critical": 0, "warning": 1, "info": 2}
    result_df["_severity_order"] = result_df["severity"].map(severity_order)
    result_df = result_df.sort_values(
        by=["_severity_order", "profit"],
        ascending=[True, True]
    ).drop(columns=["_severity_order"])
    
    return result_df


def calculate_period_comparison(
    current_df: pd.DataFrame,
    previous_df: pd.DataFrame,
    *,
    target_roi: float = 20.0,
    target_sell_rate: float = 95.0,
) -> Dict[str, Any]:
    """
    Compare KPIs between two time periods.
    
    Args:
        current_df: Current period data
        previous_df: Previous period data for comparison
        target_roi: Target ROI percentage
        target_sell_rate: Target sell-through rate
        
    Returns:
        Dictionary with current, previous, and change metrics
    """
    current_kpis = calculate_revenue_kpis(
        current_df, target_roi=target_roi, target_sell_rate=target_sell_rate
    )
    previous_kpis = calculate_revenue_kpis(
        previous_df, target_roi=target_roi, target_sell_rate=target_sell_rate
    )
    
    def calc_change(current: float, previous: float) -> Dict[str, float]:
        """Calculate absolute and percentage change."""
        diff = current - previous
        pct_change = (diff / previous * 100) if previous != 0 else 0.0
        return {"current": current, "previous": previous, "change": diff, "change_pct": pct_change}
    
    return {
        "spend": calc_change(current_kpis.total_spend, previous_kpis.total_spend),
        "revenue": calc_change(current_kpis.total_revenue, previous_kpis.total_revenue),
        "profit": calc_change(current_kpis.gross_profit, previous_kpis.gross_profit),
        "roi": calc_change(current_kpis.roi_pct, previous_kpis.roi_pct),
        "sell_through_rate": calc_change(current_kpis.sell_through_rate, previous_kpis.sell_through_rate),
        "cpl": calc_change(current_kpis.cpl, previous_kpis.cpl),
        "avg_sale_price": calc_change(current_kpis.avg_sale_price, previous_kpis.avg_sale_price),
        "leads": calc_change(float(current_kpis.total_meta_leads), float(previous_kpis.total_meta_leads)),
        "sold_leads": calc_change(float(current_kpis.sold_leads), float(previous_kpis.sold_leads)),
    }

