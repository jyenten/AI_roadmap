import pytest

from evaluation.models import (
    EvaluationQuestion,
    GoldEvidence,
)
from evaluation.random_eval import sample_questions

def build_questions(
    count: int = 10,
) -> tuple[EvaluationQuestion, ...]:
    return tuple(
        EvaluationQuestion(
            id=f"random_{index:03d}",
            topic="test",
            question=f"Question {index}",
            gold_evidence=(
                GoldEvidence(
                    source="manual.pdf",
                    pages=(index + 1,),
                    contains_any=(
                        f"Evidence {index}",
                    ),
                ),
            ),
        )
        for index in range(count)
    )


def test_sampling_is_reproducible() -> None:
    questions = build_questions()

    first_sample = sample_questions(
        questions,
        sample_size=4,
        seed=42,
    )

    second_sample = sample_questions(
        questions,
        sample_size=4,
        seed=42,
    )

    assert first_sample == second_sample


def test_sampling_returns_unique_subset() -> None:
    questions = build_questions()

    sample = sample_questions(
        questions,
        sample_size=5,
        seed=42,
    )

    ids = [
        question.id
        for question in sample
    ]

    assert len(sample) == 5
    assert len(set(ids)) == 5


def test_sampling_rejects_oversized_sample() -> None:
    questions = build_questions(
        count=3
    )

    with pytest.raises(
        ValueError,
        match="cannot exceed",
    ):
        sample_questions(
            questions,
            sample_size=4,
            seed=42,
        )