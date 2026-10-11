import math
from statistics import fmean, median
from time import perf_counter
from typing import Protocol

from evaluation.models import LatencyMetrics


Metadata = dict[str, str | int | float | bool | None]
SearchResult = tuple[
    list[str],
    list[float],
    list[Metadata],
]


class Retriever(Protocol):
    def search(
        self,
        question: str,
    ) -> SearchResult:
        ...


class TimedRetriever:
    def __init__(
        self,
        retriever: Retriever,
    ):
        self.retriever = retriever
        self.latencies_ms: list[float] = []

    def search(
        self,
        question: str,
    ) -> SearchResult:
        start = perf_counter()

        result = self.retriever.search(question)
        elapsed_ms = (perf_counter() - start) * 1000
        self.latencies_ms.append(elapsed_ms)
        return result


    def metrics(self) -> LatencyMetrics:
        if  not self.latencies_ms:
            raise ValueError(
                "No retrieval latency samples recorded."
            )

        values = sorted(
            self.latencies_ms
        )

        p95_index = (
            math.ceil(
                0.95 * len(values)
            )
            - 1
        )

        return LatencyMetrics(
            mean_ms=fmean(values),
            p50_ms=median(values),
            p95_ms=values[p95_index],
        )
