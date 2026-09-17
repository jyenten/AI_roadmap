from pathlib import Path

import pytest

from document_search.security import pdf_validation
from document_search.security.pdf_validation import (
    MAX_PDF_PAGES,
    validate_pdf_extension,
    validate_pdf_limits,
    validate_pdf_signature,
)

def test_validate_pdf_extension_accepts_pdf() -> None:
    validate_pdf_extension(Path("manual.PDF"))


def test_validate_pdf_extension_rejects_other_extension() -> None:
    with pytest.raises(ValueError, match="PDF extension"):
        validate_pdf_extension(Path("manual.txt"))


def test_validate_pdf_signature_accepts_pdf_header(
    tmp_path: Path,
) -> None:
    pdf_path = tmp_path / "manual.pdf"
    pdf_path.write_bytes(b"%PDF-1.7\nexample")

    validate_pdf_signature(pdf_path)


def test_validate_pdf_signature_rejects_invalid_file(
    tmp_path: Path,
) -> None:
    pdf_path = tmp_path / "manual.pdf"
    pdf_path.write_bytes(b"This is not a PDF")

    with pytest.raises(ValueError, match="PDF signature"):
        validate_pdf_signature(pdf_path)


def test_validate_pdf_limits_rejects_large_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pdf_path = tmp_path / "manual.pdf"
    pdf_path.write_bytes(b"%PDF-12345")

    monkeypatch.setattr(
        pdf_validation,
        "MAX_PDF_SIZE_BYTES",
        5,
    )

    with pytest.raises(ValueError, match="maximum file size"):
        validate_pdf_limits(pdf_path)


def test_validate_pdf_limits_rejects_too_many_pages(
    tmp_path: Path,
) -> None:
    pdf_path = tmp_path / "manual.pdf"
    pdf_path.write_bytes(b"%PDF-1.7")

    with pytest.raises(ValueError, match="maximum page count"):
        validate_pdf_limits(
            pdf_path,
            page_count=MAX_PDF_PAGES + 1,
        )