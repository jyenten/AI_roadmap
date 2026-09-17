from document_search.models import (
    BM25SearchIndex,
    SearchResult,
)
from document_search.security.input_validation import (
    validate_query,
    validate_top_k,
)
from document_search.tokenize import tokenize


def search_pages(
    index: BM25SearchIndex,
    query: str,
    top_k: int = 10,
) -> list[SearchResult]:
    validated_query = validate_query(query)
    validated_top_k = validate_top_k(top_k)

    query_tokens = tokenize(validated_query)

    if not query_tokens:
        raise ValueError(
            "Query must contain searchable tokens."
        )

    scores = index.model.get_scores(query_tokens)

    if len(scores) != len(index.pages):
        raise RuntimeError(
            "BM25 score count does not match indexed pages."
        )

    results = [
        SearchResult(
            document=page,
            score=float(score),
        )
        for page, score in zip(
            index.pages,
            scores,
            strict=True,
        )
    ]

    return sorted(
        results,
        key=lambda result: result.score,
        reverse=True,
    )[:validated_top_k]