"""
CPL Analysis Page - Creative Performance Ranker, Statistical Significance, and LLM Export.

This page provides tools for analyzing Meta Ads CPL data with statistical rigor
and generating AI-ready exports for Claude/ChatGPT analysis.
"""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

# Ensure project root is in path for imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.analysis.confidence import (
    ActionRecommendation,
    ConfidenceLevel,
    ConfidenceThresholds,
    add_confidence_columns,
)
from app.analysis.llm_export import generate_llm_export
from app.cache.sqlite_cache import SqliteCache
from app.config import AppConfig, check_path_permissions
from app.meta.client import MetaApiError, MetaGraphClient
from app.meta.insights import InsightsQuery, fetch_insights_frame_cached
from app.meta.objects import MetaObject, list_ads, list_adsets, list_campaigns


def _render_confidence_badge(confidence: ConfidenceLevel) -> str:
    """Return HTML badge for confidence level."""
    colors = {
        ConfidenceLevel.HIGH: ("#22c55e", "#dcfce7"),  # green
        ConfidenceLevel.MEDIUM: ("#eab308", "#fef9c3"),  # yellow
        ConfidenceLevel.LOW: ("#ef4444", "#fee2e2"),  # red
    }
    fg, bg = colors.get(confidence, ("#6b7280", "#f3f4f6"))
    label = confidence.value.upper()
    return f'<span style="background:{bg};color:{fg};padding:2px 8px;border-radius:4px;font-weight:600;font-size:12px;">{label}</span>'


def _render_action_badge(action: ActionRecommendation) -> str:
    """Return HTML badge for action recommendation."""
    colors = {
        ActionRecommendation.SCALE: ("#22c55e", "#dcfce7"),
        ActionRecommendation.MAINTAIN: ("#3b82f6", "#dbeafe"),
        ActionRecommendation.KILL: ("#ef4444", "#fee2e2"),
        ActionRecommendation.NEEDS_DATA: ("#6b7280", "#f3f4f6"),
    }
    labels = {
        ActionRecommendation.SCALE: "SCALE ↑",
        ActionRecommendation.MAINTAIN: "MAINTAIN →",
        ActionRecommendation.KILL: "KILL ✕",
        ActionRecommendation.NEEDS_DATA: "NEEDS DATA",
    }
    fg, bg = colors.get(action, ("#6b7280", "#f3f4f6"))
    label = labels.get(action, "UNKNOWN")
    return f'<span style="background:{bg};color:{fg};padding:2px 8px;border-radius:4px;font-weight:600;font-size:12px;">{label}</span>'


def main() -> None:
    st.set_page_config(
        page_title="CPL Analysis | Meta Ads Dashboard",
        page_icon="📊",
        layout="wide",
    )
    
    st.title("📊 CPL Analysis")
    st.caption("Creative performance ranking with statistical confidence and AI-ready exports.")
    
    # Load config
    dotenv_path = Path(".env")
    if dotenv_path.exists():
        ok, msg = check_path_permissions(dotenv_path)
        if not ok:
            st.warning(f"Your `.env` permissions look unsafe ({msg}). Recommended: `chmod 600 .env`.")
    
    cfg = AppConfig.load()
    cfg.ensure_local_dirs()
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Connection
        st.subheader("Connection")
        st.text_input("Ad Account ID", value=cfg.meta_ad_account_id, disabled=True)
        
        manual_token = st.text_input(
            "Access Token (optional override)",
            value="",
            type="password",
            help="Uses META_ACCESS_TOKEN from .env by default.",
        ).strip()
        
        effective_token = manual_token or (cfg.meta_access_token or "")
        if not effective_token:
            st.error("Missing token. Set META_ACCESS_TOKEN in .env or paste a token above.")
        
        # Date range
        st.subheader("Date Range")
        preset = st.selectbox("Preset", ["Last 7 days", "Last 14 days", "Last 30 days", "Custom"])
        today = date.today()
        if preset == "Last 7 days":
            since, until = today - timedelta(days=7), today
        elif preset == "Last 14 days":
            since, until = today - timedelta(days=14), today
        elif preset == "Last 30 days":
            since, until = today - timedelta(days=30), today
        else:
            since = st.date_input("Since", value=today - timedelta(days=7))
            until = st.date_input("Until", value=today)
        
        # CPL thresholds
        st.subheader("CPL Thresholds")
        cpl_target = st.number_input(
            "Target CPL ($)",
            min_value=1.0,
            value=30.0,
            step=5.0,
            help="CPL at or below this = SCALE recommendation",
        )
        cpl_acceptable = st.number_input(
            "Acceptable CPL ($)",
            min_value=1.0,
            value=45.0,
            step=5.0,
            help="CPL between target and this = MAINTAIN recommendation",
        )
        
        # Confidence thresholds
        st.subheader("Confidence Thresholds")
        high_spend = st.number_input(
            "High confidence: min spend ($)",
            min_value=100.0,
            value=500.0,
            step=50.0,
        )
        high_leads = st.number_input(
            "High confidence: min leads",
            min_value=10,
            value=30,
            step=5,
        )
        medium_spend = st.number_input(
            "Medium confidence: min spend ($)",
            min_value=50.0,
            value=250.0,
            step=50.0,
        )
        medium_leads = st.number_input(
            "Medium confidence: min leads",
            min_value=5,
            value=15,
            step=5,
        )
        
        # Filter options
        st.subheader("Filters")
        confidence_filter = st.selectbox(
            "Show confidence levels",
            ["All", "High only", "Medium and above"],
        )
        
        # Load campaigns/adsets/ads
        st.caption("Load objects to filter by campaign/ad set/ad.")
        load_objects = st.button(
            "Load campaigns/ad sets/ads",
            disabled=not bool(effective_token) or not bool(cfg.meta_ad_account_id),
        )
        
        # Navigation
        st.divider()
        st.subheader("Navigation")
        st.markdown("🏠 [← Back to Dashboard](/)")
    
    # Validation
    if not cfg.meta_ad_account_id:
        st.info("Set META_AD_ACCOUNT_ID in `.env` to get started.")
        return
    
    if not effective_token:
        return
    
    # Initialize client and cache
    client = MetaGraphClient(api_version=cfg.meta_api_version, access_token=effective_token)
    cache = SqliteCache(db_path=cfg.cache_db_path)
    
    # Session state for objects
    if "analysis_campaigns" not in st.session_state:
        st.session_state["analysis_campaigns"] = []
        st.session_state["analysis_adsets"] = []
        st.session_state["analysis_ads"] = []
    
    if load_objects:
        try:
            with st.spinner("Loading campaigns, ad sets, and ads..."):
                st.session_state["analysis_campaigns"] = list_campaigns(client, cfg.meta_ad_account_id)
                st.session_state["analysis_adsets"] = list_adsets(client, cfg.meta_ad_account_id)
                st.session_state["analysis_ads"] = list_ads(client, cfg.meta_ad_account_id)
            st.success("Loaded objects successfully!")
        except MetaApiError as e:
            st.error(f"Failed to load objects: {e}")
    
    campaigns: list[MetaObject] = st.session_state.get("analysis_campaigns", [])
    adsets: list[MetaObject] = st.session_state.get("analysis_adsets", [])
    ads: list[MetaObject] = st.session_state.get("analysis_ads", [])
    
    # Object filters in sidebar
    selected_campaign_ids: list[str] = []
    selected_adset_ids: list[str] = []
    selected_ad_ids: list[str] = []
    
    if campaigns:
        selected_campaign_ids = st.sidebar.multiselect(
            "Filter by Campaign",
            options=[c.id for c in campaigns],
            format_func=lambda cid: next((c.name for c in campaigns if c.id == cid), cid),
        )
    if adsets:
        selected_adset_ids = st.sidebar.multiselect(
            "Filter by Ad Set",
            options=[a.id for a in adsets],
            format_func=lambda aid: next((a.name for a in adsets if a.id == aid), aid),
        )
    if ads:
        selected_ad_ids = st.sidebar.multiselect(
            "Filter by Ad",
            options=[a.id for a in ads],
            format_func=lambda aid: next((a.name for a in ads if a.id == aid), aid),
        )
    
    # Build thresholds object
    thresholds = ConfidenceThresholds(
        high_spend=high_spend,
        high_leads=high_leads,
        medium_spend=medium_spend,
        medium_leads=medium_leads,
        cpl_target=cpl_target,
        cpl_acceptable=cpl_acceptable,
    )
    
    # Main content
    st.divider()
    
    # Load data button
    col1, col2 = st.columns([1, 4])
    with col1:
        refresh_data = st.button("🔄 Load/Refresh Data", type="primary")
    
    if refresh_data or "analysis_df" in st.session_state:
        if refresh_data:
            with st.spinner("Fetching data from Meta API..."):
                try:
                    query = InsightsQuery(
                        ad_account_id=cfg.meta_ad_account_id,
                        since=since,
                        until=until,
                        level="ad",
                        breakdowns=[],
                        campaign_ids=selected_campaign_ids,
                        adset_ids=selected_adset_ids,
                        ad_ids=selected_ad_ids,
                    )
                    df = fetch_insights_frame_cached(
                        client,
                        cache,
                        query,
                        lead_action_types=cfg.meta_lead_action_types,
                        ttl_seconds=cfg.cache_ttl_seconds,
                    )
                    st.session_state["analysis_df"] = df
                    st.session_state["analysis_since"] = since
                    st.session_state["analysis_until"] = until
                except MetaApiError as e:
                    st.error(f"API Error: {e}")
                    return
        
        df = st.session_state.get("analysis_df", pd.DataFrame())
        date_since = st.session_state.get("analysis_since", since)
        date_until = st.session_state.get("analysis_until", until)
        
        if df.empty:
            st.info("No data returned for the selected filters and date range.")
            return
        
        # Add confidence columns
        df_with_confidence = add_confidence_columns(df, thresholds)
        
        # Apply confidence filter
        if confidence_filter == "High only":
            df_filtered = df_with_confidence[df_with_confidence["confidence"] == ConfidenceLevel.HIGH]
        elif confidence_filter == "Medium and above":
            df_filtered = df_with_confidence[df_with_confidence["confidence"].isin([ConfidenceLevel.HIGH, ConfidenceLevel.MEDIUM])]
        else:
            df_filtered = df_with_confidence
        
        # Summary metrics
        st.subheader("Summary")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        total_spend = df_filtered["spend"].sum() if "spend" in df_filtered.columns else 0
        total_leads = int(df_filtered["leads"].sum()) if "leads" in df_filtered.columns else 0
        overall_cpl = total_spend / total_leads if total_leads > 0 else None
        
        with col1:
            st.metric("Total Spend", f"${total_spend:,.2f}")
        with col2:
            st.metric("Total Leads", f"{total_leads:,}")
        with col3:
            st.metric("Overall CPL", f"${overall_cpl:.2f}" if overall_cpl else "N/A")
        with col4:
            st.metric("Total Ads", len(df_filtered))
        with col5:
            high_conf_count = len(df_filtered[df_filtered["confidence"] == ConfidenceLevel.HIGH])
            st.metric("High Confidence Ads", high_conf_count)
        
        st.divider()
        
        # ============================================
        # SECTION 1: Creative Performance Ranker
        # ============================================
        st.subheader("🏆 Creative Performance Ranker")
        st.caption("Ads ranked by CPL with confidence indicators and action recommendations.")
        
        # Prepare display dataframe
        display_cols = [
            "confidence_emoji",
            "ad_name",
            "campaign_name",
            "spend",
            "leads",
            "cpl",
            "action_display",
        ]
        display_cols = [c for c in display_cols if c in df_filtered.columns]
        
        # Sort by action priority then CPL
        action_order = {
            ActionRecommendation.SCALE: 0,
            ActionRecommendation.MAINTAIN: 1,
            ActionRecommendation.KILL: 2,
            ActionRecommendation.NEEDS_DATA: 3,
        }
        df_sorted = df_filtered.copy()
        df_sorted["_action_order"] = df_sorted["action"].map(action_order)
        df_sorted = df_sorted.sort_values(
            by=["_action_order", "cpl", "spend"],
            ascending=[True, True, False],
            na_position="last",
        )
        
        # Format for display
        df_display = df_sorted[display_cols].copy()
        df_display = df_display.rename(columns={
            "confidence_emoji": "Conf",
            "ad_name": "Ad Name",
            "campaign_name": "Campaign",
            "spend": "Spend",
            "leads": "Leads",
            "cpl": "CPL",
            "action_display": "Action",
        })
        
        # Format numeric columns
        if "Spend" in df_display.columns:
            df_display["Spend"] = df_display["Spend"].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "N/A")
        if "CPL" in df_display.columns:
            df_display["CPL"] = df_display["CPL"].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "N/A")
        if "Leads" in df_display.columns:
            df_display["Leads"] = df_display["Leads"].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "0")
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Action summary
        st.markdown("**Quick Summary:**")
        action_counts = df_sorted["action"].value_counts()
        cols = st.columns(4)
        with cols[0]:
            scale_count = action_counts.get(ActionRecommendation.SCALE, 0)
            st.success(f"🟢 **SCALE:** {scale_count} ads")
        with cols[1]:
            maintain_count = action_counts.get(ActionRecommendation.MAINTAIN, 0)
            st.info(f"🔵 **MAINTAIN:** {maintain_count} ads")
        with cols[2]:
            kill_count = action_counts.get(ActionRecommendation.KILL, 0)
            st.error(f"🔴 **KILL:** {kill_count} ads")
        with cols[3]:
            needs_count = action_counts.get(ActionRecommendation.NEEDS_DATA, 0)
            st.warning(f"⚪ **NEEDS DATA:** {needs_count} ads")
        
        st.divider()
        
        # ============================================
        # SECTION 2: Statistical Significance
        # ============================================
        st.subheader("📈 Statistical Significance")
        
        with st.expander("View data requirements for reliable decisions", expanded=False):
            st.caption(
                "Each ad needs ~50 leads for 95% confidence that the true CPL is within ±20% of observed CPL. "
                "Below shows progress toward statistical significance."
            )
            
            # Filter to ads that need more data
            needs_data_df = df_sorted[df_sorted["action"] == ActionRecommendation.NEEDS_DATA].copy()
            
            if needs_data_df.empty:
                st.success("All ads have sufficient data for reliable decisions!")
            else:
                for _, row in needs_data_df.iterrows():
                    ad_name = row.get("ad_name", "Unknown")
                    leads_needed = int(row.get("leads_needed", 0))
                    spend_needed = row.get("spend_needed")
                    progress = row.get("progress_pct", 0)
                    current_leads = int(row.get("leads", 0))
                    
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        st.markdown(f"**{ad_name}**")
                        st.caption(f"Current: {current_leads} leads")
                    with col2:
                        st.progress(min(progress / 100, 1.0))
                        if spend_needed is not None and spend_needed > 0:
                            st.caption(f"Need ~{leads_needed} more leads (~${spend_needed:,.0f} more spend)")
                        else:
                            st.caption(f"Need ~{leads_needed} more leads")
        
        st.divider()
        
        # ============================================
        # SECTION 3: LLM Export
        # ============================================
        st.subheader("🤖 LLM Analysis Export")
        st.caption("Generate a formatted export optimized for Claude or ChatGPT analysis.")
        
        col1, col2 = st.columns(2)
        with col1:
            min_spend_export = st.number_input(
                "Min spend for top/bottom ranking ($)",
                min_value=0.0,
                value=250.0,
                step=50.0,
                key="export_min_spend",
            )
        with col2:
            top_n = st.number_input(
                "Number of top/bottom performers",
                min_value=3,
                max_value=20,
                value=5,
                step=1,
                key="export_top_n",
            )
        
        # Generate export
        export_md = generate_llm_export(
            df_with_confidence,
            date_since=date_since,
            date_until=date_until,
            thresholds=thresholds,
            min_spend_for_ranking=min_spend_export,
            top_n=top_n,
            bottom_n=top_n,
            include_full_data=True,
        )
        
        # Copy button and preview
        col1, col2 = st.columns([1, 1])
        with col1:
            st.download_button(
                label="📥 Download as Markdown",
                data=export_md,
                file_name="meta_ads_analysis.md",
                mime="text/markdown",
            )
        with col2:
            if st.button("📋 Copy to Clipboard"):
                st.code(export_md, language="markdown")
                st.info("Select all the text above (Cmd+A / Ctrl+A) and copy (Cmd+C / Ctrl+C)")
        
        with st.expander("Preview LLM Export", expanded=False):
            st.markdown(export_md, unsafe_allow_html=True)
    
    else:
        st.info("Click **Load/Refresh Data** to fetch ad performance data and begin analysis.")


if __name__ == "__main__":
    main()

