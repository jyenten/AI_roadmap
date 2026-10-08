import argparse
import json
from dataclasses import asdict
from pathlib import Path

from evaluation.candidates import validate_candidate_questions
from evaluation.dataset import load_dataset
from evaluation.models import EvaluationQuestion


DATASET_PATHS = (
    Path("eval/dev_questions.json"),
    Path("eval/random_questions.json"),
    Path("eval/test_questions.json"),
)


def load_existing_datasets() -> tuple[
    tuple[EvaluationQuestion, ...],
    ...
]:
    return tuple(
        load_dataset(path)
        for path in DATASET_PATHS
        if path.exists()
    )


def select_candidates(
    candidates: tuple[EvaluationQuestion, ...],
    approved_ids: set[str],
) -> tuple[EvaluationQuestion, ...]:
    selected = tuple(
        candidate
        for candidate in candidates
        if candidate.id in approved_ids
    )

    found_ids = {
        candidate.id
        for candidate in selected
    }

    missing_ids = approved_ids - found_ids

    if missing_ids:
        raise ValueError(
            "Unknown candidate IDs: "
            + ", ".join(sorted(missing_ids))
        )

    return selected


def save_dataset(
    path: Path,
    questions: tuple[EvaluationQuestion, ...],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            [
                asdict(question)
                for question in questions
            ],
            file,
            ensure_ascii=False,
            indent=2,
        )

        file.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Promote approved evaluation candidates "
            "into a dataset."
        )
    )

    parser.add_argument(
        "candidate_path",
        type=Path,
        help="JSON file containing proposed questions.",
    )

    parser.add_argument(
        "target_path",
        type=Path,
        help="Dataset to append approved questions to.",
    )

    parser.add_argument(
        "--ids",
        nargs="+",
        required=True,
        help="Candidates IDs explicitly approved for promotion. ",
    )

    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Directory containing source PDFs.",
    )

    args = parser.parse_args()

    candidates = load_dataset(
        args.candidate_path
    )

    approved = select_candidates(
        candidates,
        set(args.ids),
    )

    if not approved:
        raise ValueError(
            "No candidates selected for promotion."
        )

    existing_datasets = load_existing_datasets()

    validate_candidate_questions(
        candidates=approved,
        existing_datasets=existing_datasets,
        data_dir=args.data_dir,
    )

    current_target = (
        load_dataset(args.target_path)
        if args.target_path.exists()
        else ()
    )

    updated_target = (
        *current_target,
        *approved,
    )

    save_dataset(
    args.target_path,
    updated_target,
    )

    print(
        f"PROMOTED: {len(approved)} candidate(s)"
    )
    print(
        f"TARGET TOTAL: {len(updated_target)}"
    )


if __name__ == "__main__":
    main()