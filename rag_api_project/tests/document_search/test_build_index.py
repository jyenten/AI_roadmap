import pytest

from document_search.build_index import build_bm25_index
from document_search.models import PageDocument


def test_build_bm25_index_preserves_page_order() -> None:
    first_page = PageDocument(
        source="manual.pdf",
        page=1,
        text="OSPF interface cost.",
    )
    second_page = PageDocument(
        source="manual.pdf",
        page=2,
        text="Router hello packets."
    )

    index = build_bm25_index(
        [first_page, second_page]
    )

    assert index.pages == (
        first_page,
        second_page,
    )


def test_build_bm25_index_creates_score_for_each_page() -> None:
    pages = [
        PageDocument(
            source="manual.pdf",
            page=1,
            text="OSPF interface cost bandwidth"
        ),
        PageDocument(
            source="manual.pdf",
            page=2,
            text="Router hello dead interval."
        ),
    ]

    index = build_bm25_index(pages)

    scores = index.model.get_scores(
        ["ospf", "cost"]
    )

    assert len(scores) == len(index.pages)


def test_build_bm25_index_skips_pages_without_tokens() -> None:
    searchable_page = PageDocument(
            source="manual.pdf",
            page=1,
            text="OSPF interface cost.",
    )
    punctuation_page = PageDocument(
            source="manual.pdf",
            page=2,
            text="!!! --- ..."
    )

    index = build_bm25_index(
        [
            searchable_page,
            punctuation_page,
        ]
    )


    assert index.pages == (searchable_page,)


def test_build_bm25_index_rejects_empty_corpus() -> None:
    with pytest.raises(
        ValueError,
        match="without searchable pages",
    ):
        build_bm25_index([])


def test_build_bm25_index_rejects_corpus_without_tokens() -> None:
    page = PageDocument(
        source="manual.pdf",
        page=1,
        text="!!! --- ...",
    )

    with pytest.raises(
        ValueError,
        match="without searchable pages",
    ):
        build_bm25_index([page])