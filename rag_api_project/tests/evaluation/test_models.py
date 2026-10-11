from dataclasses import FrozenInstanceError

import pytest

from evaluation.models import (
    EvaluationMetrics,
    EvaluationQuestion,
    EvaluationRun,
    GoldEvidence,
    LatencyMetrics,
    QuestionResult,
    RetrievalConfig,
)


def test_evaluation_question_contains_typed_gold_evidence() -> None:
    evidence = GoldEvidence(
        source="manual.pdf",
        pages=(26,),
        contains_any=(
            "cost = reference_bandwidth / interface_bandwidth",
        ),
    )

    question = EvaluationQuestion(
        id="ospf_dev_004",
        topic="cost-calculation",
        question="How does OSPF calculate interface cost?",
        gold_evidence=(evidence,),
    )

    assert question.gold_evidence[0].source == "manual.pdf"
    assert question.gold_evidence[0].pages == (26,)


def test_evaluation_models_are_immutable() -> None:
    result = QuestionResult(
        id="ospf_dev_004",
        first_evidence_rank=1,
        reciprocal_rank=1.0,
    )

    with pytest.raises(FrozenInstanceError):
        result.first_evidence_rank = 2


def test_evaluation_run_composes_results_and_metrics() -> None:
    metrics = EvaluationMetrics(
        mrr=1.0,
        hit_at_1=1.0,
        hit_at_3=1.0,
        hit_at_5=1.0,
        hit_at_8=1.0,
    )

    config = RetrievalConfig(
        collection_name="ospf",
        embedding_model_name="all-MiniLM-L6-v2",
        retrieval_results=8,
    )

    result = QuestionResult(
        id="ospf_dev_004",
        first_evidence_rank=1,
        reciprocal_rank=1.0,
    )

    run = EvaluationRun(
        timestamp="2026-09-17T20:00:00+02:00",
        git_commit="abc123",
        git_dirty=False,
        dataset_hash="hash123",
        dataset="dev",
        question_count=1,
        retrieval_config=config,
        metrics=metrics,
        questions=(result,),
    )

    assert run.metrics.mrr == 1.0
    assert run.retrieval_config.retrieval_results == 8
    assert run.questions == (result,)
    assert run.latency is None


@pytest.mark.parametrize("field", ["mean_ms", "p50_ms", "p95_ms"])
@pytest.mark.parametrize("value", [-1, float("nan"), float("inf"), -float("inf"), True, "1", None])
def test_latency_rejects_invalid_values(field, value):
    values = dict(mean_ms=2.0, p50_ms=1.0, p95_ms=3.0)
    values[field] = value
    with pytest.raises(ValueError):
        LatencyMetrics(**values)


@pytest.mark.parametrize("field", ["mean_ms", "p50_ms", "p95_ms"])
@pytest.mark.parametrize("value", [10**1000, -(10**1000)], ids=["huge-positive", "huge-negative"])
def test_latency_rejects_extremely_large_integers(field, value):
    values = dict(mean_ms=2.0, p50_ms=1.0, p95_ms=3.0)
    values[field] = value
    with pytest.raises(ValueError, match=f"{field} must be a finite non-negative number"):
        LatencyMetrics(**values)


def test_latency_is_frozen_slotted_and_ordered():
    latency = LatencyMetrics(0, 0, 0)
    assert not hasattr(latency, "__dict__")
    with pytest.raises(FrozenInstanceError):
        latency.mean_ms = 1
    with pytest.raises(ValueError, match="p95_ms"):
        LatencyMetrics(1, 2, 1)
