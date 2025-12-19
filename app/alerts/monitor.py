"""
Alert monitoring service.

This module provides background monitoring of campaign performance
and triggers alerts when thresholds are breached.
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

import pandas as pd

from app.cache.sqlite_cache import SqliteCache, sha256_key
from app.config import AppConfig, AlertThresholds


class AlertSeverity(str, Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertType(str, Enum):
    """Types of alerts that can be triggered."""
    UNSOLD_LEAD = "unsold_lead"
    NEGATIVE_MARGIN = "negative_margin"
    LOW_SELL_RATE = "low_sell_rate"
    LOW_ROI = "low_roi"
    HIGH_REJECTION = "high_rejection"
    REVENUE_DROP = "revenue_drop"
    SYSTEM_ERROR = "system_error"


@dataclass
class Alert:
    """Represents a single alert."""
    
    id: str
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    message: str
    timestamp: datetime
    campaign_id: Optional[str] = None
    campaign_name: Optional[str] = None
    ad_id: Optional[str] = None
    ad_name: Optional[str] = None
    vertical: Optional[str] = None
    metric_value: Optional[float] = None
    threshold_value: Optional[float] = None
    acknowledged: bool = False
    acknowledged_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "alert_type": self.alert_type.value,
            "severity": self.severity.value,
            "title": self.title,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "campaign_id": self.campaign_id,
            "campaign_name": self.campaign_name,
            "ad_id": self.ad_id,
            "ad_name": self.ad_name,
            "vertical": self.vertical,
            "metric_value": self.metric_value,
            "threshold_value": self.threshold_value,
            "acknowledged": self.acknowledged,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Alert":
        """Create an Alert from a dictionary."""
        return cls(
            id=data["id"],
            alert_type=AlertType(data["alert_type"]),
            severity=AlertSeverity(data["severity"]),
            title=data["title"],
            message=data["message"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            campaign_id=data.get("campaign_id"),
            campaign_name=data.get("campaign_name"),
            ad_id=data.get("ad_id"),
            ad_name=data.get("ad_name"),
            vertical=data.get("vertical"),
            metric_value=data.get("metric_value"),
            threshold_value=data.get("threshold_value"),
            acknowledged=data.get("acknowledged", False),
            acknowledged_at=datetime.fromisoformat(data["acknowledged_at"]) if data.get("acknowledged_at") else None,
            metadata=data.get("metadata", {}),
        )


def _generate_alert_id(alert_type: AlertType, identifier: str) -> str:
    """Generate a unique but deterministic alert ID."""
    timestamp_bucket = datetime.now().strftime("%Y%m%d%H")  # Hour bucket
    return sha256_key(f"{alert_type.value}:{identifier}:{timestamp_bucket}")[:16]


class AlertMonitor:
    """
    Monitors campaign performance and triggers alerts.
    
    This class can run in the background to continuously check
    for alert conditions.
    """

    def __init__(
        self,
        cfg: AppConfig,
        cache: SqliteCache,
        channels: Optional[Sequence["AlertChannel"]] = None,
    ):
        self.cfg = cfg
        self.cache = cache
        self.channels = list(channels) if channels else []
        self._stop_event = threading.Event()
        self._monitor_thread: Optional[threading.Thread] = None
        self._recent_alerts: List[Alert] = []
        self._alert_history_key = "alert_history"

    def add_channel(self, channel: "AlertChannel") -> None:
        """Add an alert channel."""
        self.channels.append(channel)

    def check_alerts(self, df: pd.DataFrame) -> List[Alert]:
        """
        Check for alert conditions in the given data.
        
        Args:
            df: DataFrame with combined Meta + Leadspedia data
            
        Returns:
            List of triggered alerts
        """
        if df.empty:
            return []

        alerts: List[Alert] = []
        now = datetime.now()

        for _, row in df.iterrows():
            row_alerts = self._check_row_alerts(row, now)
            alerts.extend(row_alerts)

        return alerts

    def _check_row_alerts(self, row: pd.Series, timestamp: datetime) -> List[Alert]:
        """Check alert conditions for a single row of data."""
        alerts: List[Alert] = []
        
        campaign_id = str(row.get("campaign_id", ""))
        campaign_name = str(row.get("campaign_name", ""))
        ad_id = str(row.get("ad_id", ""))
        ad_name = str(row.get("ad_name", ""))
        
        # Get thresholds for this campaign's vertical
        mapping = self.cfg.get_campaign_mapping(campaign_id)
        vertical = mapping.vertical if mapping else None
        thresholds = self.cfg.get_thresholds_for_vertical(vertical)
        
        # Check sell-through rate
        sell_rate = float(row.get("sell_through_rate", 100) or 100)
        if sell_rate < thresholds.min_sell_rate:
            severity = AlertSeverity.CRITICAL if sell_rate < thresholds.min_sell_rate - 10 else AlertSeverity.WARNING
            alerts.append(Alert(
                id=_generate_alert_id(AlertType.LOW_SELL_RATE, f"{campaign_id}:{ad_id}"),
                alert_type=AlertType.LOW_SELL_RATE,
                severity=severity,
                title=f"Low Sell-Through Rate: {ad_name}",
                message=f"Sell-through rate {sell_rate:.1f}% is below threshold {thresholds.min_sell_rate}%",
                timestamp=timestamp,
                campaign_id=campaign_id,
                campaign_name=campaign_name,
                ad_id=ad_id,
                ad_name=ad_name,
                vertical=vertical,
                metric_value=sell_rate,
                threshold_value=thresholds.min_sell_rate,
            ))
        
        # Check ROI
        roi = float(row.get("roi", 0) or 0)
        if roi < thresholds.min_roi:
            severity = AlertSeverity.CRITICAL if roi < 0 else AlertSeverity.WARNING
            alerts.append(Alert(
                id=_generate_alert_id(AlertType.LOW_ROI, f"{campaign_id}:{ad_id}"),
                alert_type=AlertType.LOW_ROI,
                severity=severity,
                title=f"Low ROI: {ad_name}",
                message=f"ROI {roi:.1f}% is below target {thresholds.min_roi}%",
                timestamp=timestamp,
                campaign_id=campaign_id,
                campaign_name=campaign_name,
                ad_id=ad_id,
                ad_name=ad_name,
                vertical=vertical,
                metric_value=roi,
                threshold_value=thresholds.min_roi,
            ))
        
        # Check for negative profit (always critical)
        profit = float(row.get("profit", 0) or 0)
        if profit < 0 and thresholds.alert_on_negative_margin:
            alerts.append(Alert(
                id=_generate_alert_id(AlertType.NEGATIVE_MARGIN, f"{campaign_id}:{ad_id}"),
                alert_type=AlertType.NEGATIVE_MARGIN,
                severity=AlertSeverity.CRITICAL,
                title=f"Negative Profit: {ad_name}",
                message=f"Ad is losing money: ${profit:.2f} profit",
                timestamp=timestamp,
                campaign_id=campaign_id,
                campaign_name=campaign_name,
                ad_id=ad_id,
                ad_name=ad_name,
                vertical=vertical,
                metric_value=profit,
                threshold_value=0,
            ))
        
        # Check rejection rate (warning if > 10%)
        rejection_rate = float(row.get("rejection_rate", 0) or 0)
        if rejection_rate > 10:
            alerts.append(Alert(
                id=_generate_alert_id(AlertType.HIGH_REJECTION, f"{campaign_id}:{ad_id}"),
                alert_type=AlertType.HIGH_REJECTION,
                severity=AlertSeverity.WARNING,
                title=f"High Rejection Rate: {ad_name}",
                message=f"Rejection rate {rejection_rate:.1f}% is unusually high",
                timestamp=timestamp,
                campaign_id=campaign_id,
                campaign_name=campaign_name,
                ad_id=ad_id,
                ad_name=ad_name,
                vertical=vertical,
                metric_value=rejection_rate,
                threshold_value=10.0,
            ))
        
        # Check unsold leads
        unsold = int(row.get("lp_pending_leads", 0) or 0)
        total_leads = int(row.get("lp_total_leads", 0) or 0)
        if unsold > 0 and total_leads > 0:
            unsold_pct = unsold / total_leads * 100
            if unsold_pct > (100 - thresholds.min_sell_rate):
                alerts.append(Alert(
                    id=_generate_alert_id(AlertType.UNSOLD_LEAD, f"{campaign_id}:{ad_id}"),
                    alert_type=AlertType.UNSOLD_LEAD,
                    severity=AlertSeverity.WARNING,
                    title=f"Unsold Leads: {ad_name}",
                    message=f"{unsold} leads ({unsold_pct:.1f}%) remain unsold",
                    timestamp=timestamp,
                    campaign_id=campaign_id,
                    campaign_name=campaign_name,
                    ad_id=ad_id,
                    ad_name=ad_name,
                    vertical=vertical,
                    metric_value=float(unsold),
                    metadata={"unsold_percentage": unsold_pct},
                ))
        
        return alerts

    def send_alerts(self, alerts: List[Alert]) -> Dict[str, bool]:
        """
        Send alerts through all configured channels.
        
        Args:
            alerts: List of alerts to send
            
        Returns:
            Dictionary mapping channel names to success status
        """
        results: Dict[str, bool] = {}
        
        for channel in self.channels:
            try:
                channel.send(alerts)
                results[channel.name] = True
            except Exception as e:
                results[channel.name] = False
                # Log the error but continue with other channels
                print(f"Alert channel {channel.name} failed: {e}")
        
        # Store alerts in history
        self._store_alert_history(alerts)
        
        return results

    def _store_alert_history(self, alerts: List[Alert]) -> None:
        """Store alerts in cache for history tracking."""
        # Get existing history
        history_json = self.cache.get(self._alert_history_key, ttl_seconds=86400 * 7)  # 7 days
        history: List[Dict[str, Any]] = []
        if history_json:
            try:
                history = json.loads(history_json)
            except json.JSONDecodeError:
                pass
        
        # Add new alerts
        for alert in alerts:
            history.append(alert.to_dict())
        
        # Keep only last 1000 alerts
        history = history[-1000:]
        
        # Store back
        self.cache.set(self._alert_history_key, json.dumps(history))

    def get_alert_history(self, limit: int = 100) -> List[Alert]:
        """
        Get recent alert history.
        
        Args:
            limit: Maximum number of alerts to return
            
        Returns:
            List of recent alerts
        """
        history_json = self.cache.get(self._alert_history_key, ttl_seconds=86400 * 7)
        if not history_json:
            return []
        
        try:
            history = json.loads(history_json)
            alerts = [Alert.from_dict(a) for a in history[-limit:]]
            return list(reversed(alerts))  # Most recent first
        except (json.JSONDecodeError, KeyError, ValueError):
            return []

    def acknowledge_alert(self, alert_id: str) -> bool:
        """
        Mark an alert as acknowledged.
        
        Args:
            alert_id: ID of the alert to acknowledge
            
        Returns:
            True if alert was found and acknowledged
        """
        history_json = self.cache.get(self._alert_history_key, ttl_seconds=86400 * 7)
        if not history_json:
            return False
        
        try:
            history = json.loads(history_json)
            for alert_data in history:
                if alert_data["id"] == alert_id:
                    alert_data["acknowledged"] = True
                    alert_data["acknowledged_at"] = datetime.now().isoformat()
                    self.cache.set(self._alert_history_key, json.dumps(history))
                    return True
            return False
        except (json.JSONDecodeError, KeyError):
            return False

    def start_background_monitoring(
        self,
        data_fetcher: Callable[[], pd.DataFrame],
    ) -> None:
        """
        Start background monitoring thread.
        
        Args:
            data_fetcher: Callable that returns the current data DataFrame
        """
        if self._monitor_thread is not None and self._monitor_thread.is_alive():
            return  # Already running
        
        self._stop_event.clear()
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(data_fetcher,),
            daemon=True,
        )
        self._monitor_thread.start()

    def stop_background_monitoring(self) -> None:
        """Stop the background monitoring thread."""
        self._stop_event.set()
        if self._monitor_thread is not None:
            self._monitor_thread.join(timeout=5)
            self._monitor_thread = None

    def _monitor_loop(self, data_fetcher: Callable[[], pd.DataFrame]) -> None:
        """Background monitoring loop."""
        while not self._stop_event.is_set():
            try:
                # Fetch current data
                df = data_fetcher()
                
                # Check for alerts
                alerts = self.check_alerts(df)
                
                # Filter out recently sent alerts (deduplication)
                new_alerts = self._filter_recent_alerts(alerts)
                
                # Send alerts
                if new_alerts:
                    self.send_alerts(new_alerts)
                    self._recent_alerts.extend(new_alerts)
                    # Keep only last hour of recent alerts for deduplication
                    cutoff = datetime.now() - timedelta(hours=1)
                    self._recent_alerts = [a for a in self._recent_alerts if a.timestamp > cutoff]
                
            except Exception as e:
                # Log error but continue monitoring
                print(f"Monitor loop error: {e}")
            
            # Wait for next check interval
            self._stop_event.wait(self.cfg.alert_check_interval_seconds)

    def _filter_recent_alerts(self, alerts: List[Alert]) -> List[Alert]:
        """Filter out alerts that were recently sent (within the hour)."""
        recent_ids = {a.id for a in self._recent_alerts}
        return [a for a in alerts if a.id not in recent_ids]


# Type hint for AlertChannel (defined in channels.py)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.alerts.channels import AlertChannel

