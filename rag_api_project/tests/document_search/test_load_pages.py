from pathlib import Path

import pytest
from pypdf.errors import PdfReadError

import document_search.load_pages as load_pages_module
from document_search.load_pages import load_pdf_pages


class FakePage:
    def __init__(
        self,
        text: str | None,
    ) -> None:
        self.text = text

    def extract_text(self) -> str | None:
        return self.text


class FakeReader:
    def __init__(
        self,
        pdf_path: Path,
    ) -> None:
        self.is_encrypted = False
        self.pages = [
            FakePage("First page."),
            FakePage("  "),
            FakePage("Third page."),
        ]


def test_load_pdf_pages_creates_page_documents(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    pdf_path = data_dir / "manual.pdf"
    pdf_path.write_bytes(b"%PDF-1.7\n")

    monkeypatch.setattr(
        load_pages_module,
        "PdfReader",
        FakeReader,
    )

    pages = load_pdf_pages(data_dir)

    assert len(pages) == 2

    assert pages[0].source == "manual.pdf"
    assert pages[0].page == 1
    assert pages[0].text == "First page."

    assert pages[1].source == "manual.pdf"
    assert pages[1].page == 3
    assert pages[1].text == "Third page."


def test_load_pdf_pages_uses_deterministic_file_order(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    (data_dir / "b.pdf").write_bytes(b"%PDF-1.7\n")
    (data_dir / "a.pdf").write_bytes(b"%PDF-1.7\n")


    class FilenameReader:
        def __init__(
            self,
            pdf_path: Path,
        ) -> None:
            self.is_encrypted = False
            self.pages = [
                FakePage(pdf_path.name),
            ]

    monkeypatch.setattr(
        load_pages_module,
        "PdfReader",
        FilenameReader,
    )

    pages = load_pdf_pages(data_dir)

    assert [page.source for page in pages] == [
        "a.pdf",
        "b.pdf",
    ]


def test_load_pdf_pages_rejects_unreadable_pdf(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    pdf_path = data_dir / "broken.pdf"
    pdf_path.write_bytes(b"%PDF-1.7\n")

    class BrokenReader:
        def __init__(
            self,
            pdf_path: Path,
        ) -> None:
            raise PdfReadError("Broken PDF")

    monkeypatch.setattr(
        load_pages_module,
        "PdfReader",
        BrokenReader,
    )

    with pytest.raises(ValueError, match="Could not read PDF"):
        load_pdf_pages(data_dir)


def test_load_pdf_pages_rejects_encrypted_pdf(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    pdf_path = data_dir / "encrypted.pdf"
    pdf_path.write_bytes(b"%PDF-1.7\n")

    class EncryptedReader:
        def __init__(
            self,
            pdf_path: Path,
        ) -> None:
            self.is_encrypted = True
            self.pages = []

    monkeypatch.setattr(
        load_pages_module,
        "PdfReader",
        EncryptedReader,
    )

    with pytest.raises(ValueError, match="Encrypted PDF"):
        load_pdf_pages(data_dir)