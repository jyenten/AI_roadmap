import argparse
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
from evaluation.random_eval import sample_questions
from evaluation.runner import evaluate_dataset


RANDOM_EVAL_PATH = Path(
    "eval/random_questions.json"
)

RANDOM_HISTORY_PATH = Path(
    "eval/restults/ranomd_runs.jsonl"
)

DEFAULT_SAMPLE_SIZE = 10
DEFAULT_SEED = 42


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run reproducible RANDOM retrieval evaluation."
        )
    )

    parser.add_argument(
        "--sample-size",
        type=int,
        default=DEFAULT_SAMPLE_SIZE,
        help="Number of questions to sample."
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help="Random seed used for sampling.",
    )

    return parser


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
                "-- procelain",
            ],
            text=True,
        ).strip()

        return bool(status)
    except subprocess.CalledProcessError:
        return False


def main() -> None:
    args = build_parser().parse_args()

    question_pool = load_dataset(
        RANDOM_EVAL_PATH
    )

    questions = sample_questions(
        question_pool,
        sample_size=args.sample_size,
        seed=args.seed,
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
        dataset="random",
        dataset_hash=calculate_dataset_hash(
            RANDOM_EVAL_PATH
        ),
        retrieval_config=retrieval_config,
        git_commit=get_git_commit(),
        git_dirty=get_git_dirty(),
        sample_seed=args.seed,
        sample_size=args.sample_size,
    )

    append_run(
        RANDOM_HISTORY_PATH,
        run,
        max_runs=10,
    )

    print("=" * 80)
    print("RANDOM RETRIEVAL EVALUATION")
    print(
        f"SEED: {run.sample_seed}"
    )
    print(
        f"SAMPLE_SIZE: {run.sample_size}"
    )
    print()

    for question, result in zip(
        questions,
        run.questions,
        strict=True,
    ):
        print(
            f"{question.id}: "
            f"rank={result.first_evidence_rank}"
        )

    print()
    print(f"MRR: {run.metrics.mrr:.4f}")
    print(
        f"HIT@1: {run.metrics.hit_at_1:.4f}"
    )
    print(
        f"HIT@2: {run.metrics.hit_at_2:.4f}"
    )
    print(
        f"HIT@3: {run.metrics.hit_at_3:.4f}"
    )
    print(
        f"HIT@4: {run.metrics.hit_at_4:.4f}"
    )


if __name__ == "__main__":
    main()