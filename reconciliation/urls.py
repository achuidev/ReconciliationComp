"""URLs for reconciliation app."""
from django.urls import path

from reconciliation.views import ReconcileView

urlpatterns = [
    path("matches/", ReconcileView.as_view(), name="reconcile"),
]
