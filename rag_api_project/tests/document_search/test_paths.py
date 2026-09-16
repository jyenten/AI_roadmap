from pathlib import Path

import pytest

from document_search.security.paths import (
    resolve_safe_path,
    validate_data_directory,
)


def test_validate_data_directory_returns_resolved_directory(
        tmp_path: Path,
) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    assert validate_data_directory(data_dir) == data_dir.resolve()


def test_validate_data_directory_rejects_missing_directory(
    tmp_path: Path,
) -> None:
    missing = tmp_path / "missing"

    with pytest.raises(FileNotFoundError, match="does not exist"):
        validate_data_directory(missing)


def test_validate_data_directory_rejects_file(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "manual.pdf"
    file_path.write_text("not a directory")

    with pytest.raises(NotADirectoryError, match="not a directory"):
        validate_data_directory(file_path)


def test_resolve_safe_path_accepts_path_inside_directory(
    tmp_path: Path,
) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    expected = data_dir / "manual.pdf"

    assert resolve_safe_path(
        data_dir,
        "manual.pdf",
    ) == expected.resolve()


def test_resolve_safe_path_rejects_path_traversal(
    tmp_path: Path,
) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    with pytest.raises(ValueError, match="escapes"):
        resolve_safe_path(
            data_dir,
            "../secret.txt",
        )


def test_resolve_safe_path_rejects_symlink_escape(
    tmp_path: Path,
) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()

    link = data_dir / "outside-link"

    try:
        link.symlink_to(
            outside_dir,
            target_is_directory=True,
        )
    except OSError:
        pytest.skip(
            "Creating symbolic links is not permitted on this system."
        )

    with pytest.raises(ValueError, match="escapes"):
        resolve_safe_path(
            data_dir,
            link / "manual.pdf",
        )