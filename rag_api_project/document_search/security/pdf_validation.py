from pathlib import Path

PDF_SIGNATURE = b"%PDF-"
PDF_HEADER_SCAN_BYTES = 1_024
MAX_PDF_SIZE_BYTES = 100*1024*1024
MAX_PDF_PAGES = 2_000


def validate_pdf_extension(pdf_path: Path) -> None:
    if pdf_path.suffix.casefold() != ".pdf":
        raise ValueError(
            f"File does not have a PDF extension: {pdf_path.name}"
        )


def validate_pdf_signature(pdf_path: Path) -> None:
    with pdf_path.open("rb") as file:
        header = file.read(PDF_HEADER_SCAN_BYTES)

    if PDF_SIGNATURE not in header:
        raise ValueError(
            f"File does not contain a valid PDF signature: {pdf_path.name}"
        )


def validate_pdf_limits (
    pdf_path: Path,
    *,
    page_count: int | None = None,
) -> None:
    file_size = pdf_path.stat().st_size

    if file_size > MAX_PDF_SIZE_BYTES:
        raise ValueError(
            f"PDF exceeds the maximum file size: {pdf_path.name}"
        )

    if page_count is not None and page_count > MAX_PDF_PAGES:
        raise ValueError(
            f"PDF exceeds the maximum page count: {pdf_path.name}"
        )