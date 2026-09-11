from pathlib import Path

from pypdf import PdfReader

PDF_PATH = Path(
    "data/Cisco_OSPF_Configuration_Guide_2026.pdf"
)

SEARCH_TERM = "virtual link"

def main() -> None:
    reader = PdfReader(str(PDF_PATH))

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):
        text = page.extract_text() or ""

        position = text.lower().find(
            SEARCH_TERM.lower()
        )

        if position == -1:
            continue

        start = max(
            0,
            position - 500,
        )
        end = position + 1000

        print("=" * 80)
        print(f"PAGE: {page_number}")
        print()
        print(text[start:end])
        print()


if __name__ == "__main__":
    main()