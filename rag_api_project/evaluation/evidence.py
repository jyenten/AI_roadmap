from collections.abc import Iterable

from evaluation.models import GoldEvidence


def normalize_evidence_text(text: str) -> str:
    return " ".join(text.casefold().split())


def matches_gold_evidence(
    document: str,
    source: str | None,
    page: int | None,
    gold_evidence: tuple[GoldEvidence, ...],
) -> bool:
    normalized_document = normalize_evidence_text(document)

    return any(
        source == evidence.source
        and page in evidence.pages
        and any(
            normalize_evidence_text(fragment)
            in normalized_document
            for fragment in evidence.contains_any
        )
        for evidence in gold_evidence
    )


def find_gold_rank(
    ranked_results: Iterable[
       tuple[str, str | None, int | None] 
    ],
    gold_evidence: tuple[GoldEvidence, ...],
) -> int | None:
    for rank, (
        document,
        source,
        page,
    ) in enumerate(
        ranked_results,
        start=1,
    ):
        if matches_gold_evidence(
            document,
            source,
            page,
            gold_evidence,
        ):
            return rank
    return None