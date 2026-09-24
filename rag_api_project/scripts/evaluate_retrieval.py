import subprocess
from pathlib import Path

from app.config import get_settings
from app.retrieval import Retriever
from evaluation.dataset import (
    calculate_dataset_hash,
    load_dataset,
)
from evaluation.history import append_run
from evaluation.models import RetrievalConfig
from evaluation.runner import evaluate_dataset


EVAL_PATH = Path("eval/dev_questions.json")
DEV_HISTORY_PATH = Path(
    "eval/results/dev_runs.jsonl"
)


def get_git_commit() -> str:
    try:
        return subprocess.check_output(
            [
                "git",
                "rev-parse",
                "HEAD",
            ],
            text=True,
        ).strip()
    except subprocess.CalledProcessError:
        return "unknown"


def get_git_dirty() -> bool:
    try:
        status = subprocess.check_output(
            [
                "git",
                "status",
                "--porcelain",
            ],
            text=True,
        ).strip()

        return bool(status)
    except subprocess.CalledProcessError:
        return False


def main() -> None:
    questions = load_dataset(
        EVAL_PATH
    )

    settings = get_settings()

    retriever = Retriever(
        settings
    )

    retrieval_config = RetrievalConfig(
        collection_name=settings.collection_name,
        embedding_model_name=settings.embedding_model_name,
        retrieval_results=settings.retrieval_results,
    )

    run = evaluate_dataset(
        questions,
        retriever,
        dataset="dev",
        dataset_hash=calculate_dataset_hash(
            EVAL_PATH
        ),
        retrieval_config=retrieval_config,
        git_commit=get_git_commit(),
        git_dirty=get_git_dirty(),
    )

    append_run(
        DEV_HISTORY_PATH,
        run,
        max_runs=10,
    )

    for question, result in zip(
        questions,
        run.questions,
        strict=True,
    ):
        print("=" * 80)
        print(f"ID: {question.id}")
        print(
            f"QUESTION: {question.question}"
        )
        print(
            "FIRST_EVIDENCE_RANK: "
            f"{result.first_evidence_rank}"
        )
        print(
            "RECIPROCAL_RANK: "
            f"{result.reciprocal_rank:.4f}"
        )

    print()
    print("=" * 80)
    print(
        f"MRR: {run.metrics.mrr:.4f}"
    )
    print(
        f"HIT@1: {run.metrics.hit_at_1:.4f}"
    )
    print(
        f"HIT@3: {run.metrics.hit_at_3:.4f}"
    )
    print(
        f"HIT@5: {run.metrics.hit_at_5:.4f}"
    )
    print(
        f"HIT@8: {run.metrics.hit_at_8:.4f}"
    )


if __name__ == "__main__":
    main()
