from pathlib import Path

import pytest

from evaluation import candidates
from evaluation.models import EvaluationQuestion, GoldEvidence


def make_candidate(
    question_id: str,
    question: str,
    pages: tuple[int, ...] = (1,),
) -> EvaluationQuestion:
    return EvaluationQuestion(
        id=question_id,
        topic="routing",
        question=question,
        gold_evidence=(
            GoldEvidence(
                source="guide.pdf",
                pages=pages,
                contains_any=("supporting evidence",),
            ),
        ),
    )


def test_every_declared_page_must_exist(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        candidates,
        "build_page_lookup",
        lambda _: {("guide.pdf", 1): "supporting evidence"},
    )

    with pytest.raises(
        ValueError,
        match=r"guide\.pdf page 2",
    ):
        candidates.validate_candidate_questions(
            candidates=(make_candidate("q1", "Question one?", (1, 2)),),
            existing_datasets=(),
            data_dir=Path("unused"),
        )


def test_every_declared_page_must_contain_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        candidates,
        "build_page_lookup",
        lambda _: {
            ("guide.pdf", 1): "supporting evidence",
            ("guide.pdf", 2): "unrelated material",
        },
    )

    with pytest.raises(
        ValueError,
        match=r"no contains_any fragment matches guide\.pdf page 2",
    ):
        candidates.validate_candidate_questions(
            candidates=(make_candidate("q1", "Question one?", (1, 2)),),
            existing_datasets=(),
            data_dir=Path("unused"),
        )


def test_valid_evidence_on_all_pages_passes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        candidates,
        "build_page_lookup",
        lambda _: {
            ("guide.pdf", 1): "supporting evidence for first page",
            ("guide.pdf", 2): "second page includes supporting evidence",
        },
    )

    candidates.validate_candidate_questions(
        candidates=(make_candidate("q1", "Question one?", (1, 2)),),
        existing_datasets=(),
        data_dir=Path("unused"),
    )


def test_duplicate_question_text_within_batch_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        candidates,
        "build_page_lookup",
        lambda _: {("guide.pdf", 1): "supporting evidence"},
    )

    with pytest.raises(ValueError, match="duplicate candidate question"):
        candidates.validate_candidate_questions(
            candidates=(
                make_candidate("q1", "What is routing?"),
                make_candidate("q2", " WHAT  IS  ROUTING? "),
            ),
            existing_datasets=(),
            data_dir=Path("unused"),
        )
