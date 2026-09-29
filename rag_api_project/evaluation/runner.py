from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Protocol

from evaluation.evidence import find_gold_rank
from evaluation.metrics import (
    aggregate_metrics,
    reciprocal_rank,
)

from evaluation.models import (
    EvaluationQuestion,
    EvaluationRun,
    QuestionResult,
    RetrievalConfig,
)


class RetrieverLike(Protocol):
    def search(
        self,
        query: str,
    ) -> tuple[
        Sequence[str],
        Sequence[float],
        Sequence[Mapping[str, object]],
    ]:
        ...


def evaluate_question(
    question: EvaluationQuestion,
    retriever: RetrieverLike,
) -> QuestionResult:
    documents, distances, metadatas = retriever.search(
        question.question
    )

    if not(
        len(documents)
        == len(distances)
        == len(metadatas)
    ):
        raise RuntimeError(
            "Retriever returned inconsistent result lengths."
        )

    ranked_results = (
        (
            document,
            _get_source(metadata),
            _get_page(metadata),
        )
        for document, metadata in zip(
            documents,
            metadatas,
            strict=True,
        )
    )

    first_evidence_rank = find_gold_rank(
        ranked_results,
        question.gold_evidence,
    )

    return QuestionResult(
        id=question.id,
        first_evidence_rank=first_evidence_rank,
        reciprocal_rank=reciprocal_rank(
            first_evidence_rank
        ),
    )


def evaluate_dataset(
    questions: Sequence[EvaluationQuestion],
    retriever: RetrieverLike,
    *,
    dataset: str,
    dataset_hash: str,
    retrieval_config: RetrievalConfig,
    git_commit: str,
    git_dirty: bool,
    timestamp: str | None = None,
    sample_seed: int | None = None,
    sample_size: int | None = None,
) -> EvaluationRun:
    question_results = tuple(
        evaluate_question(
            question,
            retriever,
        )
        for question in questions
    )

    metrics = aggregate_metrics(
        result.first_evidence_rank
        for result in question_results
    )

    return EvaluationRun(
        timestamp=(
            timestamp
            or datetime.now()
            .astimezone()
            .isoformat(timespec="seconds")
        ),
        git_commit=git_commit,
        git_dirty=git_dirty,
        dataset_hash=dataset_hash,
        dataset=dataset,
        question_count=len(questions),
        retrieval_config=retrieval_config,
        metrics=metrics,
        questions=question_results,
        sample_seed=sample_seed,
        sample_size=sample_size,
    )


def _get_source(
    metadata: Mapping[str, object],
) -> str | None:
    source = metadata.get("source")

    if isinstance(source, str):
        return source

    return None


def _get_page(
    metadata: Mapping[str, object],
) -> int | None:
    page = metadata.get("page")

    if (
        isinstance(page, int)
        and not isinstance(page, bool)
    ):
        return page

    return None