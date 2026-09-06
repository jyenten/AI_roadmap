import pytest

from scripts.ingest import (
    clean_pdf_text,
    split_long_text,
    split_text,
    protect_urls,
    restore_technical_tokens,
)


def test_clean_pdf_text_preserves_ip_addresses():
    text = "network 10.1.1.1 255.240.0.0 area 20"

    cleaned = clean_pdf_text(text)

    assert "10.1.1.1" in cleaned
    assert "255.240.0.0" in cleaned


def test_clean_pdf_text_preserves_urls():
    text = "Documentation is available at www.cisco.com"

    cleaned = clean_pdf_text(text)

    assert "www.cisco.com" in cleaned


def test_clean_pdf_text_separates_joined_sentences():
    text = "First sentence.Second sentence."

    cleaned = clean_pdf_text(text)

    assert cleaned == "First sentence. Second sentence."


def test_split_text_uses_overlap():
    text = (
        "Alpha sentence contains several useful words. "
        "Bravo sentence contains some additional information. "
        "Charlie sentence continues with another relevant fact. "
        "Delta sentence finishes the example."
    )

    chunks = split_text(
        text,
        chunk_size=100,
        overlap=35,
    )

    assert len(chunks) >= 2
    assert "some additional information." in chunks[1]


def test_split_text_respects_chunks_size():
    text = " ".join(
        f"word{i:02d}"
        for i in range(40)
    )

    chunk_size = 100

    chunks = split_text(
        text,
        chunk_size=chunk_size,
        overlap=30,
    )

    assert all(
        len(chunk) <= chunk_size
        for chunk in chunks
    )


def test_split_long_text_allows_zero_overlap():
    text = " ".join(
        f"word{i:02d}"
        for i in range(30)
    )

    chunks = split_long_text(
        text,
        chunk_size=100,
        overlap=0,
    )

    assert len(chunks) >= 2


def test_split_long_text_rejects_overlap_equal_to_chunk_size():
    text = "word " * 30

    with pytest.raises(ValueError):
        split_long_text(
            text,
            chunk_size=100,
            overlap=100,
        )


def test_split_text_rejects_overlap_equal_to_chunk_size():
    text = "short text"

    with pytest.raises(ValueError):
        split_text(
            text,
            chunk_size=100,
            overlap=100,
        )


def test_clean_pdf_text_preserves_url_query_strings():
    text = "See https://www.cisco.com/search?q=ospf"

    cleaned = clean_pdf_text(text)

    assert "https://www.cisco.com/search?q=ospf" in cleaned


def test_clean_pdf_text_separates_sentences_after_question_mark():
    text = "What happened?Next sentence."

    cleaned = clean_pdf_text(text)

    assert cleaned == "What happened? Next sentence."


def test_clean_pdf_text_preserves_url_query_strings_with_uppercase_keys():
    text = "See https://example.com/search?Query=ospf"

    cleaned = clean_pdf_text(text)

    assert "https://example.com/search?Query=ospf" in cleaned


def test_protect_urls_replaces_url_with_placeholder():
    text = "See https://example.com/search?Query=ospf for details."

    protected_text, replacements = protect_urls(text)

    assert protected_text == "See __URL_0__ for details."

    assert replacements == {
        "__URL_0__": "https://example.com/search?Query=ospf"
    }


def test_restore_technical_tokens_restores_placeholder():
    text = "See __URL_0__ for details."

    replacements = {
        "__URL_0__": "https://example.com/search?Query=ospf"
    }

    restored_text = restore_technical_tokens(
        text,
        replacements,
    )

    assert restored_text == (
        "See https://example.com/search?Query=ospf for details."
    )