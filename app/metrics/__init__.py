"""Metric computation helpers."""

from app.metrics.cpl import compute_cpl, count_leads_from_actions, extract_action_value
from app.metrics.revenue import (
    RevenueKPIs,
    calculate_revenue_kpis,
    calculate_kpis_by_dimension,
    identify_problem_areas,
    calculate_period_comparison,
)

__all__ = [
    "compute_cpl",
    "count_leads_from_actions",
    "extract_action_value",
    "RevenueKPIs",
    "calculate_revenue_kpis",
    "calculate_kpis_by_dimension",
    "identify_problem_areas",
    "calculate_period_comparison",
]
