from dataclasses import dataclass
from pydantic import ValidationError

from app.config import get_settings
from app.rag import RAGService
from app.schemas import QuestionRequest

DIRTY_TEXT_MARKERS = {
    "process-idStep",
    "mode.router",
    "configurationmode.router",
    "â€",
    "\u00e2\u20ac",
}

@dataclass
class EvalCase:
    question: str
    answer_contains: list[str]
    context_contains: list[str]
    expect_sources: bool = True
    expect_source_metadata: bool = True
    expect_generator: bool = False

EVAL_CASES = [
    EvalCase(
        question="How does OSPF select the router ID?",
        answer_contains=["largest IP address", "loopback"],
        context_contains=["largest IP address"],

    ),
    EvalCase(
        question="How do you enable OSPF routing?",
        answer_contains=["router ospf", "process-id", "global configuration mode"],
        context_contains=["Enables OSPF routing"],
        
    ),
    EvalCase(
        question="What is an OSPF NSSA?",
        answer_contains=["Not-So-Stubby Area", "Type 7", "Type 5"],
        context_contains=["NSSA", "Type 7", "Type 5"],
    ),
    EvalCase(
        question="What is OSPF used for?",
        answer_contains=["link-state routing protocol", "IP packets", "best paths"],
        context_contains=["IP networks"],
    ),

]


def contains_all(text: str, expected_phrases: list[str]) -> list[str]:
    text_lower = text.lower()

    return[
        phrase 
        for phrase in expected_phrases
        if phrase.lower() not in text_lower
    ]

def check_case(service: RAGService, case: EvalCase) -> bool:
    generator_before = service._generator is not None

    response = service.answer(case.question)

    generator_after = service._generator is not None
    generator_was_used = not generator_before and generator_after

    failures: list[str] = []

    missing_answer = contains_all(response.answer, case.answer_contains)
    if missing_answer:
        failures.append(f"answer missing: {missing_answer}")

    missing_context = contains_all(response.context, case.context_contains)
    if missing_context:
        failures.append(f"context missing: {missing_context}")

    if case.expect_sources and not response.sources:
        failures.append("sources are empty")

    if case.expect_source_metadata:
        for index, source in enumerate(response.sources, start=1):
            if source.source is None:
                failures.append(f"source {index} missing source filename")

            if source.chunk_index is None:
                failures.append(f"source {index} missing chunk index")

            if source.page is None:
                failures.append(f"source {index} missing page")

    combined_text = "".join(
        [
            response.answer,
            response.context,
            *[source.text for source in response.sources],
        ]
    )

    dirty_markers = [
        marker for marker in DIRTY_TEXT_MARKERS
        if marker in combined_text
    ]

    if dirty_markers:
        failures.append(f"dirty text found: {dirty_markers}")

    if generator_was_used != case.expect_generator:
        failures.append(
            f"generator usage mismatch: expected "
            f"{case.expect_generator}, got {generator_was_used}"
        )


    if failures:
        print("FAIL")
        print(f"QUESTION: {case.question}")
        print(f"ANSWER: {response.answer}")
        print(f"CONTEXT: {response.context}")
        print(f"SOURCES: {len(response.sources)}")

        for failure in failures:
            print(f" - {failure}")

        print()
        return False

    print(f"PASS: {case.question}")
    return True

def check_question_validation() -> bool:
    failures: list[str] = []

    try:
        QuestionRequest(question="      ")
        failures.append("blank question was accepted")
    except ValidationError:
        pass

    request = QuestionRequest(
        question= "    How do you enable OSPF routing?  "
    )

    if request.question != "How do you enable OSPF routing?":
        failures.append("question whitespace was not stripped")

    if failures:
        print("FAIL: QuestionRequest validation")
        for failure in failures:
            print(f"-{failure}")
        print()
        return False

    print("PASS: QuestionRequest validation")
    return True

def main() -> None:
    settings = get_settings()
    service = RAGService(settings)

    results = [
        check_question_validation()
    ]

    results.extend(
        check_case(service, case)
        for case in EVAL_CASES
    )

    passed = sum(results)
    total = len(results)

    print()
    print(f"RESULT: {passed}/{total} passed")

    if passed != total:
        raise SystemExit(1)

if __name__ == "__main__":
    main()



