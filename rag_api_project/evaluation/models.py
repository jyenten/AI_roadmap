from dataclasses import dataclass
import math


@dataclass(frozen=True, slots=True)
class GoldEvidence:
    source: str
    pages: tuple[int, ...]
    contains_any: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EvaluationQuestion:
    id: str
    topic: str
    question: str
    gold_evidence: tuple[GoldEvidence, ...]


@dataclass(frozen=True, slots=True)
class QuestionResult:
    id: str
    first_evidence_rank: int | None
    reciprocal_rank: float


@dataclass(frozen=True, slots=True)
class RetrievalConfig:
    collection_name: str
    embedding_model_name: str
    retrieval_results: int


@dataclass(frozen=True, slots=True)
class EvaluationMetrics:
    mrr: float
    hit_at_1: float
    hit_at_3: float
    hit_at_5: float
    hit_at_8: float


@dataclass(frozen=True, slots=True)
class LatencyMetrics:
    mean_ms: float
    p50_ms: float
    p95_ms: float

    def __post_init__(self) -> None:
        for name in ("mean_ms", "p50_ms", "p95_ms"):
            value = getattr(self, name)
            try:
                valid = (
                    not isinstance(value, bool)
                    and isinstance(value, (int, float))
                    and math.isfinite(value)
                    and value >= 0
                )
            except OverflowError as exc:
                raise ValueError(f"{name} must be a finite non-negative number.") from exc
            if not valid:
                raise ValueError(f"{name} must be a finite non-negative number.")
        if self.p95_ms < self.p50_ms:
            raise ValueError("p95_ms must be greater than or equal to p50_ms.")


@dataclass(frozen=True, slots=True)
class EvaluationRun:
    timestamp: str
    git_commit: str
    git_dirty: bool
    dataset_hash: str
    dataset: str
    question_count: int
    retrieval_config: RetrievalConfig
    metrics: EvaluationMetrics
    questions: tuple[QuestionResult, ...]
    sample_seed: int | None = None
    sample_size: int | None = None
    latency: LatencyMetrics | None = None
