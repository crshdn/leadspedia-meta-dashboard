"""
Alert system for monitoring campaign performance.

This module provides real-time monitoring and alerting for
Meta Ads + Leadspedia performance metrics.
"""

from app.alerts.monitor import (
    AlertMonitor,
    Alert,
    AlertSeverity,
    AlertType,
)
from app.alerts.channels import (
    AlertChannel,
    EmailAlertChannel,
    SlackAlertChannel,
    DashboardAlertChannel,
)

__all__ = [
    "AlertMonitor",
    "Alert",
    "AlertSeverity",
    "AlertType",
    "AlertChannel",
    "EmailAlertChannel",
    "SlackAlertChannel",
    "DashboardAlertChannel",
]

