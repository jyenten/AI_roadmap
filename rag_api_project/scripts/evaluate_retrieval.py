import json
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime

from app.config import get_settings
from app.retrieval import Retriever
from scripts.eval_history import save_bounded_history


EVAL_PATH = Path("eval/dev_questions.json")
DEV_HISTORY_PATH = Path(
    "eval/results/dev_runs.jsonl"
)

def load_eval_questions(
    path: Path,
) -> list[dict]:
    with path.open(
        "r",
        encoding="utf-8",
    )as file:
        return json.load(file)


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


def get_file_sha256(
    path: Path,
) -> str:
    hasher = hashlib.sha256()

    with path.open(
        "rb"
    )as file:
        for chunk in iter(
            lambda: file.read(8192),
            b"",
        ):
            hasher.update(chunk)

    return hasher.hexdigest()


def main() -> None:
    questions = load_eval_questions(EVAL_PATH)

    settings = get_settings()


    retriever =  Retriever(settings)

    reciprocal_ranks: list[float] = []

    hit_at_1: list[int] = []
    hit_at_3: list[int] = []
    hit_at_5: list[int] = []
    hit_at_8: list[int] = []

    question_results: list[dict] = []

    for eval_item in questions:
        question = eval_item["question"]

        documents, distances, metadatas = retriever.search(
            question
        )
        print("=" * 80)
        print(f"ID: {eval_item['id']}")
        print(f"QUESTION: {question}")
        print()

        first_evidence_rank = None

        for rank, (document, distance, metadata) in enumerate(
            zip(documents, distances, metadatas),
            start=1,
        ):
            source = metadata.get("source")
            page = metadata.get("page")

            gold_evidence = eval_item["gold_evidence"]

            page_hit = any(
                source == gold["source"]
                and page in gold["pages"]
                for gold in gold_evidence
            )

            normalized_document = " ".join(
                document.lower().split()
            )

            evidence_hit = any(
                source == gold["source"]
                and page in gold["pages"]
                and any(
                    " ".join(fragment.lower().split())
                    in normalized_document
                    for fragment in gold["contains_any"]
                )
                for gold in gold_evidence
            )


            if evidence_hit and first_evidence_rank is None:
                first_evidence_rank = rank

            print(f"RANK {rank}: ")
            print(f"PAGE_HIT={page_hit} | ")
            print(f"EVIDENCE_HIT={evidence_hit}")
            print(f"distance={distance:.4f} | ")
            print(f"page={page} | ")
            print(f"source={source}")


        print()
        print(f"FIRST_EVIDENCE_RANK: {first_evidence_rank}")


        if first_evidence_rank is None:
            reciprocal_rank = 0.0
        else:
            reciprocal_rank = 1 / first_evidence_rank

        hit_at_1.append(
            int(
                first_evidence_rank is not None
                and first_evidence_rank <= 1
            )
        )

        hit_at_3.append(
            int(
                first_evidence_rank is not None
                and first_evidence_rank <= 3
            )
        )

        hit_at_5.append(
            int(
                first_evidence_rank is not None
                and first_evidence_rank <= 5
            )
        )

        hit_at_8.append(
            int(
                first_evidence_rank is not None
                and first_evidence_rank <= 8
            )
        )

        question_results.append(
            {
                "id": eval_item["id"],
                "first_evidence_rank": first_evidence_rank,
                "reciprocal_rank": reciprocal_rank,
            }
        )

        reciprocal_ranks.append(reciprocal_rank)

        print(f"RECIPROCAL_RANK: {reciprocal_rank:.4f}")


    mrr = (
        sum(reciprocal_ranks) / len(reciprocal_ranks)
        if reciprocal_ranks
        else 0.0
    )

    hit_1 = (
        sum(hit_at_1) / len(hit_at_1)
        if hit_at_1
        else 0.0
    )

    hit_3 = (
        sum(hit_at_3) / len(hit_at_3)
        if hit_at_3
        else 0.0
    )

    hit_5 = (
        sum(hit_at_5) / len(hit_at_5)
        if hit_at_5
        else 0.0
    )

    hit_8 = (
        sum(hit_at_8) / len(hit_at_8)
        if hit_at_8
        else 0.0
    )

    run_result = {
        "timestamp": datetime.now()
        .astimezone()
        .isoformat(timespec="seconds"),
        "git_commit": get_git_commit(),
        "git_dirty": get_git_dirty(),
        "dataset_hash": get_file_sha256(
            EVAL_PATH
        ),
        "dataset": "dev",
        "question_count": len(questions),
        "retrieval_config": {
            "collection_name": settings.collection_name,
            "embedding_model_name": settings.embedding_model_name,
            "retrieval_results": settings.retrieval_results,
        },
        "mrr": mrr,
        "hit_at_1": hit_1,
        "hit_at_3": hit_3,
        "hit_at_5": hit_5,
        "hit_at_8": hit_8,
        "questions": question_results,
    }

    save_bounded_history(
        DEV_HISTORY_PATH,
        run_result,
        max_runs=10,
    )

    print()
    print("=" * 80)
    print(f"MRR: {mrr:.4f}")

    print(f"HIT@1: {hit_1:.4f}")
    print(f"HIT@3: {hit_3:.4f}")
    print(f"HIT@5: {hit_5:.4f}")
    print(f"HIT@8: {hit_8:.4f}")

if __name__ == "__main__":
    main()