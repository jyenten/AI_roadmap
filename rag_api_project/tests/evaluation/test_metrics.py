from evaluation.metrics import (
    aggregate_metrics,
    hit_at_k,
    reciprocal_rank,
)


def test_reciprocal_rank() -> None:
    assert reciprocal_rank(1) == 1.0
    assert reciprocal_rank(2) == 0.5
    assert reciprocal_rank(4) == 0.25
    assert reciprocal_rank(None) == 0.0


def test_hit_at_k() -> None:
    assert hit_at_k(3, 3) == 1
    assert hit_at_k(4, 3) == 0
    assert hit_at_k(None, 3) == 0


def test_aggregate_metrics() -> None:
    metrics = aggregate_metrics(
        [
            1,
            2,
            None,
            4,
        ]
    )

    assert metrics.mrr == 0.4375
    assert metrics.hit_at_1 == 0.25
    assert metrics.hit_at_3 == 0.5
    assert metrics.hit_at_5 == 0.75
    assert metrics.hit_at_8 == 0.75
