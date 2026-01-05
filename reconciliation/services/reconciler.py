"""Core reconciliation engine that can be reused across Django projects."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from reconciliation.services.metrics import (
    flatten_values,
    numeric_similarity,
    string_similarity,
    weighted_score,
)


@dataclass
class FieldRule:
    """Configuration for comparing a single field between source and target."""

    source_key: str
    target_key: str
    weight: float = 1.0
    metric: str = "string"
    tolerance: float = 0.0

    def score(self, source: Mapping[str, Any], target: Mapping[str, Any]) -> float:
        left = source.get(self.source_key)
        right = target.get(self.target_key)
        if self.metric == "numeric":
            return numeric_similarity(left, right, self.tolerance)
        return string_similarity(left, right)


@dataclass
class ReconciliationConfig:
    """Collection of rules and thresholds for reconciliation."""

    field_rules: Sequence[FieldRule]
    min_confidence: float = 0.7
    auto_approve_threshold: float = 0.9


@dataclass
class MatchResult:
    source: Mapping[str, Any]
    target: Mapping[str, Any]
    score: float
    details: dict[str, Any]
    decision: str


class Reconciler:
    """Apply reconciliation rules to two sets of records."""

    def __init__(self, config: ReconciliationConfig) -> None:
        self.config = config

    def match(self, source_records: Iterable[Mapping[str, Any]], target_records: Iterable[Mapping[str, Any]]) -> list[MatchResult]:
        results: list[MatchResult] = []
        targets = list(target_records)
        for source in source_records:
            best_candidate = self._find_best_match(source, targets)
            results.append(best_candidate)
        return results

    def _find_best_match(self, source: Mapping[str, Any], targets: Sequence[Mapping[str, Any]]) -> MatchResult:
        best_score = -1.0
        best_target: Mapping[str, Any] | None = None
        best_details: dict[str, Any] = {}

        for target in targets:
            scores: list[tuple[float, float]] = []
            matched_on: dict[str, Any] = {}
            for rule in self.config.field_rules:
                field_score = rule.score(source, target)
                scores.append((field_score, rule.weight))
                matched_on[f"{rule.source_key}->{rule.target_key}"] = field_score
            combined_score = weighted_score(scores)
            if combined_score > best_score:
                best_score = combined_score
                best_target = target
                best_details = matched_on

        decision = self._decision_for_score(best_score)
        cleaned_source = flatten_values(source, [rule.source_key for rule in self.config.field_rules])
        cleaned_target = flatten_values(best_target or {}, [rule.target_key for rule in self.config.field_rules])
        return MatchResult(
            source=cleaned_source,
            target=cleaned_target,
            score=best_score if best_score >= 0 else 0.0,
            details=best_details,
            decision=decision,
        )

    def _decision_for_score(self, score: float) -> str:
        if score >= self.config.auto_approve_threshold:
            return "auto-approved"
        if score >= self.config.min_confidence:
            return "needs-review"
        return "rejected"
