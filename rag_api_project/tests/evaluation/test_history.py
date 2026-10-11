import json
from dataclasses import asdict, replace

import pytest

from evaluation.history import (
    append_run,
    load_history,
    save_history,
)
from evaluation.models import (
    EvaluationMetrics,
    EvaluationRun,
    LatencyMetrics,
    QuestionResult,
    RetrievalConfig,
)


def build_run(
    timestamp: str,
    *,
    sample_seed: int | None = None,
    sample_size: int | None = None,
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
        sample_seed=sample_seed,
        sample_size=sample_size,
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


def test_history_preserves_random_metadata(
    tmp_path,
) -> None:
    path = tmp_path / "random_runs.jsonl"

    run = build_run(
        "2026-09-29T18:00:00+02:00",
        sample_seed=42,
        sample_size=5,
    )

    save_history(
        path,
        (run,),
    )

    loaded = load_history(path)

    assert loaded[0].sample_seed == 42
    assert loaded[0].sample_size == 5


@pytest.mark.parametrize("include_null", [False, True])
def test_historical_history_without_latency(tmp_path, include_null):
    run = build_run("old", sample_seed=42, sample_size=5)
    raw = asdict(run)
    if not include_null:
        raw.pop("latency")
    path = tmp_path / "runs.jsonl"
    path.write_text(json.dumps(raw) + "\n", encoding="utf-8")
    assert load_history(path) == (run,)


def test_append_preserves_old_and_new_history(tmp_path):
    path = tmp_path / "runs.jsonl"
    old = build_run("old", sample_seed=42, sample_size=5)
    raw = asdict(old)
    raw.pop("latency")
    measured = replace(build_run("measured"), latency=LatencyMetrics(2, 1, 3))
    path.write_text(
        json.dumps(raw) + "\n" + json.dumps(asdict(measured)) + "\n",
        encoding="utf-8",
    )
    loaded = load_history(path)
    assert loaded == (old, measured)
    assert isinstance(loaded[1].latency, LatencyMetrics)
    added = replace(build_run("new"), latency=LatencyMetrics(4, 3, 5))
    append_run(path, added)
    assert load_history(path) == (old, measured, added)
    assert json.loads(path.read_text(encoding="utf-8").splitlines()[1])["latency"] == asdict(measured.latency)


@pytest.mark.parametrize("latency", [
    [], "invalid", 1, {}, {"mean_ms": 1, "p50_ms": 1},
    {"mean_ms": 1, "p50_ms": 2, "p95_ms": 1},
    {"mean_ms": -1, "p50_ms": 1, "p95_ms": 2},
    {"mean_ms": float("nan"), "p50_ms": 1, "p95_ms": 2},
    {"mean_ms": 1, "p50_ms": 1, "p95_ms": float("inf")},
    {"mean_ms": "1", "p50_ms": 1, "p95_ms": 2},
    {"mean_ms": 1, "p50_ms": 1, "p95_ms": 2, "extra": 0},
])
def test_history_rejects_malformed_latency_without_overwriting(tmp_path, latency):
    path = tmp_path / "runs.jsonl"
    raw = asdict(build_run("invalid"))
    raw["latency"] = latency
    contents = json.dumps(raw) + "\n"
    path.write_text(contents, encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid evaluation history entry"):
        load_history(path)
    with pytest.raises(ValueError):
        append_run(path, build_run("new"))
    assert path.read_text(encoding="utf-8") == contents
