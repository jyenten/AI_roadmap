from rank_bm25 import BM25Okapi

from document_search.models import (
    BM25SearchIndex,
    PageDocument,
)
from document_search.tokenize import tokenize


def build_bm25_index(
    pages: list[PageDocument],
) -> BM25SearchIndex:
    indexed_pages: list[PageDocument] = []
    tokenized_corpus: list[list[str]] = []

    for page in pages:
        tokens = tokenize(page.text)

        if not tokens:
            continue

        indexed_pages.append(page)
        tokenized_corpus.append(tokens)

    if not indexed_pages:
        raise ValueError(
            "Cannot build BM25 index without searchable pages."
        )

    model = BM25Okapi(tokenized_corpus)

    return BM25SearchIndex(
        pages=tuple(indexed_pages),
        model=model,
    )