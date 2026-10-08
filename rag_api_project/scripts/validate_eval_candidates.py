import argparse
from pathlib import Path

from evaluation.candidates import validate_candidate_questions
from evaluation.dataset import load_dataset


DEFAULT_DATASET_PATHS = (
    Path("eval/dev_questions.json"),
    Path("eval/random_questions.json"),
    Path("eval/test_questions.json"),
)


def load_existing_datasets(
    candidate_path: Path,
) -> tuple:
    resolved_candidate_path = candidate_path.resolve()

    return tuple(
        load_dataset(path)
        for path in DEFAULT_DATASET_PATHS
        if path.exists()
        and path.resolve() != resolved_candidate_path
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate proposed evaluation questions."
    )

    parser.add_argument(
        "candidate_path",
        type=Path,
        help="Path to a JSON file containing candidate questions.",
    )

    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Directory containing the source PDFs.",
    )

    args = parser.parse_args()

    candidates = load_dataset(args.candidate_path)

    existing_datasets = load_existing_datasets(
        args.candidate_path
    )

    validate_candidate_questions(
        candidates=candidates,
        existing_datasets=existing_datasets,
        data_dir=args.data_dir,
    )

    print(
        f"VALID: {len(candidates)} candidate(s)"
    )


if __name__ == "__main__":
    main()