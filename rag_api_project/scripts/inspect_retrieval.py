import re

from app.config import get_settings
from app.retrieval import (Retriever,
                           collect_candidate_lines,
                           score_line,
                           lexical_overlap_score,
                           RetrievedLine,
                        )


QUESTION = "How do you enable OSPF routing?"

EVAL_QUESTIONS = [
    "How does OSPF select the router ID?",
    "How do you enable OSPF routing?",
    "What is an OSPF NSSA?",
    "What is OSPF used for?",
]

TEST_LINES = [
    "router ospf process-id",
    "Enables OSPF routing and enters router configuration",
    "Device(config)# router ospf 109",
    "Device(config)# router ospfv3 1",
]

def inspect_crossencoder_only(
        retriever: Retriever,
        question: str,
) -> None:
    documents, _distances, metadatas = retriever.search(question)

    raw_retrieved_lines: list[RetrievedLine] = []
    seen_texts: set[str] = set()

    for document, metadata in zip(documents, metadatas):
        candidates = re.split(
            r"\n+|(?<=[.!?])\s+",
            document,
        )

        for candidate in candidates:
            line = candidate.strip()

            if len(line) < 20 or line in seen_texts:
                continue

            raw_retrieved_lines.append(
                RetrievedLine(
                    text=line,
                    metadata=metadata,
                )
            )

            seen_texts.add(line)

    model_scores = retriever.reranker.predict(
        [
            (question, line.text)
            for line in raw_retrieved_lines
        ]
    )

    ranked_lines = sorted(
        zip(model_scores, raw_retrieved_lines),
        key=lambda item: float(item[0]),
        reverse=True
    )

    print("=" * 80)
    print(f"QUESTION: {question}")
    print()

    for rank, (model_score, line) in enumerate(
        ranked_lines[:5],
        start=1,
    ):
        print(f"RANK: {rank}")
        print(
            f"CROSSENCODER SCORE: "
            f"{float(model_score):.4f}"
        )
        print(f"PAGE: {line.metadata.get('page')}")
        print(f"CHUNK: "
              f"{line.metadata.get('chunk_index')}"

        )

        print(f"TEXT: {line.text}")
        print()

def inspect_current_hybrid(
        retriver: Retriever,
        question: str,
) -> None:
    (
        _context,
        selected_lines,
        _documents,
        _distances,
        _metadatas,
    ) = retriver.build_context(question)

    model_scores = retriver.reranker.predict(
        [
            (question, line.text)
            for line in selected_lines
        ]
    )

    print("=" * 80)
    print(f"HYBRID QUESTION: {question}")
    print()

    for rank, (line, model_score) in enumerate(
        zip(selected_lines, model_scores),
        start=1,
    ):
        heuristic_score = score_line(
            question,
            line.text,
        )

        combined_score = (
            float(model_score) + heuristic_score
        )

        print(f"RANK: {rank}")
        print(
            f"CROSSENCODER SCORE: "
            f"{float(model_score):.4f}"
        )
        print(f"HEURISTIC SCORE: {heuristic_score}")
        print(f"COMBINED SCORE: {combined_score:.4f}")
        print(f"PAGE: {line.metadata.get('page')}")
        print(
              f"CHUNK: "
              f"{line.metadata.get('chunk_index')}"

        )
        print(f"TEXT: {line.text}")
        print()

def inspect_hybrid_threshold(
        retriever: Retriever,
        question: str,
) -> None:
    documents, _distances, metadatas = retriever.search(
        question
    )

    candidate_lines = collect_candidate_lines(
        question,
        documents,
        metadatas,
    )

    candidate_lines = candidate_lines[
        : retriever.settings.reranker_candidate_lines
    ]

    model_scores = retriever.reranker.predict(
        [
            (question, line.text)
            for line in candidate_lines
        ]
    )

    ranked = []

    for model_score, line in zip(
        model_scores,
        candidate_lines,
    ):
        heuristic_score = score_line(
            question,
            line.text,
        )

        combined_score = (
            float(model_score) + heuristic_score
        )

        ranked.append(
            (
                combined_score,
                float(model_score),
                heuristic_score,
                line,
            )
        )

    ranked.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    best_score = ranked[0][0]
    minimum_score = best_score * 0.5

    print("=" * 80)
    print(f"THRESHOLD QUESTION: {question}")
    print(f"BEST SCORE: {best_score:.4f}")
    print(f"MINIMUM SCORE: {minimum_score:.4f}")
    print()

    for rank, (
        combined_score,
        model_score,
        heuristic_score,
        line,
    ) in enumerate(
        ranked[:10],
        start=1,
    ):
        status = (
            "KEEP"
            if combined_score >= minimum_score
            else "DROP"
        )

        print(f"RANK: {rank}")
        print(f"STATUS: {status}")
        print(f"COMBINED SCORE: {combined_score:.4f}")
        print(f"CROSSENCODER SCORE: {model_score:.4f}")
        print(f"HEURISTIC SCORE: {heuristic_score}")
        print(f"PAGE: {line.metadata.get('page')}")
        print(f"CHUNK: {line.metadata.get('chunk_index')}")
        print(f"TEXT: {line.text}")
        print()



def main() -> None:

    print("LEXICAL OVERLAP TEST")
    print()

    for line in TEST_LINES:
        overlap_score = lexical_overlap_score(
            QUESTION,
            line,
        )

        print(f"SCORE: {overlap_score}")
        print(f"TEXT: {line}")
        print()


    settings = get_settings()
    retriever = Retriever(settings)

    documents, distances, metadatas = retriever.search(QUESTION)

    raw_lines: set[str] = set()

    raw_retrieved_lines: list[RetrievedLine] = []
    seen_texts: set[str] = set()

    for document, metadata in zip(
        documents,
        metadatas,
    ):
        candidates = re.split(
            r"\n+|(?<=[.!?])\s+",
            document,
        )

        for candidate in candidates:
            line = candidate.strip()

            if len(line) < 20 or line in seen_texts:
                continue

            raw_retrieved_lines.append(
                RetrievedLine(
                    text=line,
                    metadata=metadata,
                )
            )

            seen_texts.add(line)

    lexical_with_neighbors: set[str] = set()

    for document in documents:
        candidates = [
            candidate.strip()
            for candidate in re.split(
                r"\n+|(?<=[.!?])\s+",
                document,
            )
            if len(candidate.strip()) >= 20
        ]

        for index, line in enumerate(candidates):
            if lexical_overlap_score(QUESTION, line) > 0:
                lexical_with_neighbors.add(line)

            if index > 0:
                lexical_with_neighbors.add(
                    candidates[index - 1]
                )

            if index + 1 < len(candidates):
                lexical_with_neighbors.add(
                    candidates[index -1]
                )

    for document in documents:
        candidates = re.split(
            r"\n+|(?<=[.!?])\s+",
            document,
        )

        for candidate in candidates:
            line = candidate.strip()

            if len(line) >= 20:
                raw_lines.add(line)

    lexical_candidate_lines = [
        line
        for line in raw_lines
        if lexical_overlap_score(QUESTION, line) > 0
    ]

    print(f"QUESTION: {QUESTION}")
    print(f"RESULTS: {len(documents)}")
    print()

    for rank, (document, distance, metadata) in enumerate(
        zip(documents, distances, metadatas),
        start=1,
    ):
        source = metadata.get("source")
        page = metadata.get("page")
        chunk_index = metadata.get("chunk_index")

        preview = " ".join(document.split())

        if len(preview) > 300:
            preview = preview[:300].rstrip() + "..."

        print(f"RANK: {rank}")
        print(f"DISTANCE: {distance:.4f}")
        print(f"SOURCE: {source}")
        print(f"PAGE: {page}")
        print(f"CHUNK: {chunk_index}")
        print(f"TEXT: {preview}")
        print()

    candidate_lines = collect_candidate_lines(
        QUESTION,
        documents,
        metadatas,
    )

    filtered_candidate_count = len(candidate_lines)

    filtered_texts = {
        line.text
        for line in candidate_lines
    }

    lexical_texts = set(lexical_candidate_lines)

    common_lines = filtered_texts & lexical_texts
    only_filtered = filtered_texts - lexical_texts
    only_lexical = lexical_texts - filtered_texts

    candidate_lines = candidate_lines[
        : settings.reranker_candidate_lines
    ]

    reranker_candidate_count = len(candidate_lines)

    reranked_lines = retriever.rerank_lines(
        QUESTION,
        candidate_lines,
    )

    model_scores = retriever.reranker.predict(
        [
            (QUESTION, line.text)
            for line in reranked_lines
        ]
    )

    print(f"RAW CANDIDATE LINES: {len(raw_lines)}")
    print(f"LEXICAL CANDIDATE LINES:"
          f"{len(lexical_candidate_lines)}")
    print(
        f"LEXICAL + NEIGHBORS: "
        f"{len(lexical_with_neighbors)}"
    )
    print(f"FILTERED CANDIDATE LINES: {filtered_candidate_count}")
    print(f"RERANKER CANDIDATE LINES: {reranker_candidate_count}")
    print()

    print(
        f"RAW RETRIEVED LINES: "
        f"{len(raw_retrieved_lines)}"
    )

    raw_model_scores = retriever.reranker.predict(
        [
            (QUESTION, line.text)
            for line in raw_retrieved_lines
        ]
    )

    crossencoder_ranked = sorted(
        zip(raw_model_scores, raw_retrieved_lines),
        key=lambda item: float(item[0]),
        reverse=True,
    )

    print()
    print("=" * 80)
    print("CROSSENCODER ONLY - TOP10")
    print()

    for rank, (model_score, line) in enumerate(
        crossencoder_ranked[:10],
        start=1,
    ):
        source = line.metadata.get("source")
        page = line.metadata.get("page")
        chunk_index = line.metadata.get("chunk_index")

        print(f"RANK: {rank}")
        print(f"CROSSENCODER SCORE: {float(model_score):4f}")
        print(f"SOURCE: {source}")
        print(f"PAGE: {page}")
        print(f"CHUNK: {chunk_index}")
        print(f"TEXT: {line.text}")
        print("=" * 80)
        print()

    print(f"COMMON LINES: {len(common_lines)}")
    print(f"ONLY CURRENT FILTER: {len(only_filtered)}")
    print(f"ONLY LEXICAL FILTER: {len(only_lexical)}")
    print()

    print("=" * 80)
    print("AFTER RERANKING")
    print(f"SELECTED LINES: {len(reranked_lines)}")
    print()

    for rank, (line, model_scores) in enumerate(
        zip(reranked_lines, model_scores),
        start=1,
        ):

        source = line.metadata.get("source")
        page = line.metadata.get("page")
        chunk_index = line.metadata.get("chunk_index")

        preview = " ".join(line.text.split())


        if len(preview) > 300:
            preview = preview[:300].rstrip() + "..."


        heuristic_score = score_line(
            QUESTION,
            line.text,
        )

        combined_score = (
            float(model_scores) + heuristic_score
        )

        print(f"COMBINED SCORE: {combined_score:.4f}")
        print(f"CROSSENCODER SCORE: {float(model_scores):.4f}")
        print(f"HEURISTIC SCORE: {heuristic_score}")
        print(f"RANK: {rank}")
        print(f"SOURCE: {source}")
        print(f"PAGE: {page}")
        print(f"CHUNK: {chunk_index}")
        print(f"TEXT: {preview}")
        print()

        print()
        print("=" * 80)
        print("CROSSENCODER EVALUATION")
        print()

        for question in EVAL_QUESTIONS:
            inspect_crossencoder_only(
                retriever,
                question,
            )

        print()
        print("=" * 80)
        print("CURRENT HYBRID EVALUATION")
        print()

        for question in EVAL_QUESTIONS:
            inspect_current_hybrid(
                retriever,
                question,
            )

    print()
    print("=" * 80)
    print("THRESHOLD DIAGNOSTIC")
    print()

    inspect_hybrid_threshold(
        retriever,
        "How does OSPF select the router ID?",
    )

if __name__ == "__main__":
    main()
