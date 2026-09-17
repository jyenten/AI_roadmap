import argparse
from pathlib import Path

from document_search.build_index import build_bm25_index
from document_search.load_pages import load_pdf_pages
from document_search.models import SearchResult
from document_search.search import search_pages

DEFAULT_DATA_DIR = Path("data")
DEFAULT_TOP_K = 10
PREVIEW_LENGHT = 300


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search PDF documents using BM25."
    )

    parser.add_argument(
        "query",
        help="Text query to search for.",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help=f"Number of results to return (default: {DEFAULT_TOP_K})"
    )

    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help=f"Directory containing PDFs (default: {DEFAULT_DATA_DIR}).",
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Select a result and display its full page text.",
    )

    return parser


def make_preview(
    text: str,
    max_lenght: int = PREVIEW_LENGHT,
) -> str:
    compact = " ".join(text.split())

    if len(compact) <= max_lenght:
        return compact

    return compact[:max_lenght].rstrip() + "..."


def print_results(
    results: list[SearchResult],
) -> None:
    if not results:
        print("No results found.")
        return

    for rank, result in enumerate(
        results,
        start=1,
    ):
        document = result.document

        print(
            f"{rank}. "
            f"{document.source} | "
            f"page {document.page} | "
            f"score={result.score:.4f}" 
        )
        print(make_preview(document.text))
        print()

def select_result(
    results: list[SearchResult],
) -> SearchResult | None:
    while True:
        choice = input(
            "Select result number for full text "
            "or press Enter to exit: "
        ).strip()

        if not choice:
            return None

        try:
            selected_index = int(choice) - 1
        except ValueError:
            print("Enter a result number.")
            continue

        if 0 <= selected_index < len(results):
            return results[selected_index]

        print(
            f"Choose a number between 1 and {len(results)}."
        )


def print_result_detail(
    result: SearchResult,
) -> None:
    document = result.document

    print("=" * 80)
    print(f"SOURCE: {document.source}")
    print(f"PAGE:   {document.page}")
    print(f"SCORE:  {result.score:.4f}")
    print("=" * 80)
    print(document.text)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    pages = load_pdf_pages(args.data_dir)
    index = build_bm25_index(pages)

    results = search_pages(
        index,
        args.query,
        top_k=args.top_k,
    )

    print_results(results)

    if args.interactive and results:
        selected = select_result(results)

        if selected is not None:
            print_result_detail(selected)


if __name__ == "__main__":
    main()