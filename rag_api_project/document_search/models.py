from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from rank_bm25 import BM250kapi

@dataclass(frozen=True, slots=True)
class PageDocument:
    source: str
    page: int
    text: str


@dataclass(frozen=True, slots=True)
class SearchResult:
    document: PageDocument
    score: float


@dataclass(frozen=True, slots=True)
class BM25SearchIndex:
    pages: tuple[PageDocument, ...]
    model: BM250kapi