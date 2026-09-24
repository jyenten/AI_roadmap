import json

import pytest

from evaluation.history import (
    append_run,
    load_history,
    save_history,
)
from evaluation.models import (
    EvaluationMetrics,
    EvaluationRun,
    QuestionResult,
    RetrievalConfig,
)


def build_run(
    timestamp: str,
) -> EvaluationRun:
    return EvaluationRun(
        timestamp=timestamp,
        git_commit="abc123",
        git_dirty=False,
        dataset_hash="hash123",
        dataset="dev",
        question_count=1,
        retrieval_config=RetrievalConfig(
            collection_name="ospf",
            embedding_model_name="model",
            retrieval_results=8,
        ),
        metrics=EvaluationMetrics(
            mrr=1.0,
            hit_at_1=1.0,
            hit_at_3=1.0,
            hit_at_5=1.0,
            hit_at_8=1.0,
        ),
        questions=(
            QuestionResult(
                id="dev_001",
                first_evidence_rank=1,
                reciprocal_rank=1.0,
            ),
        ),
    )


def test_history_round_trip(
    tmp_path,
) -> None:
    path = tmp_path / "results" / "runs.jsonl"

    run = build_run(
        "2026-09-23T10:00:00+02:00"
    )

    save_history(
        path,
        (run,),
    )

    loaded = load_history(path)

    assert loaded == (run,)
    assert isinstance(
        loaded[0].retrieval_config,
        RetrievalConfig,
    )
    assert isinstance(
        loaded[0].questions[0],
        QuestionResult,
    )


def test_append_run_keeps_bounded_history(
    tmp_path,
) -> None:
    path = tmp_path / "runs.jsonl"

    for hour in range(4):
        append_run(
            path,
            build_run(
                f"2026-09-23T{hour:02d}:00:00+02:00"
            ),
            max_runs=2,
        )

    history = load_history(path)

    assert len(history) == 2
    assert history[0].timestamp == (
        "2026-09-23T02:00:00+02:00"
    )
    assert history[1].timestamp == (
        "2026-09-23T03:00:00+02:00"
    )


def test_load_history_rejects_invalid_json(
    tmp_path,
) -> None:
    path = tmp_path / "runs.jsonl"

    save_history(
        path,
        (
            build_run(
                "2026-09-23T10:00:00+02:00"
            ),
        ),
    )

    with path.open(
        "a",
        encoding="utf-8",
    ) as file:
        file.write(
            "{invalid json}\n"
        )

    with pytest.raises(
        ValueError,
        match="line 2",
    ):
        load_history(path)