import json
from dataclasses import asdict
from pathlib import Path

from evaluation.models import(
    EvaluationMetrics,
    EvaluationRun,
    LatencyMetrics,
    QuestionResult,
    RetrievalConfig
)


def load_history(
    path: Path,
) -> tuple[EvaluationRun, ...]:
    if not path.exists():
        return()


    runs = []


    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        for line_number, line in enumerate(
            file,
            start=1,
        ):
            if not line.strip():
                continue

            try:
                raw_run = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid history JSON on line {line_number}."
                ) from exc

            runs.append(
                _parse_run(raw_run)
            )
            
    return tuple(runs)


def save_history(
    path: Path,
    runs: tuple[EvaluationRun, ...]
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        for run in runs:
            json.dump(
                asdict(run),
                file,
                ensure_ascii=False,
            )
            file.write("\n")

def append_run(
    path: Path,
    run: EvaluationRun,
    *,
    max_runs: int = 10,
) -> None:
    if (
        isinstance(max_runs,bool)
        or not isinstance(max_runs, int)
        or max_runs < 1
    ):
        raise ValueError(
            "max_runs must be a positive integer."
        )
    
    history = load_history(path)

    updated_history = (
        history + (run,)
    )[-max_runs:]

    save_history(
        path,
        updated_history,
    )


def _parse_run(
    raw_run: object,
) -> EvaluationRun:
    if not isinstance(raw_run, dict):
            
        raise ValueError(
            "Evaluation history entry must be an object."
        )

    try:
        raw_config = raw_run["retrieval_config"]
        raw_metrics = raw_run["metrics"]
        raw_questions = raw_run["questions"]
        raw_latency = raw_run.get("latency")
        if raw_latency is not None and not isinstance(raw_latency, dict):
            raise TypeError
        latency = (
            LatencyMetrics(**raw_latency)
            if raw_latency is not None
            else None
        )

        if not isinstance(raw_config, dict):
            raise TypeError

        if not isinstance(raw_metrics, dict):
            raise TypeError

        if not isinstance(raw_questions, list):
            raise TypeError

        return EvaluationRun(
            timestamp=raw_run["timestamp"],
            git_commit=raw_run["git_commit"],
            git_dirty=raw_run["git_dirty"],
            dataset_hash=raw_run["dataset_hash"],
            dataset=raw_run["dataset"],
            question_count=raw_run["question_count"],
            retrieval_config=RetrievalConfig(
                **raw_config
            ),
            metrics=EvaluationMetrics(
                **raw_metrics
            ),
            questions=tuple(
                QuestionResult(
                    **question
                )
                for question in raw_questions
            ),
            sample_seed=raw_run.get(
                "sample_seed"
            ),
            sample_size=raw_run.get(
                "sample_size"
            ),
            latency=latency,
        )
    except (
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        raise ValueError(
            "Invalid evaluation history entry."
        ) from exc
