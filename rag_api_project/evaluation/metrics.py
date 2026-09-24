from collections.abc import Iterable

from evaluation.models import EvaluationMetrics


def reciprocal_rank(
    rank: int | None,
) -> float:
    _validate_rank(rank)

    if rank is None:
        return 0.0

    return 1.0 / rank


def hit_at_k(
    rank: int | None,
    k: int,
) -> int:
    _validate_rank(rank)

    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError(
            "k must be a positive integer."
        )

    return int(
        rank is not None
        and rank <= k
    )


def mean_reciprocal_rank(
    ranks: Iterable[int | None],
) -> float:
    ranks = tuple(ranks)

    if not ranks:
        return 0.0

    return sum(
        reciprocal_rank(rank)
        for rank in ranks
    ) / len(ranks)


def aggregate_metrics(
    ranks: Iterable[int | None],
) -> EvaluationMetrics:
    ranks = tuple(ranks)

    if not ranks:
        return EvaluationMetrics(
            mrr=0.0,
            hit_at_1=0.0,
            hit_at_3=0.0,
            hit_at_5=0.0,
            hit_at_8=0.0,
        )

    return EvaluationMetrics(
        mrr=mean_reciprocal_rank(ranks),
        hit_at_1=mean_hit_at_k(ranks, 1),
        hit_at_3=mean_hit_at_k(ranks, 3),
        hit_at_5=mean_hit_at_k(ranks, 5),
        hit_at_8=mean_hit_at_k(ranks, 8),
    )


def mean_hit_at_k(
    ranks: tuple[int | None, ...],
    k: int,
) -> float:
    return sum(
        hit_at_k(rank, k)
        for rank in ranks
    ) / len(ranks)


def _validate_rank(
    rank: int | None,
) -> None:
    if rank is None:
        return

    if (
        isinstance(rank, bool)
        or not isinstance(rank, int)
        or rank < 1
    ):
        raise ValueError(
            "rank must be a positive integer or None."
        )