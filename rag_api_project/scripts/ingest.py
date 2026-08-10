import re
import textwrap
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader

from app.config import get_settings

def clean_pdf_text(text: str) -> str:
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

    text = re.sub(r"(?<=[a-z])(?=Step\s+\d+\b)", " ", text)
    text = re.sub(r"(?<=[a-z])(?=Example:)", " ", text)
    text = re.sub(r"(?<=[a-z])(?=Router[#>(])", " ", text)
    text = re.sub(r"(?<=[a-z])(?=Device[#>(])", " ", text)
    text = re.sub(r"(?<=[.!?])(?=\S)", " ", text)

    text = re.sub(r"[\t]+", " ", text)
    text = re.sub(r"\n{3,}", "n\n", text)

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

def split_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
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
                textwrap.wrap(
                    unit,
                    width=chunk_size,
                    break_long_words=False,
                    break_on_hyphens=False,
                )
            )
            continue

        candidate = f"{current}\n\n{unit}".strip()

        if len(candidate) <= chunk_size:
            current = candidate

        else:
            if current:
                chunks.append(current)

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

