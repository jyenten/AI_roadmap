import pytest

from document_search.security.input_validation import (
    MAX_QUERY_LENGTH,
    MAX_TOP_K,
    validate_query,
    validate_top_k,
)


def test_validate_query_accepts_valid_query() -> None:
    query = "  OSPF interface cost  "

    assert validate_query(query) == query


def test_validate_query_rejects_empty_query() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        validate_query("    \n\t    ")


def test_validate_query_rejects_oversized_query() -> None:
    query = "X" * (MAX_QUERY_LENGTH + 1)

    with pytest.raises(ValueError, match="must not exceed"):
        validate_query(query)


def test_validate_top_k_accepts_valid_value() -> None:
    assert validate_top_k(10) == 10


def test_validate_top_k_rejects_zero() -> None:
    with pytest.raises(ValueError, match="between"):
        validate_top_k(0)


def test_validate_top_k_rejects_value_above_limit() -> None:
    with pytest.raises(ValueError, match="between"):
        validate_top_k(MAX_TOP_K + 1)


def test_validate_top_k_rejects_boolean() -> None:
    with pytest.raises(TypeError, match="integer"):
        validate_top_k(True)