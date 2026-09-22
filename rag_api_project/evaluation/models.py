from dataclasses import dataclass

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