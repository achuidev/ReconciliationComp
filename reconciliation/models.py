"""Database models for reconciliation runs and records."""
from __future__ import annotations
from django.db import models


class ReconciliationRule(models.Model):
    """Rule configuring how to match records between two data sets."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # JSON field for arbitrary matching configuration (keys, weights, thresholds)
    config = models.JSONField(default=dict)

    def __str__(self) -> str:
        return self.name


class ReconciliationRun(models.Model):
    """Represents an execution of reconciliation between two data sources."""

    created_at = models.DateTimeField(auto_now_add=True)
    rule = models.ForeignKey(ReconciliationRule, on_delete=models.PROTECT)
    source_label = models.CharField(max_length=255)
    target_label = models.CharField(max_length=255)

    def __str__(self) -> str:  # pragma: no cover - repr convenience
        return f"Run {self.pk} ({self.source_label} -> {self.target_label})"


class SourceRecord(models.Model):
    """A record coming from the source system."""

    run = models.ForeignKey(ReconciliationRun, on_delete=models.CASCADE)
    payload = models.JSONField()

    def __str__(self) -> str:  # pragma: no cover - repr convenience
        return f"SourceRecord {self.pk}"


class TargetRecord(models.Model):
    """A record coming from the target system."""

    run = models.ForeignKey(ReconciliationRun, on_delete=models.CASCADE)
    payload = models.JSONField()

    def __str__(self) -> str:  # pragma: no cover - repr convenience
        return f"TargetRecord {self.pk}"


class MatchCandidate(models.Model):
    """Stores the outcome of matching a source record to a target record."""

    run = models.ForeignKey(ReconciliationRun, on_delete=models.CASCADE)
    source_record = models.ForeignKey(SourceRecord, on_delete=models.CASCADE)
    target_record = models.ForeignKey(TargetRecord, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    matched_on = models.JSONField(default=dict)
    decision = models.CharField(max_length=32, default="pending")

    class Meta:
        unique_together = ("source_record", "target_record")

    def __str__(self) -> str:  # pragma: no cover - repr convenience
        return f"MatchCandidate {self.pk}: {self.score}"
