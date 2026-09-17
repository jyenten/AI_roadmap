from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from document_search.models import PageDocument
from document_search.security.paths import (
    resolve_safe_path,
    validate_data_directory,
)
from document_search.security.pdf_validation import (
    validate_pdf_extension,
    validate_pdf_limits,
    validate_pdf_signature,
)


def load_pdf_pages(data_dir: Path) -> list[PageDocument]:
    base_dir = validate_data_directory(data_dir)

    pdf_paths = sorted(
        (
            path
            for path in base_dir.iterdir()
            if path.is_file()
            and path.suffix.casefold() == ".pdf"
        ),
        key=lambda path: path.name.casefold(),
    )

    pages: list[PageDocument] = []

    for candidate in pdf_paths:
        pdf_path = resolve_safe_path(
            base_dir,
            candidate,
        )

        validate_pdf_extension(pdf_path)
        validate_pdf_signature(pdf_path)
        validate_pdf_limits(pdf_path)

        try:
            reader = PdfReader(pdf_path)
        except PdfReadError as exc:
            raise ValueError(
                f"Could not read PDF: {candidate.name}"
            ) from exc

        if reader.is_encrypted:
            raise ValueError(
                f"Encrypted PDF is not supported: {candidate.name}"
            )

        validate_pdf_limits(
            pdf_path,
            page_count=len(reader.pages),
        )

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):
            try:
                text = page.extract_text() or ""
            except PdfReadError as exc:
                raise ValueError(
                    f"Could not extract page {page_number}"
                    f"from PDF: {candidate.name}"
                ) from exc
            if not text.strip():
                continue

            pages.append(
                PageDocument(
                    source=candidate.name,
                    page=page_number,
                    text=text,
                )
            )

    return pages