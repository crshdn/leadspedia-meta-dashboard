from __future__ import annotations

import json
import os
import stat
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from dotenv import load_dotenv


def _parse_csv_env(value: str | None) -> list[str]:
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]


def _path_from_env(value: str | None) -> Path | None:
    if not value:
        return None
    return Path(value).expanduser()


def _parse_json_env(value: str | None, default: Any = None) -> Any:
    """Parse a JSON string from environment variable."""
    if not value:
        return default if default is not None else {}
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return default if default is not None else {}


def _parse_bool_env(value: str | None, default: bool = False) -> bool:
    """Parse a boolean from environment variable."""
    if not value:
        return default
    return value.lower() in ("true", "1", "yes", "on")


def check_path_permissions(path: Path) -> tuple[bool, str]:
    """
    Best-effort local safety check:
    - File should be owned by current user
    - Should not be readable/writable/executable by group/other
    """
    try:
        st = path.stat()
    except FileNotFoundError:
        return True, "not_found"

    mode = stat.S_IMODE(st.st_mode)
    group_other_bits = mode & 0o077

    if hasattr(os, "getuid") and st.st_uid != os.getuid():
        return False, f"bad_owner uid={st.st_uid} expected={os.getuid()}"
    if group_other_bits != 0:
        return False, f"too_permissive mode={oct(mode)} expected_like=0o600"
    return True, "ok"


@dataclass(frozen=True)
class CampaignMapping:
    """Maps a Meta campaign to Leadspedia affiliate/vertical configuration."""
    
    meta_campaign_id: str
    affiliate_id: str
    vertical: str
    min_sell_rate: float = 95.0  # Minimum acceptable sell-through rate %
    min_roi: float = 20.0  # Minimum acceptable ROI %
    
    @classmethod
    def from_dict(cls, meta_campaign_id: str, data: Dict[str, Any]) -> "CampaignMapping":
        return cls(
            meta_campaign_id=meta_campaign_id,
            affiliate_id=str(data.get("affiliate_id", "")),
            vertical=str(data.get("vertical", "")),
            min_sell_rate=float(data.get("min_sell_rate", 95.0)),
            min_roi=float(data.get("min_roi", 20.0)),
        )


@dataclass(frozen=True)
class AlertThresholds:
    """Alert threshold configuration."""
    
    min_sell_rate: float = 95.0  # Alert when sell-through rate drops below this %
    min_roi: float = 20.0  # Alert when ROI drops below this %
    max_unsold_time_minutes: int = 30  # Alert if lead unsold after this many minutes
    alert_on_negative_margin: bool = True  # Alert when any lead sells below cost
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AlertThresholds":
        return cls(
            min_sell_rate=float(data.get("min_sell_rate", 95.0)),
            min_roi=float(data.get("min_roi", 20.0)),
            max_unsold_time_minutes=int(data.get("max_unsold_time_minutes", 30)),
            alert_on_negative_margin=bool(data.get("alert_on_negative_margin", True)),
        )


@dataclass(frozen=True)
class AppConfig:
    # Meta Ads API configuration
    meta_api_version: str
    meta_ad_account_id: str
    meta_access_token: str | None
    meta_lead_action_types: Sequence[str]
    
    # Cache configuration
    cache_db_path: Path
    cache_ttl_seconds: int

    # Google Sheets export
    google_sheets_spreadsheet_id: str | None
    google_sheets_worksheet_name: str
    google_service_account_json_path: Path | None
    
    # Leadspedia API configuration
    leadspedia_api_key: str | None
    leadspedia_api_secret: str | None
    leadspedia_base_url: str
    leadspedia_affiliate_id: str | None  # Your affiliate ID in Leadspedia
    leadspedia_campaign_map: Dict[str, CampaignMapping]  # Legacy - use ConfigManager instead
    # Basic Auth credentials (for report endpoints that use Basic Auth instead of HMAC)
    leadspedia_basic_user: str | None
    leadspedia_basic_pass: str | None
    
    # Alert configuration
    alert_thresholds_default: AlertThresholds
    alert_thresholds_by_vertical: Dict[str, AlertThresholds]
    alert_email_enabled: bool
    alert_email_to: str | None
    alert_email_from: str | None
    alert_smtp_host: str | None
    alert_smtp_port: int
    alert_smtp_user: str | None
    alert_smtp_password: str | None
    alert_slack_enabled: bool
    alert_slack_webhook_url: str | None
    alert_check_interval_seconds: int

    @staticmethod
    def load() -> "AppConfig":
        load_dotenv(override=False)

        # Meta Ads API configuration
        meta_api_version = os.getenv("META_API_VERSION", "v24.0").strip()
        meta_ad_account_id = os.getenv("META_AD_ACCOUNT_ID", "").strip()
        meta_access_token = os.getenv("META_ACCESS_TOKEN")
        meta_access_token = meta_access_token.strip() if meta_access_token else None

        meta_lead_action_types = _parse_csv_env(
            os.getenv(
                "META_LEAD_ACTION_TYPES",
                "lead,omni_lead,onsite_conversion.lead_grouped,offsite_conversion.fb_pixel_lead",
            )
        )

        # Cache configuration
        cache_db_path = _path_from_env(os.getenv("META_CACHE_DB_PATH")) or Path(".cache/meta_cache.sqlite")
        cache_ttl_seconds = int(os.getenv("META_CACHE_TTL_SECONDS", "900"))

        # Google Sheets configuration
        google_sheets_spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        google_sheets_spreadsheet_id = (
            google_sheets_spreadsheet_id.strip() if google_sheets_spreadsheet_id else None
        )
        google_sheets_worksheet_name = os.getenv("GOOGLE_SHEETS_WORKSHEET_NAME", "meta_lead_ads").strip()
        google_service_account_json_path = _path_from_env(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON_PATH"))

        # Leadspedia API configuration
        leadspedia_api_key = os.getenv("LEADSPEDIA_API_KEY")
        leadspedia_api_key = leadspedia_api_key.strip() if leadspedia_api_key else None
        leadspedia_api_secret = os.getenv("LEADSPEDIA_API_SECRET")
        leadspedia_api_secret = leadspedia_api_secret.strip() if leadspedia_api_secret else None
        leadspedia_base_url = os.getenv("LEADSPEDIA_BASE_URL", "https://api.leadspedia.com/core/v2/").strip()
        leadspedia_affiliate_id = os.getenv("LEADSPEDIA_AFFILIATE_ID")
        leadspedia_affiliate_id = leadspedia_affiliate_id.strip() if leadspedia_affiliate_id else None

        # Parse campaign mappings (legacy - prefer ConfigManager)
        campaign_map_raw = _parse_json_env(os.getenv("LEADSPEDIA_CAMPAIGN_MAP"), {})
        leadspedia_campaign_map: Dict[str, CampaignMapping] = {}
        for campaign_id, mapping_data in campaign_map_raw.items():
            if isinstance(mapping_data, dict):
                leadspedia_campaign_map[campaign_id] = CampaignMapping.from_dict(campaign_id, mapping_data)

        # Basic Auth credentials for report endpoints
        leadspedia_basic_user = os.getenv("LEADSPEDIA_BASIC_USER")
        leadspedia_basic_user = leadspedia_basic_user.strip() if leadspedia_basic_user else None
        leadspedia_basic_pass = os.getenv("LEADSPEDIA_BASIC_PASS")
        leadspedia_basic_pass = leadspedia_basic_pass.strip() if leadspedia_basic_pass else None

        # Parse alert thresholds
        thresholds_raw = _parse_json_env(os.getenv("ALERT_THRESHOLDS"), {})
        default_thresholds_data = thresholds_raw.get("default", {})
        alert_thresholds_default = AlertThresholds.from_dict(default_thresholds_data)
        
        alert_thresholds_by_vertical: Dict[str, AlertThresholds] = {}
        for vertical, threshold_data in thresholds_raw.items():
            if vertical != "default" and isinstance(threshold_data, dict):
                alert_thresholds_by_vertical[vertical] = AlertThresholds.from_dict(threshold_data)

        # Alert email configuration
        alert_email_enabled = _parse_bool_env(os.getenv("ALERT_EMAIL_ENABLED"), False)
        alert_email_to = os.getenv("ALERT_EMAIL_TO")
        alert_email_to = alert_email_to.strip() if alert_email_to else None
        alert_email_from = os.getenv("ALERT_EMAIL_FROM")
        alert_email_from = alert_email_from.strip() if alert_email_from else None
        alert_smtp_host = os.getenv("ALERT_SMTP_HOST")
        alert_smtp_host = alert_smtp_host.strip() if alert_smtp_host else None
        alert_smtp_port = int(os.getenv("ALERT_SMTP_PORT", "587"))
        alert_smtp_user = os.getenv("ALERT_SMTP_USER")
        alert_smtp_user = alert_smtp_user.strip() if alert_smtp_user else None
        alert_smtp_password = os.getenv("ALERT_SMTP_PASSWORD")
        alert_smtp_password = alert_smtp_password.strip() if alert_smtp_password else None

        # Alert Slack configuration
        alert_slack_enabled = _parse_bool_env(os.getenv("ALERT_SLACK_ENABLED"), False)
        alert_slack_webhook_url = os.getenv("ALERT_SLACK_WEBHOOK_URL")
        alert_slack_webhook_url = alert_slack_webhook_url.strip() if alert_slack_webhook_url else None

        # Alert monitoring interval
        alert_check_interval_seconds = int(os.getenv("ALERT_CHECK_INTERVAL_SECONDS", "300"))

        cfg = AppConfig(
            meta_api_version=meta_api_version,
            meta_ad_account_id=meta_ad_account_id,
            meta_access_token=meta_access_token,
            meta_lead_action_types=meta_lead_action_types,
            cache_db_path=cache_db_path,
            cache_ttl_seconds=cache_ttl_seconds,
            google_sheets_spreadsheet_id=google_sheets_spreadsheet_id,
            google_sheets_worksheet_name=google_sheets_worksheet_name,
            google_service_account_json_path=google_service_account_json_path,
            leadspedia_api_key=leadspedia_api_key,
            leadspedia_api_secret=leadspedia_api_secret,
            leadspedia_base_url=leadspedia_base_url,
            leadspedia_affiliate_id=leadspedia_affiliate_id,
            leadspedia_campaign_map=leadspedia_campaign_map,
            leadspedia_basic_user=leadspedia_basic_user,
            leadspedia_basic_pass=leadspedia_basic_pass,
            alert_thresholds_default=alert_thresholds_default,
            alert_thresholds_by_vertical=alert_thresholds_by_vertical,
            alert_email_enabled=alert_email_enabled,
            alert_email_to=alert_email_to,
            alert_email_from=alert_email_from,
            alert_smtp_host=alert_smtp_host,
            alert_smtp_port=alert_smtp_port,
            alert_smtp_user=alert_smtp_user,
            alert_smtp_password=alert_smtp_password,
            alert_slack_enabled=alert_slack_enabled,
            alert_slack_webhook_url=alert_slack_webhook_url,
            alert_check_interval_seconds=alert_check_interval_seconds,
        )
        cfg._validate()
        return cfg

    def _validate(self) -> None:
        if not self.meta_api_version.startswith("v"):
            raise ValueError("META_API_VERSION must look like v24.0")
        if self.meta_ad_account_id and not self.meta_ad_account_id.startswith("act_"):
            raise ValueError("META_AD_ACCOUNT_ID must look like act_123...")
        if self.cache_ttl_seconds < 0:
            raise ValueError("META_CACHE_TTL_SECONDS must be >= 0")
        if self.alert_check_interval_seconds < 60:
            raise ValueError("ALERT_CHECK_INTERVAL_SECONDS must be >= 60")

    def ensure_local_dirs(self) -> None:
        self.cache_db_path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def leadspedia_enabled(self) -> bool:
        """Check if Leadspedia integration is configured."""
        return bool(self.leadspedia_api_key and self.leadspedia_api_secret)

    @property
    def alerts_enabled(self) -> bool:
        """Check if any alert channel is enabled."""
        return self.alert_email_enabled or self.alert_slack_enabled

    def get_thresholds_for_vertical(self, vertical: str | None) -> AlertThresholds:
        """Get alert thresholds for a specific vertical, falling back to defaults."""
        if vertical and vertical in self.alert_thresholds_by_vertical:
            return self.alert_thresholds_by_vertical[vertical]
        return self.alert_thresholds_default

    def get_campaign_mapping(self, meta_campaign_id: str) -> CampaignMapping | None:
        """Get Leadspedia mapping for a Meta campaign ID."""
        return self.leadspedia_campaign_map.get(meta_campaign_id)


