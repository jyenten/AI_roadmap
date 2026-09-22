import json
from pathlib import Path

import pytest

from evaluation.dataset import (
    calculate_dataset_hash,
    load_dataset,
)
from evaluation.models import EvaluationQuestion


def write_dataset(
    path: Path,
    questions: list[dict],
) -> None:
    path.write_text(
        json.dumps(questions),
        encoding="utf-8",
    )


def test_load_dataset_returns_typed_questions(
    tmp_path: Path,
) -> None:
    dataset_path = tmp_path / "dev.json"

    write_dataset(
        dataset_path,
        [
            {
                "id": "dev_001",
                "topic": "cost",
                "question": "How is cot calculated?",
                "gold_evidence": [
                    {
                        "source": "manual.pdf",
                        "pages": [26],
                        "contains_any": [
                            "reference bandwidth",
                        ],
                    }
                ],
            }
        ],
    )

    questions = load_dataset(dataset_path)

    assert len(questions) == 1
    assert isinstance(
        questions[0],
        EvaluationQuestion,
    )
    assert questions[0].gold_evidence[0].pages == (26,)


def test_load_dataset_rejects_duplicate_ids(
    tmp_path: Path,
) -> None:
    dataset_path = tmp_path / "dev.json"

    question = {
        "id": "dev_001",
        "topic": "cost",
        "question": "How is cost calcualted?",
        "gold_evidence": [
            {
                "source": "manual.pdf",
                "pages": [26],
                "contains_any": [
                    "reference bandwidth",
                ],
            }
        ],
    }

    write_dataset(
        dataset_path,
        [
            question,
            question,
        ],
    )

    with pytest.raises(
        ValueError,
        match="IDs must be unique",
    ):
        load_dataset(dataset_path)


def test_dataset_hash_changes_with_content(
    tmp_path: Path,
) -> None:
    dataset_path = tmp_path / "dev.json"

    dataset_path.write_text(
        "first",
        encoding="utf-8"
    )
    first_hash = calculate_dataset_hash(
        dataset_path
    )

    dataset_path.write_text(
        "second",
        encoding="utf-8",
    )
    second_hash = calculate_dataset_hash(
        dataset_path
    )

    assert first_hash != second_hash