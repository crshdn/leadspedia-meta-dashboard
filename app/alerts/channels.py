"""
Alert notification channels.

This module provides implementations for different alert delivery channels
including Email, Slack, and Dashboard notifications.
"""

from __future__ import annotations

import json
import smtplib
from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, List, Optional

import requests

from app.alerts.monitor import Alert, AlertSeverity
from app.config import AppConfig


class AlertChannel(ABC):
    """Abstract base class for alert channels."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Channel name for identification."""
        pass
    
    @abstractmethod
    def send(self, alerts: List[Alert]) -> None:
        """
        Send alerts through this channel.
        
        Args:
            alerts: List of alerts to send
            
        Raises:
            Exception: If sending fails
        """
        pass
    
    @property
    @abstractmethod
    def is_configured(self) -> bool:
        """Check if this channel is properly configured."""
        pass


class EmailAlertChannel(AlertChannel):
    """
    Email alert channel using SMTP.
    
    Sends formatted HTML emails for alerts.
    """
    
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_user: Optional[str],
        smtp_password: Optional[str],
        from_address: str,
        to_address: str,
        use_tls: bool = True,
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_address = from_address
        self.to_address = to_address
        self.use_tls = use_tls

    @property
    def name(self) -> str:
        return "email"

    @property
    def is_configured(self) -> bool:
        return bool(self.smtp_host and self.from_address and self.to_address)

    @classmethod
    def from_config(cls, cfg: AppConfig) -> Optional["EmailAlertChannel"]:
        """Create an EmailAlertChannel from AppConfig."""
        if not cfg.alert_email_enabled:
            return None
        if not cfg.alert_smtp_host or not cfg.alert_email_to or not cfg.alert_email_from:
            return None
        
        return cls(
            smtp_host=cfg.alert_smtp_host,
            smtp_port=cfg.alert_smtp_port,
            smtp_user=cfg.alert_smtp_user,
            smtp_password=cfg.alert_smtp_password,
            from_address=cfg.alert_email_from,
            to_address=cfg.alert_email_to,
        )

    def send(self, alerts: List[Alert]) -> None:
        """Send alerts via email."""
        if not alerts:
            return
        
        if not self.is_configured:
            raise ValueError("Email channel not properly configured")
        
        # Group alerts by severity for the subject line
        critical_count = sum(1 for a in alerts if a.severity == AlertSeverity.CRITICAL)
        warning_count = sum(1 for a in alerts if a.severity == AlertSeverity.WARNING)
        
        subject = self._build_subject(critical_count, warning_count, len(alerts))
        html_body = self._build_html_body(alerts)
        text_body = self._build_text_body(alerts)
        
        # Parse recipients (supports comma-separated emails)
        recipients = [email.strip() for email in self.to_address.split(",") if email.strip()]
        
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.from_address
        msg["To"] = ", ".join(recipients)
        
        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))
        
        # Send
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            if self.use_tls:
                server.starttls()
            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.from_address, recipients, msg.as_string())

    def _build_subject(self, critical: int, warning: int, total: int) -> str:
        """Build email subject line."""
        if critical > 0:
            return f"🚨 CRITICAL: {critical} critical alert(s) - Meta Ads Dashboard"
        elif warning > 0:
            return f"⚠️ WARNING: {warning} warning(s) - Meta Ads Dashboard"
        else:
            return f"ℹ️ {total} alert(s) - Meta Ads Dashboard"

    def _build_html_body(self, alerts: List[Alert]) -> str:
        """Build HTML email body."""
        severity_colors = {
            AlertSeverity.CRITICAL: "#dc3545",
            AlertSeverity.WARNING: "#ffc107",
            AlertSeverity.INFO: "#17a2b8",
        }
        
        rows = ""
        for alert in alerts:
            color = severity_colors.get(alert.severity, "#6c757d")
            rows += f"""
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">
                    <span style="background-color: {color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">
                        {alert.severity.value.upper()}
                    </span>
                </td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{alert.title}</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{alert.message}</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{alert.campaign_name or '-'}</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{alert.timestamp.strftime('%Y-%m-%d %H:%M')}</td>
            </tr>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th {{ background-color: #f8f9fa; padding: 12px 8px; text-align: left; border-bottom: 2px solid #dee2e6; }}
            </style>
        </head>
        <body>
            <h2>Meta Ads Dashboard Alerts</h2>
            <p>The following alerts have been triggered:</p>
            <table>
                <tr>
                    <th>Severity</th>
                    <th>Alert</th>
                    <th>Details</th>
                    <th>Campaign</th>
                    <th>Time</th>
                </tr>
                {rows}
            </table>
            <p style="color: #6c757d; font-size: 12px; margin-top: 20px;">
                This is an automated message from your Meta Ads Dashboard.
            </p>
        </body>
        </html>
        """

    def _build_text_body(self, alerts: List[Alert]) -> str:
        """Build plain text email body."""
        lines = ["Meta Ads Dashboard Alerts", "=" * 40, ""]
        
        for alert in alerts:
            lines.append(f"[{alert.severity.value.upper()}] {alert.title}")
            lines.append(f"  {alert.message}")
            lines.append(f"  Campaign: {alert.campaign_name or 'N/A'}")
            lines.append(f"  Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M')}")
            lines.append("")
        
        return "\n".join(lines)


class SlackAlertChannel(AlertChannel):
    """
    Slack alert channel using webhooks.
    
    Sends formatted Slack messages with alert blocks.
    """
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    @property
    def name(self) -> str:
        return "slack"

    @property
    def is_configured(self) -> bool:
        return bool(self.webhook_url)

    @classmethod
    def from_config(cls, cfg: AppConfig) -> Optional["SlackAlertChannel"]:
        """Create a SlackAlertChannel from AppConfig."""
        if not cfg.alert_slack_enabled:
            return None
        if not cfg.alert_slack_webhook_url:
            return None
        
        return cls(webhook_url=cfg.alert_slack_webhook_url)

    def send(self, alerts: List[Alert]) -> None:
        """Send alerts to Slack."""
        if not alerts:
            return
        
        if not self.is_configured:
            raise ValueError("Slack channel not properly configured")
        
        payload = self._build_payload(alerts)
        
        response = requests.post(
            self.webhook_url,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()

    def _build_payload(self, alerts: List[Alert]) -> Dict[str, Any]:
        """Build Slack webhook payload."""
        # Group by severity
        critical = [a for a in alerts if a.severity == AlertSeverity.CRITICAL]
        warnings = [a for a in alerts if a.severity == AlertSeverity.WARNING]
        info = [a for a in alerts if a.severity == AlertSeverity.INFO]
        
        # Build header
        if critical:
            header_emoji = "🚨"
            header_text = f"{len(critical)} Critical Alert(s)"
        elif warnings:
            header_emoji = "⚠️"
            header_text = f"{len(warnings)} Warning(s)"
        else:
            header_emoji = "ℹ️"
            header_text = f"{len(info)} Info Alert(s)"
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{header_emoji} Meta Ads Dashboard: {header_text}",
                    "emoji": True,
                }
            },
            {"type": "divider"},
        ]
        
        # Add alert blocks
        for alert in alerts[:10]:  # Limit to 10 alerts
            severity_emoji = {
                AlertSeverity.CRITICAL: "🔴",
                AlertSeverity.WARNING: "🟡",
                AlertSeverity.INFO: "🔵",
            }.get(alert.severity, "⚪")
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{severity_emoji} *{alert.title}*\n{alert.message}",
                },
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Campaign:*\n{alert.campaign_name or 'N/A'}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Time:*\n{alert.timestamp.strftime('%H:%M')}",
                    },
                ],
            })
        
        if len(alerts) > 10:
            blocks.append({
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"_...and {len(alerts) - 10} more alerts_",
                    }
                ],
            })
        
        return {"blocks": blocks}


class DashboardAlertChannel(AlertChannel):
    """
    Dashboard alert channel.
    
    Stores alerts for display in the Streamlit dashboard.
    This channel doesn't send external notifications but makes
    alerts available for the dashboard UI.
    """
    
    def __init__(self, max_alerts: int = 100):
        self.max_alerts = max_alerts
        self._alerts: List[Alert] = []

    @property
    def name(self) -> str:
        return "dashboard"

    @property
    def is_configured(self) -> bool:
        return True  # Always configured

    def send(self, alerts: List[Alert]) -> None:
        """Store alerts for dashboard display."""
        self._alerts.extend(alerts)
        # Keep only most recent alerts
        self._alerts = self._alerts[-self.max_alerts:]

    def get_alerts(self) -> List[Alert]:
        """Get all stored alerts."""
        return list(reversed(self._alerts))

    def get_unacknowledged(self) -> List[Alert]:
        """Get unacknowledged alerts."""
        return [a for a in self._alerts if not a.acknowledged]

    def get_by_severity(self, severity: AlertSeverity) -> List[Alert]:
        """Get alerts by severity."""
        return [a for a in self._alerts if a.severity == severity]

    def clear(self) -> None:
        """Clear all alerts."""
        self._alerts.clear()

    def acknowledge(self, alert_id: str) -> bool:
        """Acknowledge an alert by ID."""
        from datetime import datetime
        for alert in self._alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                alert.acknowledged_at = datetime.now()
                return True
        return False


def create_channels_from_config(cfg: AppConfig) -> List[AlertChannel]:
    """
    Create all configured alert channels from AppConfig.
    
    Args:
        cfg: Application configuration
        
    Returns:
        List of configured and enabled alert channels
    """
    channels: List[AlertChannel] = []
    
    # Always add dashboard channel
    channels.append(DashboardAlertChannel())
    
    # Add email channel if configured
    email = EmailAlertChannel.from_config(cfg)
    if email:
        channels.append(email)
    
    # Add Slack channel if configured
    slack = SlackAlertChannel.from_config(cfg)
    if slack:
        channels.append(slack)
    
    return channels

