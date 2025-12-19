"""
Statistical confidence scoring for ad performance data.

Provides confidence levels based on spend and lead thresholds,
action recommendations, and sample size requirements for statistical significance.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

import pandas as pd


class ConfidenceLevel(str, Enum):
    """Confidence level for ad performance data reliability."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ActionRecommendation(str, Enum):
    """Recommended action based on confidence and CPL."""
    SCALE = "scale"
    MAINTAIN = "maintain"
    KILL = "kill"
    NEEDS_DATA = "needs_data"


@dataclass(frozen=True)
class ConfidenceThresholds:
    """Configurable thresholds for confidence scoring."""
    high_spend: float = 500.0
    high_leads: int = 30
    medium_spend: float = 250.0
    medium_leads: int = 15
    
    # CPL thresholds for action recommendations
    cpl_target: float = 30.0
    cpl_acceptable: float = 45.0


# Default thresholds
DEFAULT_THRESHOLDS = ConfidenceThresholds()


def compute_confidence_level(
    spend: float,
    leads: int,
    thresholds: ConfidenceThresholds = DEFAULT_THRESHOLDS,
) -> ConfidenceLevel:
    """
    Determine confidence level based on spend and lead count.
    
    High confidence requires BOTH spend >= threshold AND leads >= threshold.
    Medium confidence requires BOTH spend >= medium threshold AND leads >= medium threshold.
    Otherwise, confidence is low.
    """
    if spend >= thresholds.high_spend and leads >= thresholds.high_leads:
        return ConfidenceLevel.HIGH
    if spend >= thresholds.medium_spend and leads >= thresholds.medium_leads:
        return ConfidenceLevel.MEDIUM
    return ConfidenceLevel.LOW


def compute_action_recommendation(
    confidence: ConfidenceLevel,
    cpl: Optional[float],
    thresholds: ConfidenceThresholds = DEFAULT_THRESHOLDS,
) -> ActionRecommendation:
    """
    Determine recommended action based on confidence level and CPL.
    
    Only high-confidence data gets actionable recommendations.
    Medium/low confidence always returns NEEDS_DATA.
    """
    if confidence != ConfidenceLevel.HIGH:
        return ActionRecommendation.NEEDS_DATA
    
    if cpl is None:
        return ActionRecommendation.NEEDS_DATA
    
    if cpl <= thresholds.cpl_target:
        return ActionRecommendation.SCALE
    if cpl <= thresholds.cpl_acceptable:
        return ActionRecommendation.MAINTAIN
    return ActionRecommendation.KILL


def compute_required_sample_size(
    current_leads: int,
    target_leads: int = 50,
    current_spend: float = 0.0,
    current_cpl: Optional[float] = None,
) -> dict:
    """
    Calculate how much more data is needed for statistical significance.
    
    Uses rule of thumb: ~50 conversions needed for 95% confidence
    that true CPL is within ±20% of observed CPL.
    
    Returns dict with:
        - leads_needed: additional leads required
        - spend_needed: estimated additional spend required (based on current CPL)
        - progress_pct: percentage toward target (0-100)
    """
    leads_needed = max(0, target_leads - current_leads)
    progress_pct = min(100.0, (current_leads / target_leads) * 100) if target_leads > 0 else 0.0
    
    # Estimate spend needed based on current CPL
    spend_needed: Optional[float] = None
    if current_cpl is not None and current_cpl > 0 and leads_needed > 0:
        spend_needed = leads_needed * current_cpl
    
    return {
        "leads_needed": leads_needed,
        "spend_needed": spend_needed,
        "progress_pct": progress_pct,
        "target_leads": target_leads,
        "current_leads": current_leads,
    }


def confidence_to_emoji(confidence: ConfidenceLevel) -> str:
    """Return emoji indicator for confidence level."""
    mapping = {
        ConfidenceLevel.HIGH: "🟢",
        ConfidenceLevel.MEDIUM: "🟡",
        ConfidenceLevel.LOW: "🔴",
    }
    return mapping.get(confidence, "⚪")


def action_to_display(action: ActionRecommendation) -> str:
    """Return display string for action recommendation."""
    mapping = {
        ActionRecommendation.SCALE: "SCALE ↑",
        ActionRecommendation.MAINTAIN: "MAINTAIN →",
        ActionRecommendation.KILL: "KILL ✕",
        ActionRecommendation.NEEDS_DATA: "NEEDS DATA",
    }
    return mapping.get(action, "UNKNOWN")


def add_confidence_columns(
    df: pd.DataFrame,
    thresholds: ConfidenceThresholds = DEFAULT_THRESHOLDS,
    target_leads: int = 50,
) -> pd.DataFrame:
    """
    Add confidence scoring columns to a DataFrame with ad performance data.
    
    Expects columns: spend, leads, cpl
    Adds columns: confidence, confidence_emoji, action, action_display,
                  leads_needed, spend_needed, progress_pct
    """
    if df.empty:
        return df
    
    result = df.copy()
    
    # Ensure numeric types
    for col in ["spend", "leads", "cpl"]:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors="coerce")
    
    # Compute confidence level
    def _compute_conf(row):
        spend = row.get("spend", 0) or 0
        leads = row.get("leads", 0) or 0
        return compute_confidence_level(float(spend), int(leads), thresholds)
    
    result["confidence"] = result.apply(_compute_conf, axis=1)
    result["confidence_emoji"] = result["confidence"].apply(confidence_to_emoji)
    
    # Compute action recommendation
    def _compute_action(row):
        conf = row.get("confidence", ConfidenceLevel.LOW)
        cpl = row.get("cpl")
        return compute_action_recommendation(conf, cpl, thresholds)
    
    result["action"] = result.apply(_compute_action, axis=1)
    result["action_display"] = result["action"].apply(action_to_display)
    
    # Compute sample size requirements
    def _compute_sample_req(row):
        leads = int(row.get("leads", 0) or 0)
        spend = float(row.get("spend", 0) or 0)
        cpl = row.get("cpl")
        return compute_required_sample_size(leads, target_leads, spend, cpl)
    
    sample_reqs = result.apply(_compute_sample_req, axis=1, result_type="expand")
    result["leads_needed"] = sample_reqs["leads_needed"]
    result["spend_needed"] = sample_reqs["spend_needed"]
    result["progress_pct"] = sample_reqs["progress_pct"]
    
    return result

