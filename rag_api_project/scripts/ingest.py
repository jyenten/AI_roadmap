from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader

from app.config import get_settings

def read_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages: list[str] = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages)

def split_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = start + len(text)
        chunk = text[start:end].strip()
        
        chunk = text[start:end].strip()

        if chunk:
         chunks.append(chunk)

        start += chunk_size - overlap

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

    collection = client.get_or_create_collection(
        name=settings.collection_name,
        embedding_function=embedding_function,
    )

    all_chunks: list[str] = []
    all_ids: list[str] = []
    all_metadata: list[dict[str, str]] = []

    for pdf_path in pdf_files:
        text = read_pdf_text(pdf_path)
        chunks = split_text(text)

        for index, chunk in enumerate(chunks):
            chunk_id = f"{pdf_path.stem}-{index}"
            all_chunks.append(chunk)

            all_ids.append(chunk_id)
            all_metadata.append(
                {
                    "source": pdf_path.name,
                    "chunk_index": str(index),
                }
            )
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

