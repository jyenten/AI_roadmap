from document_search.tokenize import tokenize


def test_tokenize_returns_nromalized_worlds() -> None:
    text = "Hello, WORLD! File-name 123."

    assert tokenize(text) == [
        "hello",
        "world",
        "file",
        "name",
        "123",
    ]


def test_tokenize_normalizes_whitespace() -> None:
    text = "first\nsecond\tthird"

    assert tokenize(text) == [
        "first",
        "second",
        "third",
    ]


def test_tokenize_empty_text_returns_empty_list() -> None:
    assert tokenize("") == []