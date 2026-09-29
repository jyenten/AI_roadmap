import random
from collections.abc import Sequence

from evaluation.models import EvaluationQuestion


def sample_questions(
    questions: Sequence[EvaluationQuestion],
    *,
    sample_size: int,
    seed: int,
) -> tuple[EvaluationQuestion, ...]:
    if (
        isinstance(sample_size, bool)
        or not isinstance(sample_size, int)
        or sample_size < 1
    ):
        raise ValueError(
            "sample_size must be a positive integer."
        )

    if sample_size > len(questions):
        raise ValueError(
            "sample_size cannot exceed the number of questions."
        )

    if (
        isinstance(seed, bool)
        or not isinstance(seed, int)
    ):
        raise ValueError(
            "seed must be an integer."
        )

    random_generator = random.Random(seed)

    selected_indices = random_generator.sample(
        range(len(questions)),
        k=sample_size,
    )

    return tuple(
        questions[index]
        for index in sorted(selected_indices)
    )