"""REST-style views showcasing reconciliation usage."""
from __future__ import annotations
from django.http import JsonResponse
from django.views import View

from reconciliation.services.reconciler import FieldRule, ReconciliationConfig, Reconciler


class ReconcileView(View):
    """Accepts two lists of dictionaries and returns match decisions."""

    def post(self, request, *args, **kwargs):  # type: ignore[override]
        data = request.json if hasattr(request, "json") else request.POST
        source = data.get("source", [])
        target = data.get("target", [])
        rules = [
            FieldRule("name", "name", weight=0.6, metric="string"),
            FieldRule("amount", "amount", weight=0.4, metric="numeric", tolerance=0.01),
        ]
        config = ReconciliationConfig(field_rules=rules)
        reconciler = Reconciler(config)
        matches = reconciler.match(source, target)
        serialized = [
            {
                "source": match.source,
                "target": match.target,
                "score": match.score,
                "details": match.details,
                "decision": match.decision,
            }
            for match in matches
        ]
        return JsonResponse({"results": serialized})
