from pathlib import Path


def validate_data_directory(data_dir: Path) -> Path:
    try:
        resolved = data_dir.resolve(strict=True)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Data directory does not exist: {data_dir}"
        ) from exc

    if not resolved.is_dir():
        raise NotADirectoryError(
            f"Data path is not a directory: {data_dir}"
        )

    return resolved


def resolve_safe_path(
    base_dir: Path,
    candidate: Path | str,
) -> Path:
    base = validate_data_directory(base_dir)

    candidate_path = Path(candidate)

    if candidate_path.is_absolute():
        resolved = candidate_path.resolve()
    else:
        resolved = (base / candidate_path).resolve()

    try:
        resolved.relative_to(base)
    except ValueError as exc:
        raise ValueError(
            f"Path escapes the allowed directory: {candidate}"
        ) from exc

    return resolved