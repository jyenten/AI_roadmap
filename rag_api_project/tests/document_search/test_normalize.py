from document_search.normalize import normalize_text


def test_normalize_text_nromalizes_case_and_whitespace() -> None:
    text = " Hello \n\t WORLD from PDF "

    assert normalize_text(text) == "hello world from pdf"


def test_nomalize_text_handles_empty_whitespace() -> None:
    assert normalize_text("  \n\t  ") == ""