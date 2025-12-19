from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any, Iterable, Mapping, Sequence


def _to_decimal(value: Any) -> Decimal | None:
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def extract_action_value(actions: Any, *, action_type: str) -> Decimal:
    """
    actions is typically a list[{"action_type": "...", "value": "..."}]
    """
    if not isinstance(actions, list):
        return Decimal(0)
    total = Decimal(0)
    for item in actions:
        if not isinstance(item, Mapping):
            continue
        if item.get("action_type") != action_type:
            continue
        d = _to_decimal(item.get("value"))
        if d is not None:
            total += d
    return total


def count_leads_from_actions(actions: Any, *, lead_action_types: Sequence[str]) -> int:
    total = Decimal(0)
    for t in lead_action_types:
        total += extract_action_value(actions, action_type=t)
    if total <= 0:
        return 0
    # Lead counts should be integral; guard against decimals in API by rounding down.
    return int(total)


def compute_cpl(spend: Any, leads: int) -> float | None:
    d_spend = _to_decimal(spend)
    if d_spend is None:
        return None
    if leads <= 0:
        return None
    return float(d_spend / Decimal(leads))


