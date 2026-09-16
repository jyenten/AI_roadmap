MAX_QUERY_LENGTH = 1_000
MAX_TOP_K = 100


def validate_query(query: str) -> str:
    if not query.strip():
        raise ValueError("Query must not be empty.")

    if len(query) > MAX_QUERY_LENGTH:
        raise ValueError(
            f"Query must not exceed {MAX_QUERY_LENGTH} characters."
        )

    return query


def validate_top_k(top_k: int) -> int:
    if isinstance(top_k, bool) or not isinstance(top_k, int):
        raise TypeError("top_k must be an integer.")

    if not 1 <= top_k <= MAX_TOP_K:
        raise ValueError(
            f"top_k must be between 1 and {MAX_TOP_K}."
        )

    return top_k