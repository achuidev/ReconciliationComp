"""Utility functions for scoring potential matches."""
from __future__ import annotations
from difflib import SequenceMatcher
from typing import Any, Iterable, Mapping


def normalized_string(value: Any) -> str:
    return "" if value is None else str(value).strip().lower()


def string_similarity(left: Any, right: Any) -> float:
    """Compute ratio-based similarity between two arbitrary values."""
    lval = normalized_string(left)
    rval = normalized_string(right)
    if not lval and not rval:
        return 1.0
    return SequenceMatcher(None, lval, rval).ratio()


def numeric_similarity(left: Any, right: Any, tolerance: float = 0.0) -> float:
    """Return 1 when difference is within tolerance, otherwise a decayed score."""
    try:
        lnum = float(left)
        rnum = float(right)
    except (TypeError, ValueError):
        return 0.0

    diff = abs(lnum - rnum)
    if diff <= tolerance:
        return 1.0
    return max(0.0, 1 - diff / max(abs(lnum), abs(rnum), 1))


def weighted_score(scores: Iterable[tuple[float, float]]) -> float:
    """Combine a list of (score, weight) tuples into a weighted average."""
    total_weight = sum(weight for _, weight in scores)
    if total_weight == 0:
        return 0.0
    return sum(score * weight for score, weight in scores) / total_weight


def flatten_values(payload: Mapping[str, Any], keys: Iterable[str]) -> dict[str, Any]:
    """Pull out a subset of keys from a payload, ignoring missing ones."""
    return {key: payload.get(key) for key in keys if key in payload}
