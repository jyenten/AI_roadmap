from dataclasses import FrozenInstanceError

import pytest

from evaluation.models import (
    EvaluationMetrics,
    EvaluationQuestion,
    EvaluationRun,
    GoldEvidence,
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