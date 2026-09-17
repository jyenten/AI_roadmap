import pytest

from document_search.build_index import build_bm25_index
from document_search.models import PageDocument
from document_search.search import search_pages


def build_test_index():
    return build_bm25_index(
        [
            PageDocument(
                source="manual.pdf",
                page=1,
                text="OSPF interface cost bandwidth.",
            ),
            PageDocument(
                source="manual.pdf",
                page=2,
                text="DHCP address pool lease.",
            ),
            PageDocument(
                source="manual.pdf",
                page=3,
                text="Spanning tree VLAN switch.",
            ),
        ]
    )


def test_search_pages_ranks_relevant_page_first() -> None:
    index = build_test_index()

    results = search_pages(
        index,
        "OSPF interface cost",
        top_k=3,
    )

    assert results[0].document.page == 1


def test_search_pages_respects_top_k() -> None:
    index = build_test_index()

    results = search_pages(
        index,
        "OSPF",
        top_k=2,
    )

    assert len(results) == 2


def test_search_pages_rejects_unsearchable_query() -> None:
    index = build_test_index()

    with pytest.raises(ValueError):
        search_pages(
            index,
            "!!! --- ...",
        )