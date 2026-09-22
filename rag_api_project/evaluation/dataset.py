import hashlib
import json
from pathlib import Path

from evaluation.models import (
    EvaluationQuestion,
    GoldEvidence,
)


def load_dataset(
    path: Path,
) -> tuple[EvaluationQuestion, ...]:
    try:
        with path.open(
            "r",
            encoding="utf=8",
        ) as file:
            raw_data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in evaluation dataset: {path}"
        ) from exc

    return validate_dataset(raw_data)


def validate_dataset(
    raw_data: object,
) -> tuple[EvaluationQuestion, ...]:
    if not isinstance(raw_data, list):
        raise ValueError(
            "Evaluation dataset must be a JSON list."
        )

    if not raw_data:
        raise ValueError(
            "Evaluation dataset must not be empty."
        )
    questions = tuple(
        _parse_question(item)
        for item in raw_data
    )

    question_ids = [
        question.id
        for question in questions
    ]

    if len(question_ids) != len(set(question_ids)):
        raise ValueError(
            "Evaluation question IDs must be unique."
        )

    return questions


def calculate_dataset_hash(
        path: Path,
) -> str:
    with path.open("rb") as file:
        return hashlib.file_digest(
            file,
            "sha256",
        ).hexdigest()


def _parse_question(
    raw_question: object,
) -> EvaluationQuestion:
    if not isinstance(raw_question, dict):
        raise ValueError(
            "Each evaluation question must be a JSON object."
        )

    question_id = _require_text(
        raw_question.get("id"),
        "id",
    )
    topic = _require_text(
        raw_question.get("topic"),
        "topic",
    )
    question = _require_text(
        raw_question.get("question"),
        "question",
    )

    raw_evidence = raw_question.get("gold_evidence")

    if not isinstance(raw_evidence, list) or not raw_evidence:
        raise ValueError(
            f"Question {question_id!r} must contain gold evidence"
        )

    gold_evidence = tuple(
        _parse_gold_evidence(item)
        for item in raw_evidence
    )

    return EvaluationQuestion(
        id=question_id,
        topic=topic,
        question=question,
        gold_evidence=gold_evidence,
    )


def _parse_gold_evidence(
    raw_evidence: object,
) -> GoldEvidence:
    if not isinstance(raw_evidence, dict):
        raise ValueError(
            "Gold evidence must be a JSON object."
        )

    source = _require_text(
        raw_evidence.get("source"),
        "source",
    )

    raw_pages = raw_evidence.get("pages")

    if not isinstance(raw_pages, list) or not raw_pages:
        raise ValueError(
            "Gold evidence must contain pages."
        )

    pages = tuple(
        page
        for page in raw_pages
        if isinstance(page, int)
        and not isinstance(page, bool)
        and page > 0
    )

    if len(pages) != len(raw_pages):
        raise ValueError(
            "Gold evidence pages must be positive integers."
        )

    raw_fragments = raw_evidence.get("contains_any")

    if not isinstance(raw_fragments, list) or not raw_fragments:
        raise ValueError(
            "Gold evidence must contain text fragments."
        )

    contains_any = tuple(
        _require_text(
            fragment,
            "contains_any,"
        )
        for fragment in raw_fragments
    )

    return GoldEvidence(
        source=source,
        pages=pages,
        contains_any=contains_any,
    )


def _require_text(
    value: object,
    field_name: str,
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"{field_name} must be a non-empty string."
        )

    return value