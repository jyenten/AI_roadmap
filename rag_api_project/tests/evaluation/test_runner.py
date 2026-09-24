import pytest

from evaluation.models import (
    EvaluationQuestion,
    GoldEvidence,
    RetrievalConfig,
)
from evaluation.runner import (
    evaluate_dataset,
    evaluate_question,
)


class FakeRetriever:
    def search(
        self,
        query: str,
    ):
        return (
            [
                "Unrelated text.",
                (
                    "OSPF calculator cost using "
                    "cost = reference_bandwidth / interface_bandwidth"
                ),
            ],
            [
                0.1,
                0.2,
            ],
            [
                {
                    "source": "manual.pdf",
                    "page": 10,
                },
                {
                    "source": "manual.pdf",
                    "page": 26,
                },
            ],
        )


def build_question() -> EvaluationQuestion:
    return EvaluationQuestion(
        id="dev_001",
        topic="cost",
        question="How is OSPF cost calculated?",
        gold_evidence=(
            GoldEvidence(
                source="manual.pdf",
                pages=(26,),
                contains_any=(
                    "cost = reference_bandwidth / interface_bandwidth",
            ),
        ),
    ),
)


def test_evaluate_question_returns_gold_rankk() -> None:
    result = evaluate_question(
        build_question(),
        FakeRetriever(),
    )

    assert result.first_evidence_rank == 2
    assert result.reciprocal_rank == 0.5


def  test_evaluate_dataset_builds_run() -> None:
    question = build_question()

    run = evaluate_dataset(
        [question],
        FakeRetriever(),
        dataset="dev",
        dataset_hash="abc123",
        retrieval_config=RetrievalConfig(
            collection_name="ospf",
            embedding_model_name="model",
            retrieval_results=8,
        ),
        git_commit="commit123",
        git_dirty=False,
        timestamp="2026-09-23T11:00:00+02:00",
    )

    assert run.question_count == 1
    assert run.metrics.mrr == 0.5
    assert run.metrics.hit_at_3 == 1
    assert run.questions[0].id == "dev_001"
    

def test_evaluate_question_rejects_inconsistent_results() -> None:
    class BrokenRetriever:
        def search(
            self,
            query: str,
        ):
            return (
                ["document"],
                [],
                [{"source": "manual.pdf", "page": 1}],
            )

    with pytest.raises(
        RuntimeError,
        match="inconsistent result lengths",
    ):
        evaluate_question(
            build_question(),
            BrokenRetriever(),
        )

