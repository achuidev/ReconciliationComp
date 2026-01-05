"""Admin registrations for reconciliation models."""
from django.contrib import admin

from reconciliation.models import MatchCandidate, ReconciliationRule, ReconciliationRun, SourceRecord, TargetRecord

@admin.register(ReconciliationRule)
class ReconciliationRuleAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(ReconciliationRun)
class ReconciliationRunAdmin(admin.ModelAdmin):
    list_display = ("id", "source_label", "target_label", "created_at")
    list_filter = ("source_label", "target_label")
    search_fields = ("source_label", "target_label")


@admin.register(SourceRecord)
class SourceRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "run")
    list_filter = ("run",)


@admin.register(TargetRecord)
class TargetRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "run")
    list_filter = ("run",)


@admin.register(MatchCandidate)
class MatchCandidateAdmin(admin.ModelAdmin):
    list_display = ("id", "run", "source_record", "target_record", "score", "decision")
    list_filter = ("decision", "run")
    search_fields = ("source_record__id", "target_record__id")
