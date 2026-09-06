import re
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader

from app.config import get_settings

def protect_urls(
    text: str,
) -> tuple[str, dict[str, str]]:
    replacements: dict[str, str] = {}

    def replace_url(match: re.Match[str]) -> str:
        placeholder = f"__URL_{len(replacements)}__"
        replacements[placeholder] = match.group(0)

        return placeholder

    protected_text = re.sub(
        r"https?://[^\s]+",
        replace_url,
        text,
    )

    return protected_text, replacements


def restore_technical_tokens(
    text: str,
    replacements: dict[str, str],
) -> str:
    for placeholder, original in replacements.items():
        text = text.replace(
            placeholder,
            original,
        )

    return text


def clean_pdf_text(text: str) -> str:
    text, protected_tokens = protect_urls(text)
    replacements = {
        "\u00a0": " ",
        "\u00e2\u20ac\u015b": '"',
        "\u00e2\u20ac\u0165": '"',
        "â€¢": "•",
        "â€˜": "•",
        "â€™": "'",
        "â€œ": '"',
        "â€": '"',
        "â€“": "-",
        "â€”": "-",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(
        r"(?<=[a-z])(?=Step\s+\d+\b)",
        " ",
        text,
    )
    text = re.sub(
        r"(?<=[a-z])(?=Example:)",
        " ",
        text,
    )
    text = re.sub(
        r"(?<=[a-z])(?=Router[#>(])",
        " ",
        text,
    )
    text = re.sub(
        r"(?<=[a-z])(?=Device[#>(])",
        " ",
        text,
    )
    text = re.sub(
        r"(?<=[a-z])\.(?=[A-Z][a-z])",
        ". ",
        text,
    )
    text = re.sub(
        r"(?<=[!?])(?=[A-Z][a-z]+(?:\s|$))",
        " ",
        text,
    )
    text = re.sub(
        r"[\t]+",
        " ",
        text,
    )
    text = re.sub(
        r"\n{3,}", "\n\n",
        text,
    )


    text = restore_technical_tokens(
        text,
        protected_tokens,
    )


    return text.strip()


def read_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages: list[str] = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    raw_text = "\n".join(pages)
    return clean_pdf_text(raw_text)

def read_pdf_pages(pdf_path: Path) -> list[tuple [int, str]]:
    reader = PdfReader(str(pdf_path))
    pages: list[tuple[int, str]] = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = clean_pdf_text(text)

        if text:
            pages.append((page_number, text))

    return pages

def get_overlap_text(
    text: str,
    overlap: int,
) -> str:
    if overlap <= 0 or not text:
        return ""

    if len(text) <= overlap:
        return text

    overlap_text = text[-overlap:]

    first_space = overlap_text.find(" ")

    if first_space != -1:
        overlap_text = overlap_text[first_space + 1:]

    return overlap_text.strip()


def validate_chunk_params(
    chunk_size: int,
    overlap: int,
) -> None:
    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0"
        )

    if overlap < 0:
        raise ValueError(
            "overlap must not be negative"
        )

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )


def split_long_text(
    text: str,
    chunk_size: int,
    overlap: int,
) -> list[str]:
    validate_chunk_params(
        chunk_size,
        overlap,
    )
    words = text.split()

    if not words:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(words):
        end = start
        current_words: list[str] = []
        current_length = 0

        while end < len(words):
            word = words[end]

            separator_length = (
                1 if current_words else 0
            )

            next_length = (
                current_length
                + separator_length
                + len(word)
            )

            if next_length > chunk_size:
                break

            current_words.append(word)
            current_length = next_length
            end += 1

        if not current_words:
            chunks.append(words[start])
            start += 1
            continue

        chunk = " ".join(current_words)
        chunks.append(chunk)

        if end >= len(words):
            break

        overlap_text = get_overlap_text(
            chunk,
            overlap,
        )

        overlap_word_count = len(
            overlap_text.split()
        )

        new_start = end - overlap_word_count

        if new_start <= start:
            new_start = start + 1

        start = new_start

    return chunks


def split_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[str]:
    validate_chunk_params(
        chunk_size,
        overlap,
    )
    units = [
        unit.strip()
        for unit in re.split(r"\n[ \t]*\n|(?<=[.!?])\s+", text)
        if unit.strip()
    ]

    chunks: list[str] = []
    current = ""

    for unit in units:
        if len(unit) > chunk_size:
            if current:
                chunks.append(current)
                current = ""

            chunks.extend(
                split_long_text(
                    unit,
                    chunk_size,
                    overlap,
                )
            )
            continue

        candidate = f"{current}\n\n{unit}".strip()

        if len(candidate) <= chunk_size:
            current = candidate

        else:
            if current:
                chunks.append(current)

                overlap_text = get_overlap_text(
                    current,
                    overlap,
                )

                candidate = f"{overlap_text}\n\n{unit}".strip()

                if len(candidate) <= chunk_size:
                    current = candidate
                else:
                    current = unit
            else:
                current = unit

    if current:
        chunks.append(current)

    return chunks


def main() -> None:
    settings = get_settings()

    pdf_files = list(settings.data_dir.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in {settings.data_dir}"
        )
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=settings.embedding_model_name
    )

    client = chromadb.PersistentClient(
        path=str(settings.chroma_dir)
    )

    collection_names = [
        collection.name if hasattr(collection, "name") else collection
        for collection in client.list_collections()
    ]

    if settings.collection_name in collection_names:
        client.delete_collection(name=settings.collection_name)

    collection = client.create_collection(
        name=settings.collection_name,
        embedding_function=embedding_function,
    )

    all_chunks: list[str] = []
    all_ids: list[str] = []
    all_metadata: list[dict[str, str | int]] = []

    for pdf_path in pdf_files:
        pages = read_pdf_pages(pdf_path)
        global_chunk_index = 0

        for page_number, page_text in pages:
            chunks = split_text(page_text)


            for page_chunk_index, chunk in enumerate(chunks):
                chunk_id = (
                    f"{pdf_path.stem}"
                    f"page-{page_number}"
                    f"chunk-{page_chunk_index}"
                )   

                all_chunks.append(chunk)
                all_ids.append(chunk_id)
                all_metadata.append(
                    {
                        "source": pdf_path.name,
                        "chunk_index": global_chunk_index,
                        "page": page_number,
                    }
                )

                global_chunk_index += 1


    if not all_chunks:
        raise ValueError("No text chunks were created from the PDF files")
    
    collection.upsert(
        documents=all_chunks,
        ids= all_ids,
        metadatas=all_metadata,
    )

    print(
        f"Ingest completed: {len(all_chunks)} chunks "
        f"stored in collection '{settings.collection_name}'."
    )


if __name__ == "__main__":
    main()