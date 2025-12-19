from __future__ import annotations

import sys
from dataclasses import asdict
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

# Streamlit runs scripts with the script directory early in sys.path.
# When the script is `app/dashboard.py`, that makes imports like `import app.*`
# fail unless the project root is also on sys.path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.cache.sqlite_cache import SqliteCache
from app.config import AppConfig, check_path_permissions
from app.export.csv_export import dataframe_to_csv_bytes
from app.export.google_sheets import GoogleSheetsConfig, push_dataframe_to_sheet
from app.meta.client import MetaGraphClient, MetaApiError
from app.meta.insights import InsightsQuery, fetch_action_type_summary_cached, fetch_insights_frame_cached
from app.meta.objects import MetaObject, list_ads, list_adsets, list_campaigns
from app.leadspedia.client import LeadspediaClient, LeadspediaApiError
from app.leadspedia.matching import fetch_and_match_data_cached
from app.metrics.revenue import (
    RevenueKPIs,
    calculate_revenue_kpis,
    identify_problem_areas,
)
from app.alerts.monitor import AlertMonitor, Alert, AlertSeverity, AlertType
from app.alerts.channels import create_channels_from_config, DashboardAlertChannel
from app.config_manager import ConfigManager, CampaignConfig, CampaignVerticalMapping
from app.leadspedia.leads import fetch_verticals_cached, LeadspediaVertical


def _maybe_warn_on_dotenv_permissions(dotenv_path: Path) -> None:
    ok, msg = check_path_permissions(dotenv_path)
    if ok:
        return
    st.warning(f"Your `.env` permissions look unsafe ({msg}). Recommended: `chmod 600 .env`.")


def main() -> None:
    st.set_page_config(page_title="Meta Lead Ads Dashboard", layout="wide")
    st.title("Meta Lead Ads Dashboard")
    st.caption("Local reporting dashboard for Lead Ads with revenue tracking via Leadspedia.")

    dotenv_path = Path(".env")
    if dotenv_path.exists():
        _maybe_warn_on_dotenv_permissions(dotenv_path)

    cfg = AppConfig.load()
    cfg.ensure_local_dirs()

    with st.sidebar:
        # Navigation to Analysis page
        st.subheader("Navigation")
        st.markdown("📊 [Go to CPL Analysis](/analysis)")
        st.divider()
        
        st.subheader("Connection")
        st.text_input("Ad Account ID", value=cfg.meta_ad_account_id, disabled=True)

        manual_token = st.text_input(
            "Access Token (optional manual override)",
            value="",
            type="password",
            help="Preferred is META_ACCESS_TOKEN via .env. This field is not persisted.",
        ).strip()

        effective_token = manual_token or (cfg.meta_access_token or "")
        if not effective_token:
            st.error("Missing token. Set META_ACCESS_TOKEN in .env or paste a token above.")

        st.subheader("Date range")
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

        st.subheader("Testing guardrails")
        min_spend = st.number_input("Min spend to judge", min_value=0.0, value=50.0, step=10.0)
        min_leads = st.number_input("Min leads to judge", min_value=0, value=5, step=1)

        st.subheader("Filters")
        st.caption("Load objects to enable campaign/ad set/ad filtering.")
        load_objects = st.button("Load campaigns/ad sets/ads", disabled=not bool(effective_token) or not bool(cfg.meta_ad_account_id))

        st.subheader("Integrations")
        st.subheader("Exports")
        sheets_enabled = bool(cfg.google_sheets_spreadsheet_id and cfg.google_service_account_json_path)
        if not sheets_enabled:
            st.caption("Sheets export: set GOOGLE_SHEETS_SPREADSHEET_ID and GOOGLE_SERVICE_ACCOUNT_JSON_PATH to enable.")

    if not cfg.meta_ad_account_id:
        st.info("Set META_AD_ACCOUNT_ID in `.env` (see `config.example.env.txt`).")
        return

    if not effective_token:
        return

    client = MetaGraphClient(api_version=cfg.meta_api_version, access_token=effective_token)
    cache = SqliteCache(db_path=cfg.cache_db_path)
    
    # Initialize Leadspedia client if configured
    lp_client: Optional[LeadspediaClient] = None
    if cfg.leadspedia_enabled:
        lp_client = LeadspediaClient(
            api_key=cfg.leadspedia_api_key,  # type: ignore
            api_secret=cfg.leadspedia_api_secret,  # type: ignore
            base_url=cfg.leadspedia_base_url,
            basic_user=cfg.leadspedia_basic_user,
            basic_pass=cfg.leadspedia_basic_pass,
        )
    
    # Initialize ConfigManager for campaign mappings
    config_manager = ConfigManager()

    if "campaigns" not in st.session_state:
        st.session_state["campaigns"] = []
        st.session_state["adsets"] = []
        st.session_state["ads"] = []

    if load_objects:
        try:
            st.session_state["campaigns"] = list_campaigns(client, cfg.meta_ad_account_id)
            st.session_state["adsets"] = list_adsets(client, cfg.meta_ad_account_id)
            st.session_state["ads"] = list_ads(client, cfg.meta_ad_account_id)
        except MetaApiError as e:
            st.error(str(e))

    campaigns: list[MetaObject] = st.session_state.get("campaigns", [])
    adsets: list[MetaObject] = st.session_state.get("adsets", [])
    ads: list[MetaObject] = st.session_state.get("ads", [])

    selected_campaign_ids: list[str] = []
    selected_adset_ids: list[str] = []
    selected_ad_ids: list[str] = []

    if campaigns:
        selected_campaign_ids = st.sidebar.multiselect(
            "Campaigns",
            options=[c.id for c in campaigns],
            format_func=lambda cid: next((c.name for c in campaigns if c.id == cid), cid),
        )
    if adsets:
        selected_adset_ids = st.sidebar.multiselect(
            "Ad Sets",
            options=[a.id for a in adsets],
            format_func=lambda aid: next((a.name for a in adsets if a.id == aid), aid),
        )
    if ads:
        selected_ad_ids = st.sidebar.multiselect(
            "Ads",
            options=[a.id for a in ads],
            format_func=lambda aid: next((a.name for a in ads if a.id == aid), aid),
        )

    st.divider()
    st.subheader("Status")

    status = asdict(cfg)
    status["meta_access_token"] = "set" if effective_token else "missing"
    status["cache_db_path"] = str(cfg.cache_db_path)
    status["google_service_account_json_path"] = (
        str(cfg.google_service_account_json_path) if cfg.google_service_account_json_path else None
    )
    st.json(status)

    st.divider()
    st.subheader("Data")

    def run_query(breakdowns: list[str]) -> pd.DataFrame:
        q = InsightsQuery(
            ad_account_id=cfg.meta_ad_account_id,
            since=since,
            until=until,
            level="ad",
            breakdowns=breakdowns,
            campaign_ids=selected_campaign_ids,
            adset_ids=selected_adset_ids,
            ad_ids=selected_ad_ids,
        )
        return fetch_insights_frame_cached(
            client,
            cache,
            q,
            lead_action_types=cfg.meta_lead_action_types,
            ttl_seconds=cfg.cache_ttl_seconds,
        )

    # Initialize alert monitor if alerts are enabled
    alert_monitor: Optional[AlertMonitor] = None
    dashboard_alert_channel: Optional[DashboardAlertChannel] = None
    if cfg.alerts_enabled and cfg.leadspedia_enabled:
        channels = create_channels_from_config(cfg)
        dashboard_alert_channel = next(
            (c for c in channels if isinstance(c, DashboardAlertChannel)), None
        )
        alert_monitor = AlertMonitor(cfg, cache, channels)

    # Create tabs - conditionally add Revenue, Alerts, and Config tabs
    if cfg.leadspedia_enabled:
        if cfg.alerts_enabled:
            tab_revenue, tab_alerts, tab_config, tab_overall, tab_age_gender, tab_placement, tab_device = st.tabs(
                ["Revenue & ROI", "Alerts", "Configuration", "Overall (ad level)", "Age/Gender", "Placement", "Device"]
            )
        else:
            tab_revenue, tab_config, tab_overall, tab_age_gender, tab_placement, tab_device = st.tabs(
                ["Revenue & ROI", "Configuration", "Overall (ad level)", "Age/Gender", "Placement", "Device"]
            )
            tab_alerts = None
    else:
        tab_overall, tab_age_gender, tab_placement, tab_device = st.tabs(
            ["Overall (ad level)", "Age/Gender", "Placement", "Device"]
        )
        tab_revenue = None
        tab_alerts = None
        tab_config = None

    # Configuration tab (if Leadspedia is enabled)
    if cfg.leadspedia_enabled and lp_client is not None:
        if tab_config is not None:
            with tab_config:
                _render_config_tab(
                    lp_client=lp_client,
                    cache=cache,
                    cfg=cfg,
                    config_manager=config_manager,
                    campaigns=campaigns,
                )

    # Revenue & ROI tab (if Leadspedia is enabled)
    if tab_revenue is not None and lp_client is not None:
        with tab_revenue:
            _render_revenue_tab(
                client=client,
                lp_client=lp_client,
                cache=cache,
                cfg=cfg,
                since=since,
                until=until,
                selected_campaign_ids=selected_campaign_ids,
                selected_adset_ids=selected_adset_ids,
                selected_ad_ids=selected_ad_ids,
                min_spend=min_spend,
                alert_monitor=alert_monitor,
                config_manager=config_manager,
            )

    # Alerts tab
    if tab_alerts is not None and alert_monitor is not None:
        with tab_alerts:
            _render_alerts_tab(alert_monitor, dashboard_alert_channel, cache, cfg)

    with tab_overall:
        if st.button("Refresh overall"):
            st.session_state["df_overall"] = run_query([])
        df = st.session_state.get("df_overall", pd.DataFrame())
        _render_results(df, min_spend=min_spend, min_leads=min_leads, cfg=cfg, tab_key="overall")

        with st.expander("Validation / Debug (recommended the first time)"):
            st.caption(
                "Use this to confirm your lead action type mapping matches Ads Manager. "
                "If lead counts don't match, update META_LEAD_ACTION_TYPES."
            )
            q = InsightsQuery(
                ad_account_id=cfg.meta_ad_account_id,
                since=since,
                until=until,
                level="ad",
                breakdowns=[],
                campaign_ids=selected_campaign_ids,
                adset_ids=selected_adset_ids,
                ad_ids=selected_ad_ids,
            )
            if st.button("Show action types seen in this range"):
                try:
                    summary = fetch_action_type_summary_cached(client, cache, q, ttl_seconds=cfg.cache_ttl_seconds)
                    st.dataframe(summary, use_container_width=True)
                except Exception as e:
                    st.error(f"Failed to load action type summary: {e}")

            if df is not None and not df.empty and "spend" in df.columns and "leads" in df.columns:
                spend_sum = float(pd.to_numeric(df["spend"], errors="coerce").fillna(0).sum())
                leads_sum = int(pd.to_numeric(df["leads"], errors="coerce").fillna(0).sum())
                cpl = (spend_sum / leads_sum) if leads_sum > 0 else None

    with tab_age_gender:
        if st.button("Refresh age/gender"):
            st.session_state["df_age_gender"] = run_query(["age", "gender"])
        df = st.session_state.get("df_age_gender", pd.DataFrame())
        _render_results(df, min_spend=min_spend, min_leads=min_leads, cfg=cfg, tab_key="age_gender")

    with tab_placement:
        if st.button("Refresh placement"):
            st.session_state["df_placement"] = run_query(["publisher_platform", "platform_position"])
        df = st.session_state.get("df_placement", pd.DataFrame())
        _render_results(df, min_spend=min_spend, min_leads=min_leads, cfg=cfg, tab_key="placement")

    with tab_device:
        if st.button("Refresh device"):
            st.session_state["df_device"] = run_query(["device_platform"])
        df = st.session_state.get("df_device", pd.DataFrame())
        _render_results(df, min_spend=min_spend, min_leads=min_leads, cfg=cfg, tab_key="device")


def _render_alerts_tab(
    alert_monitor: AlertMonitor,
    dashboard_channel: Optional[DashboardAlertChannel],
    cache: SqliteCache,
    cfg: AppConfig,
) -> None:
    """Render the Alerts tab with alert history and status."""
    
    st.markdown("### Alert Center")
    st.caption("View and manage alerts for campaign performance issues.")
    
    # Alert configuration summary
    with st.expander("Alert Configuration", expanded=False):
        st.markdown("**Current Thresholds (Default)**")
        thresholds = cfg.alert_thresholds_default
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Min Sell Rate", f"{thresholds.min_sell_rate}%")
        with col2:
            st.metric("Min ROI", f"{thresholds.min_roi}%")
        with col3:
            st.metric("Max Unsold Time", f"{thresholds.max_unsold_time_minutes} min")
        
    
    st.divider()
    
    # Get alert history
    alerts = alert_monitor.get_alert_history(limit=100)
    
    if not alerts:
        st.info("No alerts have been triggered yet. Alerts will appear here when performance thresholds are breached.")
        
        # Check for alerts manually
        if st.button("Check for Alerts Now", key="manual_alert_check"):
            # Get revenue data if available
            combined_df = st.session_state.get("df_revenue", pd.DataFrame())
            if combined_df.empty:
                st.warning("No revenue data available. Refresh the Revenue & ROI tab first.")
            else:
                new_alerts = alert_monitor.check_alerts(combined_df)
                if new_alerts:
                    result = alert_monitor.send_alerts(new_alerts)
                    st.success(f"Found and sent {len(new_alerts)} alert(s)")
                    st.rerun()
                else:
                    st.success("No alerts triggered - all metrics within thresholds!")
        return
    
    # Alert statistics
    critical_count = sum(1 for a in alerts if a.severity == AlertSeverity.CRITICAL)
    warning_count = sum(1 for a in alerts if a.severity == AlertSeverity.WARNING)
    unacked_count = sum(1 for a in alerts if not a.acknowledged)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Alerts", len(alerts))
    with col2:
        if critical_count > 0:
            st.metric("Critical", critical_count, delta="Needs attention", delta_color="inverse")
        else:
            st.metric("Critical", 0)
    with col3:
        st.metric("Warnings", warning_count)
    with col4:
        st.metric("Unacknowledged", unacked_count)
    
    st.divider()
    
    # Filter controls
    col1, col2 = st.columns(2)
    with col1:
        severity_filter = st.multiselect(
            "Filter by Severity",
            options=["critical", "warning", "info"],
            default=["critical", "warning"],
            key="alert_severity_filter",
        )
    with col2:
        show_acknowledged = st.checkbox("Show Acknowledged", value=False, key="show_acked")
    
    # Filter alerts
    filtered_alerts = [
        a for a in alerts
        if a.severity.value in severity_filter
        and (show_acknowledged or not a.acknowledged)
    ]
    
    if not filtered_alerts:
        st.info("No alerts match the current filters.")
        return
    
    # Display alerts
    for alert in filtered_alerts:
        _render_alert_card(alert, alert_monitor)


def _render_alert_card(alert: Alert, alert_monitor: AlertMonitor) -> None:
    """Render a single alert card."""
    
    # Determine styling based on severity
    if alert.severity == AlertSeverity.CRITICAL:
        icon = "🔴"
        border_color = "#dc3545"
    elif alert.severity == AlertSeverity.WARNING:
        icon = "🟡"
        border_color = "#ffc107"
    else:
        icon = "🔵"
        border_color = "#17a2b8"
    
    # Use container with custom styling
    with st.container():
        col1, col2, col3 = st.columns([0.7, 0.2, 0.1])
        
        with col1:
            st.markdown(f"**{icon} {alert.title}**")
            st.caption(alert.message)
            
            # Additional info
            info_parts = []
            if alert.campaign_name:
                info_parts.append(f"Campaign: {alert.campaign_name}")
            if alert.ad_name:
                info_parts.append(f"Ad: {alert.ad_name}")
            if alert.metric_value is not None and alert.threshold_value is not None:
                info_parts.append(f"Value: {alert.metric_value:.2f} (threshold: {alert.threshold_value:.2f})")
            
            if info_parts:
                st.caption(" | ".join(info_parts))
        
        with col2:
            st.caption(f"{alert.timestamp.strftime('%Y-%m-%d %H:%M')}")
            if alert.acknowledged:
                st.caption("Acknowledged")
        
        with col3:
            if not alert.acknowledged:
                if st.button("Ack", key=f"ack_{alert.id}"):
                    alert_monitor.acknowledge_alert(alert.id)
                    st.rerun()
        
        st.divider()


def _render_config_tab(
    *,
    lp_client: LeadspediaClient,
    cache: SqliteCache,
    cfg: AppConfig,
    config_manager: ConfigManager,
    campaigns: list,
) -> None:
    """Render the Configuration tab for campaign-to-vertical mappings."""
    
    st.markdown("### Campaign Configuration")
    st.caption("Map your Meta campaigns to Leadspedia verticals for accurate revenue tracking.")
    
    # Load current config
    campaign_config = config_manager.load()
    
    # Affiliate ID section
    st.markdown("#### Affiliate Settings")
    
    current_affiliate = campaign_config.affiliate_id or cfg.leadspedia_affiliate_id or ""
    new_affiliate_id = st.text_input(
        "Your Leadspedia Affiliate ID",
        value=current_affiliate,
        help="Your affiliate ID in Leadspedia (you can find this in your Leadspedia account settings)",
        key="config_affiliate_id",
    )
    
    if new_affiliate_id != current_affiliate:
        if st.button("Save Affiliate ID", key="save_affiliate"):
            config_manager.set_affiliate_id(new_affiliate_id)
            st.success("Affiliate ID saved!")
            st.rerun()
    
    st.divider()
    
    # Fetch verticals from Leadspedia
    st.markdown("#### Leadspedia Verticals")
    
    if st.button("Refresh Verticals from Leadspedia", key="refresh_verticals"):
        st.toast("Fetching verticals...", icon="🔄")
        try:
            result = fetch_verticals_cached(lp_client, cache, ttl_seconds=60)
            st.session_state["lp_verticals"] = result
            if not result:
                st.error("No verticals returned from Leadspedia.")
        except Exception as e:
            st.error(f"Error fetching verticals: {e}")
    
    verticals: list[LeadspediaVertical] = st.session_state.get("lp_verticals", [])
    
    if not verticals:
        st.info("Click 'Refresh Verticals' to load your Leadspedia verticals.")
    else:
        st.success(f"Found {len(verticals)} vertical(s)")
        
        # Show verticals in a table
        vertical_data = [{"ID": v.id, "Name": v.name, "Status": v.status} for v in verticals]
        st.dataframe(vertical_data, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Default vertical setting
    st.markdown("#### Default Settings")
    
    if verticals:
        vertical_options = {v.id: f"{v.name} ({v.id})" for v in verticals}
        vertical_options[""] = "-- No default --"
        
        current_default = campaign_config.default_vertical_id or ""
        new_default = st.selectbox(
            "Default Vertical (for unmapped campaigns)",
            options=[""] + [v.id for v in verticals],
            format_func=lambda x: vertical_options.get(x, x),
            index=0 if not current_default else ([""] + [v.id for v in verticals]).index(current_default) if current_default in [v.id for v in verticals] else 0,
            key="config_default_vertical",
        )
        
        col1, col2 = st.columns(2)
        with col1:
            new_min_sell_rate = st.number_input(
                "Default Min Sell Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=campaign_config.default_min_sell_rate,
                step=5.0,
                key="config_default_sell_rate",
            )
        with col2:
            new_min_roi = st.number_input(
                "Default Min ROI (%)",
                min_value=-100.0,
                max_value=1000.0,
                value=campaign_config.default_min_roi,
                step=5.0,
                key="config_default_roi",
            )
        
        if st.button("Save Default Settings", key="save_defaults"):
            config_manager.set_default_vertical(new_default if new_default else None)
            config_manager.set_default_thresholds(new_min_sell_rate, new_min_roi)
            st.success("Default settings saved!")
            st.rerun()
    
    st.divider()
    
    # Campaign mappings section
    st.markdown("#### Campaign Mappings")
    
    if not campaigns:
        st.warning("No Meta campaigns loaded. Click 'Load campaigns/ad sets/ads' in the sidebar first.")
    elif not verticals:
        st.warning("No Leadspedia verticals loaded. Click 'Refresh Verticals' above first.")
    else:
        # Show existing mappings
        if campaign_config.mappings:
            st.markdown("**Current Mappings:**")
            for mapping in campaign_config.mappings:
                col1, col2, col3 = st.columns([3, 3, 1])
                with col1:
                    st.text(f"{mapping.meta_campaign_name or mapping.meta_campaign_id}")
                with col2:
                    st.text(f"→ {mapping.vertical_name or mapping.vertical_id}")
                with col3:
                    if st.button("Remove", key=f"remove_{mapping.meta_campaign_id}"):
                        config_manager.remove_mapping(mapping.meta_campaign_id)
                        st.rerun()
            st.divider()
        
        # Add new mapping
        st.markdown("**Add New Mapping:**")
        
        # Get unmapped campaigns
        mapped_ids = {m.meta_campaign_id for m in campaign_config.mappings}
        unmapped_campaigns = [c for c in campaigns if c.id not in mapped_ids]
        
        if not unmapped_campaigns:
            st.success("All campaigns are mapped!")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                campaign_options = {c.id: c.name for c in unmapped_campaigns}
                selected_campaign_id = st.selectbox(
                    "Meta Campaign",
                    options=[c.id for c in unmapped_campaigns],
                    format_func=lambda x: campaign_options.get(x, x),
                    key="new_mapping_campaign",
                )
            
            with col2:
                vertical_options = {v.id: v.name for v in verticals}
                selected_vertical_id = st.selectbox(
                    "Leadspedia Vertical",
                    options=[v.id for v in verticals],
                    format_func=lambda x: vertical_options.get(x, x),
                    key="new_mapping_vertical",
                )
            
            if st.button("Add Mapping", key="add_mapping"):
                campaign_name = next((c.name for c in campaigns if c.id == selected_campaign_id), "")
                vertical_name = next((v.name for v in verticals if v.id == selected_vertical_id), "")
                
                config_manager.add_mapping(
                    meta_campaign_id=selected_campaign_id,
                    meta_campaign_name=campaign_name,
                    vertical_id=selected_vertical_id,
                    vertical_name=vertical_name,
                )
                st.success(f"Mapped '{campaign_name}' to '{vertical_name}'")
                st.rerun()
    
    st.divider()
    
    # Show raw config for debugging
    with st.expander("Raw Configuration (Debug)", expanded=False):
        st.json(campaign_config.to_dict())


def _render_revenue_tab(
    *,
    client: MetaGraphClient,
    lp_client: LeadspediaClient,
    cache: SqliteCache,
    cfg: AppConfig,
    since: date,
    until: date,
    selected_campaign_ids: list[str],
    selected_adset_ids: list[str],
    selected_ad_ids: list[str],
    min_spend: float,
    alert_monitor: Optional[AlertMonitor] = None,
    config_manager: Optional[ConfigManager] = None,
) -> None:
    """Render the Revenue & ROI tab with combined Meta + Leadspedia data."""
    
    st.markdown("### Revenue & ROI Analysis")
    st.caption("Combined Meta Ads spend data with Leadspedia revenue data for profitability analysis.")
    
    # Check for configuration
    campaign_config = config_manager.load() if config_manager else None
    has_affiliate = bool(cfg.leadspedia_affiliate_id) or (campaign_config and campaign_config.affiliate_id)
    has_mappings = bool(cfg.leadspedia_campaign_map) or (campaign_config and (campaign_config.mappings or campaign_config.default_vertical_id))
    
    if not has_affiliate and not has_mappings:
        st.warning(
            "No Leadspedia configuration found. Go to the **Configuration** tab to set up your "
            "affiliate ID and campaign-to-vertical mappings."
        )
        return
    
    # Refresh button
    if st.button("Refresh Revenue Data", key="refresh_revenue"):
        # First get Meta data
        q = InsightsQuery(
            ad_account_id=cfg.meta_ad_account_id,
            since=since,
            until=until,
            level="ad",
            breakdowns=[],
            campaign_ids=selected_campaign_ids,
            adset_ids=selected_adset_ids,
            ad_ids=selected_ad_ids,
        )
        meta_df = fetch_insights_frame_cached(
            client, cache, q,
            lead_action_types=cfg.meta_lead_action_types,
            ttl_seconds=cfg.cache_ttl_seconds,
        )
        
        # Add campaign_id to the dataframe if we need to look it up
        # The InsightsQuery should include campaign_id in the response
        
        # Fetch and match with Leadspedia data
        try:
            combined_df = fetch_and_match_data_cached(
                meta_df=meta_df,
                lp_client=lp_client,
                cache=cache,
                cfg=cfg,
                since=since,
                until=until,
                ttl_seconds=cfg.cache_ttl_seconds,
                config_manager=config_manager,
            )
            st.session_state["df_revenue"] = combined_df
            st.session_state["meta_df_for_revenue"] = meta_df
            
            # Check for alerts if monitor is available
            if alert_monitor is not None:
                alerts = alert_monitor.check_alerts(combined_df)
                if alerts:
                    alert_monitor.send_alerts(alerts)
                    st.toast(f"{len(alerts)} alert(s) triggered", icon="⚠️")
                    
        except LeadspediaApiError as e:
            st.error(f"Leadspedia API error: {e}")
            return
        except Exception as e:
            st.error(f"Error fetching revenue data: {e}")
            return
    
    # Get cached data
    combined_df = st.session_state.get("df_revenue", pd.DataFrame())
    
    if combined_df.empty:
        st.info("Click 'Refresh Revenue Data' to load combined metrics.")
        return
    
    # Calculate overall KPIs
    thresholds = cfg.alert_thresholds_default
    kpis = calculate_revenue_kpis(
        combined_df,
        target_roi=thresholds.min_roi,
        target_sell_rate=thresholds.min_sell_rate,
    )
    
    # Display KPI summary cards
    _render_kpi_cards(kpis)
    
    st.divider()
    
    # Tabs for different views within revenue
    rev_tab1, rev_tab2, rev_tab3 = st.tabs(["Detailed Data", "Problem Areas", "Performance Summary"])
    
    with rev_tab1:
        st.markdown("#### Combined Performance Data")
        
        # Column selection for display
        display_cols = [
            "campaign_name", "adset_name", "ad_name",
            "spend", "meta_leads", "revenue", "profit", "roi",
            "sell_through_rate", "avg_sale_price", "cpl", "break_even_cpl",
        ]
        available_cols = [c for c in display_cols if c in combined_df.columns]
        
        # Format numeric columns for display
        display_df = combined_df[available_cols].copy()
        
        st.dataframe(
            display_df.sort_values(by=["profit"], ascending=False),
            use_container_width=True,
        )
        
        # Download button
        st.download_button(
            label="Download Combined Data CSV",
            data=dataframe_to_csv_bytes(combined_df),
            file_name="meta_leadspedia_combined_report.csv",
            mime="text/csv",
            key="download_revenue_csv",
        )
    
    with rev_tab2:
        st.markdown("#### Problem Areas")
        st.caption("Ads/campaigns that need attention based on configured thresholds.")
        
        problems_df = identify_problem_areas(
            combined_df,
            min_spend=min_spend,
            target_roi=thresholds.min_roi,
            target_sell_rate=thresholds.min_sell_rate,
        )
        
        if problems_df.empty:
            st.success("No problem areas identified! All metrics are within targets.")
        else:
            # Show critical issues first
            critical = problems_df[problems_df["severity"] == "critical"]
            if not critical.empty:
                st.error(f"**{len(critical)} Critical Issues Found**")
                st.dataframe(critical, use_container_width=True)
            
            # Show warnings
            warnings = problems_df[problems_df["severity"] == "warning"]
            if not warnings.empty:
                st.warning(f"**{len(warnings)} Warnings**")
                st.dataframe(warnings, use_container_width=True)
    
    with rev_tab3:
        st.markdown("#### Performance Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Financial Health**")
            if kpis.is_profitable:
                st.success(f"Overall Profitable: ${kpis.gross_profit:,.2f} profit")
            else:
                st.error(f"Overall Loss: ${kpis.gross_profit:,.2f}")
            
            st.metric(
                "ROI vs Target",
                f"{kpis.roi_pct:.1f}%",
                delta=f"{kpis.margin_vs_target:.1f}%",
                delta_color="normal" if kpis.margin_vs_target >= 0 else "inverse",
            )
            
            st.metric(
                "ROAS",
                f"{kpis.roas:.2f}x",
                help="Return on Ad Spend (Revenue / Spend)",
            )
        
        with col2:
            st.markdown("**Lead Performance**")
            st.metric(
                "Sell-Through Rate",
                f"{kpis.sell_through_rate:.1f}%",
                delta=f"{kpis.sell_rate_vs_target:.1f}%",
                delta_color="normal" if kpis.sell_rate_vs_target >= 0 else "inverse",
            )
            
            st.metric(
                "Unsold Leads",
                f"{kpis.unsold_leads:,}",
                delta_color="inverse" if kpis.unsold_leads > 0 else "off",
            )
            
            st.metric(
                "Break-Even CPL",
                f"${kpis.break_even_cpl:.2f}",
                help="Maximum CPL to break even at current sell rate and price",
            )
        
        # Show efficiency metrics
        st.markdown("**Efficiency Metrics**")
        eff_col1, eff_col2, eff_col3, eff_col4 = st.columns(4)
        with eff_col1:
            st.metric("CPL (Actual)", f"${kpis.cpl:.2f}")
        with eff_col2:
            st.metric("Avg Sale Price", f"${kpis.avg_sale_price:.2f}")
        with eff_col3:
            st.metric("Profit/Lead", f"${kpis.ppl:.2f}")
        with eff_col4:
            st.metric("EPC", f"${kpis.epc:.4f}")


def _render_kpi_cards(kpis: RevenueKPIs) -> None:
    """Render KPI summary cards at the top of the revenue tab."""
    
    # First row: Financial KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Spend",
            f"${kpis.total_spend:,.2f}",
        )
    
    with col2:
        st.metric(
            "Total Revenue",
            f"${kpis.total_revenue:,.2f}",
        )
    
    with col3:
        delta_color = "normal" if kpis.gross_profit >= 0 else "inverse"
        st.metric(
            "Profit",
            f"${kpis.gross_profit:,.2f}",
            delta=f"{kpis.roi_pct:.1f}% ROI",
            delta_color=delta_color,
        )
    
    with col4:
        st.metric(
            "Leads (Meta)",
            f"{kpis.total_meta_leads:,}",
        )
    
    with col5:
        st.metric(
            "Sold Leads",
            f"{kpis.sold_leads:,}",
            delta=f"{kpis.sell_through_rate:.1f}% sell rate",
        )


def _apply_filters(df: pd.DataFrame, tab_key: str) -> pd.DataFrame:
    """Render filter controls in an expander and return filtered dataframe."""
    if df is None or df.empty:
        return df

    # Identify column types
    text_cols = [c for c in df.columns if df[c].dtype == "object" or str(df[c].dtype) == "string"]
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    filtered_df = df.copy()

    with st.expander("🔍 Filter options", expanded=False):
        # Text column filters (multiselect)
        if text_cols:
            st.markdown("**Filter by name/category**")
            num_filter_cols = min(len(text_cols), 3)
            cols = st.columns(num_filter_cols)
            for i, col in enumerate(text_cols):
                with cols[i % num_filter_cols]:
                    unique_vals = sorted([str(v) for v in df[col].dropna().unique().tolist()])
                    selected = st.multiselect(
                        col.replace("_", " ").title(),
                        options=unique_vals,
                        default=[],
                        key=f"filter_{tab_key}_{col}",
                    )
                    if selected:
                        filtered_df = filtered_df[filtered_df[col].astype(str).isin(selected)]

        # Numeric column filters (min/max ranges)
        if numeric_cols:
            st.markdown("**Filter by numeric range**")
            # Group numeric columns into rows of 2 (min/max pairs side by side)
            for col in numeric_cols:
                col_min = df[col].min()
                col_max = df[col].max()
                if pd.isna(col_min) or pd.isna(col_max):
                    continue

                col_label = col.replace("_", " ").title()
                # Use smaller steps for ratio/rate columns
                step = 0.01 if col in ["cpl", "ctr", "cpc", "frequency"] else 1.0

                c1, c2 = st.columns(2)
                with c1:
                    user_min = st.number_input(
                        f"{col_label} ≥",
                        value=float(col_min),
                        min_value=float(col_min),
                        max_value=float(col_max),
                        step=step,
                        key=f"filter_{tab_key}_{col}_min",
                    )
                with c2:
                    user_max = st.number_input(
                        f"{col_label} ≤",
                        value=float(col_max),
                        min_value=float(col_min),
                        max_value=float(col_max),
                        step=step,
                        key=f"filter_{tab_key}_{col}_max",
                    )

                filtered_df = filtered_df[
                    (filtered_df[col].fillna(0) >= user_min) & (filtered_df[col].fillna(0) <= user_max)
                ]

        # Show filter summary
        if len(filtered_df) != len(df):
            st.caption(f"Showing {len(filtered_df)} of {len(df)} rows")

    return filtered_df


def _render_results(df: pd.DataFrame, *, min_spend: float, min_leads: int, cfg: AppConfig, tab_key: str) -> None:
    if df is None or df.empty:
        st.info("No rows (yet). Click Refresh.")
        return

    # Normalize numeric columns for sorting and display
    for col in ["spend", "impressions", "clicks", "reach", "frequency", "ctr", "cpc", "cpl", "leads"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Apply user filters
    filtered_df = _apply_filters(df, tab_key)

    st.dataframe(filtered_df.sort_values(by=["cpl", "spend"], ascending=[True, False]), use_container_width=True)

    st.download_button(
        label="Download CSV (filtered)",
        data=dataframe_to_csv_bytes(filtered_df),
        file_name="meta_lead_ads_report.csv",
        mime="text/csv",
        use_container_width=False,
        key=f"download_csv_{tab_key}",
    )

    if cfg.google_sheets_spreadsheet_id and cfg.google_service_account_json_path:
        if st.button("Push to Google Sheets (filtered)", key=f"push_sheets_{tab_key}"):
            ok, msg = check_path_permissions(cfg.google_service_account_json_path)
            if not ok:
                st.error(
                    f"Service account JSON permissions look unsafe ({msg}). Recommended: chmod 600 {cfg.google_service_account_json_path}"
                )
            else:
                try:
                    push_dataframe_to_sheet(
                        filtered_df,
                        GoogleSheetsConfig(
                            spreadsheet_id=cfg.google_sheets_spreadsheet_id,
                            worksheet_name=cfg.google_sheets_worksheet_name,
                            service_account_json_path=cfg.google_service_account_json_path,
                        ),
                    )
                    st.success("Pushed to Google Sheets.")
                except Exception as e:
                    st.error(f"Sheets export failed: {e}")

    if "cpl" in filtered_df.columns and "spend" in filtered_df.columns and "leads" in filtered_df.columns:
        judged = filtered_df[(filtered_df["spend"].fillna(0) >= float(min_spend)) & (filtered_df["leads"].fillna(0) >= int(min_leads))].copy()
        if not judged.empty:
            st.subheader("Winners / Losers (guardrail view)")
            st.caption("This is a quick triage tool; verify with judgment and business context.")
            st.dataframe(judged.sort_values(by=["cpl", "spend"], ascending=[True, False]), use_container_width=True)


if __name__ == "__main__":
    main()


