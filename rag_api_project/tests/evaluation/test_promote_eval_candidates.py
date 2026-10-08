import json
import sys
from pathlib import Path

import pytest

from evaluation.dataset import load_dataset
from scripts import promote_eval_candidates as promote


def write_dataset(path: Path, items: list[dict]) -> None:
    path.write_text(
        json.dumps(items, indent=2) + "\n",
        encoding="utf-8",
    )


def make_question(question_id: str) -> dict:
    return {
        "id": question_id,
        "topic": "test-topic",
        "question": f"Question for {question_id}?",
        "gold_evidence": [
            {
                "source": "test.pdf",
                "pages": [1],
                "contains_any": ["test evidence"],
            }
        ],
    }


def test_select_candidates_returns_only_approved_ids() -> None:
    candidate_path = Path(
        "eval/candidates/random_batch_001.json"
    )
    candidates = load_dataset(candidate_path)

    selected = promote.select_candidates(
        candidates,
        {"rip_random_001", "ipv6_random_002"},
    )

    assert [question.id for question in selected] == [
        "rip_random_001",
        "ipv6_random_002",
    ]


def test_select_candidates_rejects_unknown_id() -> None:
    candidate_path = Path(
        "eval/candidates/random_batch_001.json"
    )
    candidates = load_dataset(candidate_path)

    with pytest.raises(ValueError):
        promote.select_candidates(
            candidates,
            {"does_not_exist"},
        )


def test_main_appends_approved_candidates_to_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    candidate_path = tmp_path / "candidates.json"
    target_path = tmp_path / "target.json"

    write_dataset(
        candidate_path,
        [
            make_question("candidate_001"),
            make_question("candidate_002"),
        ],
    )

    write_dataset(
        target_path,
        [
            make_question("existing_001"),
        ],
    )

    original_candidate_contents = candidate_path.read_text(
        encoding="utf-8"
    )

    monkeypatch.setattr(
        promote,
        "load_existing_datasets",
        lambda: (),
    )

    monkeypatch.setattr(
        promote,
        "validate_candidate_questions",
        lambda **kwargs: None,
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "promote_eval_candidates",
            str(candidate_path),
            str(target_path),
            "--ids",
            "candidate_002",
        ],
    )

    promote.main()

    target = load_dataset(target_path)

    assert [question.id for question in target] == [
        "existing_001",
        "candidate_002",
    ]

    assert (
        candidate_path.read_text(encoding="utf-8")
        == original_candidate_contents
    )