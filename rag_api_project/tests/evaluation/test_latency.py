from unittest.mock import Mock

import pytest

from evaluation.latency import TimedRetriever, LatencyMetrics
from evaluation.models import LatencyMetrics as CanonicalLatencyMetrics


def test_successful_search_records_one_sample_and_preserves_result(monkeypatch):
    result = (["evidence"], [0.1], [{"source": "manual.pdf", "page": 1}])
    underlying = Mock()
    underlying.search.side_effect = [result, result, RuntimeError("failed")]
    ticks = iter([0, 0.001, 1, 1.003, 2])
    monkeypatch.setattr("evaluation.latency.perf_counter", lambda: next(ticks))
    retriever = TimedRetriever(underlying)
    assert retriever.search("first") is result
    assert retriever.search("second") is result
    with pytest.raises(RuntimeError, match="failed"):
        retriever.search("third")
    assert retriever.latencies_ms == pytest.approx([1, 3])
    assert underlying.search.call_count == 3
    metrics = retriever.metrics()
    assert LatencyMetrics is CanonicalLatencyMetrics
    assert metrics.mean_ms == pytest.approx(2)
    assert metrics.p50_ms == pytest.approx(2)
    assert metrics.p95_ms == pytest.approx(3)


def test_metrics_require_samples():
    with pytest.raises(ValueError, match="No retrieval latency samples"):
        TimedRetriever(Mock()).metrics()
