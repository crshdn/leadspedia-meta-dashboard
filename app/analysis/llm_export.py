"""
LLM-ready export generation for Meta Ads CPL data.

Generates markdown formatted output optimized for pasting into
Claude or ChatGPT for analysis and recommendations.
"""

from __future__ import annotations

from datetime import date
from typing import Optional

import pandas as pd

from app.analysis.confidence import (
    ConfidenceLevel,
    ConfidenceThresholds,
    DEFAULT_THRESHOLDS,
    add_confidence_columns,
)


def _format_currency(value: Optional[float]) -> str:
    """Format a value as currency string."""
    if value is None or pd.isna(value):
        return "N/A"
    return f"${value:,.2f}"


def _format_number(value: Optional[float]) -> str:
    """Format a numeric value."""
    if value is None or pd.isna(value):
        return "N/A"
    if isinstance(value, float):
        return f"{value:,.2f}"
    return f"{value:,}"


def _dataframe_to_markdown_table(df: pd.DataFrame, columns: list[str]) -> str:
    """Convert DataFrame subset to markdown table."""
    if df.empty:
        return "*No data*"
    
    # Filter to requested columns that exist
    available_cols = [c for c in columns if c in df.columns]
    if not available_cols:
        return "*No data*"
    
    subset = df[available_cols].copy()
    
    # Build header
    header = "| " + " | ".join(available_cols) + " |"
    separator = "| " + " | ".join(["---"] * len(available_cols)) + " |"
    
    # Build rows
    rows = []
    for _, row in subset.iterrows():
        values = []
        for col in available_cols:
            val = row[col]
            if col in ["spend", "cpl", "spend_needed"]:
                values.append(_format_currency(val))
            elif col in ["leads", "leads_needed"]:
                values.append(_format_number(val))
            elif col == "progress_pct":
                values.append(f"{val:.0f}%" if val is not None and not pd.isna(val) else "N/A")
            else:
                values.append(str(val) if val is not None and not pd.isna(val) else "N/A")
        rows.append("| " + " | ".join(values) + " |")
    
    return "\n".join([header, separator] + rows)


def generate_llm_export(
    df: pd.DataFrame,
    *,
    date_since: date,
    date_until: date,
    thresholds: ConfidenceThresholds = DEFAULT_THRESHOLDS,
    min_spend_for_ranking: float = 250.0,
    top_n: int = 5,
    bottom_n: int = 5,
    include_full_data: bool = True,
) -> str:
    """
    Generate markdown export optimized for LLM analysis.
    
    Args:
        df: DataFrame with ad performance data (spend, leads, cpl columns required)
        date_since: Start date of the data range
        date_until: End date of the data range
        thresholds: Confidence thresholds to use
        min_spend_for_ranking: Minimum spend to include in top/bottom rankings
        top_n: Number of top performers to highlight
        bottom_n: Number of bottom performers to highlight
        include_full_data: Whether to include the full data table
    
    Returns:
        Markdown string ready for pasting into Claude/ChatGPT
    """
    if df.empty:
        return "## Meta Ads CPL Analysis Data\n\n*No data available for the selected date range.*"
    
    # Add confidence columns if not present
    if "confidence" not in df.columns:
        df = add_confidence_columns(df, thresholds)
    
    # Ensure numeric types
    for col in ["spend", "leads", "cpl"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Calculate summary statistics
    total_spend = df["spend"].sum() if "spend" in df.columns else 0
    total_leads = int(df["leads"].sum()) if "leads" in df.columns else 0
    overall_cpl = total_spend / total_leads if total_leads > 0 else None
    
    # Count by confidence level
    conf_counts = df["confidence"].value_counts().to_dict() if "confidence" in df.columns else {}
    high_conf_count = conf_counts.get(ConfidenceLevel.HIGH, 0)
    medium_conf_count = conf_counts.get(ConfidenceLevel.MEDIUM, 0)
    low_conf_count = conf_counts.get(ConfidenceLevel.LOW, 0)
    
    # Filter for ranking (minimum spend threshold)
    rankable = df[df["spend"] >= min_spend_for_ranking].copy() if "spend" in df.columns else df.copy()
    
    # Sort for top/bottom performers
    if "cpl" in rankable.columns and not rankable.empty:
        # Top performers: lowest CPL (exclude nulls)
        top_performers = (
            rankable[rankable["cpl"].notna()]
            .nsmallest(top_n, "cpl")
        )
        # Bottom performers: highest CPL
        bottom_performers = (
            rankable[rankable["cpl"].notna()]
            .nlargest(bottom_n, "cpl")
        )
    else:
        top_performers = pd.DataFrame()
        bottom_performers = pd.DataFrame()
    
    # Build the markdown document
    sections = []
    
    # Header
    sections.append("## Meta Ads CPL Analysis Data")
    sections.append("")
    
    # Summary
    sections.append(f"**Date Range:** {date_since.isoformat()} to {date_until.isoformat()}")
    sections.append(f"**Total Spend:** {_format_currency(total_spend)}")
    sections.append(f"**Total Leads:** {total_leads:,}")
    sections.append(f"**Overall CPL:** {_format_currency(overall_cpl)}")
    sections.append(f"**Total Ads:** {len(df)}")
    sections.append("")
    
    # Confidence breakdown
    sections.append("### Data Reliability Summary")
    sections.append(f"- 🟢 High confidence (reliable): {high_conf_count} ads")
    sections.append(f"- 🟡 Medium confidence (directional): {medium_conf_count} ads")
    sections.append(f"- 🔴 Low confidence (insufficient data): {low_conf_count} ads")
    sections.append("")
    
    # Top performers
    sections.append(f"### Top {top_n} Performers (by CPL, min ${min_spend_for_ranking:.0f} spend)")
    display_cols = ["ad_name", "campaign_name", "spend", "leads", "cpl", "confidence_emoji", "action_display"]
    # Use available columns
    display_cols = [c for c in display_cols if c in top_performers.columns]
    if not display_cols:
        display_cols = ["ad_name", "spend", "leads", "cpl"]
        display_cols = [c for c in display_cols if c in top_performers.columns]
    sections.append(_dataframe_to_markdown_table(top_performers, display_cols))
    sections.append("")
    
    # Bottom performers
    sections.append(f"### Bottom {bottom_n} Performers (by CPL, min ${min_spend_for_ranking:.0f} spend)")
    sections.append(_dataframe_to_markdown_table(bottom_performers, display_cols))
    sections.append("")
    
    # Full data (collapsible in some contexts)
    if include_full_data:
        sections.append("### Full Data")
        sections.append("<details>")
        sections.append("<summary>Click to expand full data table</summary>")
        sections.append("")
        full_cols = ["ad_name", "campaign_name", "adset_name", "spend", "leads", "cpl", 
                     "confidence_emoji", "action_display", "leads_needed", "spend_needed"]
        full_cols = [c for c in full_cols if c in df.columns]
        # Sort by CPL for the full table
        sorted_df = df.sort_values(by="cpl", ascending=True, na_position="last") if "cpl" in df.columns else df
        sections.append(_dataframe_to_markdown_table(sorted_df, full_cols))
        sections.append("")
        sections.append("</details>")
        sections.append("")
    
    # Analysis prompt
    sections.append("---")
    sections.append("")
    sections.append("## Analysis Request")
    sections.append("")
    sections.append("Please analyze this Meta Ads data and help me identify:")
    sections.append("")
    sections.append("1. **Creative patterns**: What do the top-performing ads have in common?")
    sections.append("   Look at naming conventions that might indicate creative type, hook, or angle.")
    sections.append("")
    sections.append("2. **Statistical concerns**: Which results are statistically reliable vs. noise?")
    sections.append("   Flag any conclusions that need more data to confirm.")
    sections.append("   Reference the confidence indicators (🟢 = reliable, 🟡 = directional, 🔴 = insufficient).")
    sections.append("")
    sections.append("3. **Optimization recommendations**: Based on reliable data only, what should I:")
    sections.append("   - **Scale** (increase budget)")
    sections.append("   - **Kill** (pause immediately)")
    sections.append("   - **Test further** (needs more data before deciding)")
    sections.append("")
    sections.append("4. **Hypotheses to test**: What creative variations should I test next based on patterns you see?")
    sections.append("")
    sections.append("### Important Context")
    sections.append("")
    sections.append(f"- Target CPL: ${thresholds.cpl_target:.0f} or less (up to ${thresholds.cpl_acceptable:.0f} is acceptable)")
    sections.append("- I'm running both Advantage+ and manual targeting campaigns")
    sections.append("- Sample sizes are small (~$250-500 per ad, ~25 leads)")
    sections.append("- **Focus on creative-level insights, not targeting recommendations**")
    sections.append("- Only make recommendations based on 🟢 high-confidence data")
    sections.append("")
    
    return "\n".join(sections)

