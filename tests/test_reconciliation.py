from reconciliation.services.reconciler import FieldRule, ReconciliationConfig, Reconciler


def test_reconciler_picks_best_match():
    source_records = [
        {"name": "Alice", "amount": 100.0},
        {"name": "Bob", "amount": 200.0},
    ]
    target_records = [
        {"name": "Alicia", "amount": 100.0},
        {"name": "Robert", "amount": 199.5},
    ]
    config = ReconciliationConfig(
        field_rules=[
            FieldRule("name", "name", weight=0.6, metric="string"),
            FieldRule("amount", "amount", weight=0.4, metric="numeric", tolerance=1.0),
        ],
        min_confidence=0.5,
        auto_approve_threshold=0.85,
    )

    reconciler = Reconciler(config)
    matches = reconciler.match(source_records, target_records)

    assert matches[0].decision == "auto-approved"
    assert matches[0].score > matches[1].score
    assert matches[1].decision == "needs-review"
    assert "name->name" in matches[0].details
