from dataclasses import FrozenInstanceError

import pytest

from document_search.models import (
    BM25SearchIndex,
    PageDocument,
    SearchResult,
)


def test_page_document_stores_source_data() -> None:
    document = PageDocument(
        source="manual.pdf",
        page=26,
        text="OSPF calculates interface cost.",
    )

    assert document.source == "manual.pdf"
    assert document.page == 26
    assert document.text == "OSPF calculates interface cost."


def test_page_document_is_imutable() -> None:
    document = PageDocument(
        source="maunual.pdf",
        page=26,
        text="Ecample text.",
    )

    with pytest.raises(FrozenInstanceError):
        document.page = 27





def test_search_result_references_document() -> None:
    document = PageDocument(
        source="manual.pdf",
        page=26,
        text="Ecample text.",
    )

    result = SearchResult(
        document=document,
        score=12.5,
    )

    assert result.document is document
    assert result.score == 12.5



def  test_bm25_search_index_keeps_page_order() -> None:
    first_page = PageDocument(
        source="manual.pdf",
        page=1,
        text="First page.",
    )
    second_page = PageDocument(
        source="manual.pdf",
        page=2,
        text="Second page.",
    )
    model = object()

    index = BM25SearchIndex(
        pages=(first_page,second_page),
        model=model,
    )

    assert index.pages == (first_page,second_page)
    assert index.model is model