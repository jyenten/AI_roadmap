from evaluation.evidence import(
    find_gold_rank,
    matches_gold_evidence,
)
from evaluation.models import GoldEvidence


def build_gold_evidence() -> tuple[GoldEvidence, ...]:
    return (
        GoldEvidence(
            source="manual.pdf",
            pages=(26,),
            contains_any=(
                "cost = reference_bandwidth / interface_bandwidth",
            ),
        ),
    )


def test_matches_gold_evidence() -> None:
    evidence = build_gold_evidence()

    assert matches_gold_evidence(
        document=(
            "OSPF calculates cost using "
            "COST = reference_bandwidth / interface_bandwidth."
        ),
        source="manual.pdf",
        page=26,
        gold_evidence=evidence,
    )


def test_matching_requires_correct_source_and_page() -> None:
    evidence = build_gold_evidence()

    assert not matches_gold_evidence(
        document=(
            "cost = reference_bandwidth / interface_bandwidth"
        ),
        source="other.pdf",
        page=26,
        gold_evidence=evidence,
    )


def test_find_gold_rank_returns_first_matching_rank() -> None:
    evidence = build_gold_evidence()

    results = [
        (
            "Unrelated text.",
            "manual.pdf",
            10,
        ),
        (
            "Cost = reference_bandwidth / interface_bandwidth",
            "manual.pdf",
            26,
        ),
        (
            "Cost = reference_bandwidth / interface_bandwidth",
            "manual.pdf",
            26,
        ),
    ]

    assert find_gold_rank(
        results,
        evidence,
    ) == 2