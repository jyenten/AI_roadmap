from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

from app.config import get_settings

BASE_DIR = Path(__file__).resolve().parent.parent
TEST_CHROMA_DIR = BASE_DIR / "test_chroma_db"

TEST_DOCUMENTS = [
    ("test_ospf.md", 1, "OSPF uses the largest IP address configured on its interfaces as the router ID. If a loopback interface is configured, OSPF uses the loopback IP address as the router ID."),
    ("test_ospf.md", 2, "router ospf process-id\nEnables OSPF routing and enters router configuration mode.\nDevice(config)# router ospf 109"),
    ("test_ospf.md", 3, "An OSPF NSSA is a Not-So-Stubby Area. NSSA uses Type 7 LSAs that can be translated into Type 5 LSAs for external routes."),
    ("test_ospf.md", 4, "OSPF is an interior gateway protocol and a link-state routing protocol designed expressly for IP networks. It helps routers route IP packets and calculate best paths."),
]

def main() -> None:
    settings = get_settings()

    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=settings.embedding_model_name,
    )

    client = chromadb.PersistentClient(
        path=str(TEST_CHROMA_DIR),
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

    ids: list[str] = []
    documents: list[str] = []
    metadatas: list[dict[str, str | int]] = []

    for chunk_index, (source, page, text) in enumerate(TEST_DOCUMENTS):
        ids.append(f"test-chunk-{chunk_index}")
        documents.append(text)
        metadatas.append(
            {"source": source, "page": page, "chunk_index": chunk_index}
        )

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    print(
        f"Created test ChromaDB collection "
        f"'{settings.collection_name}' with {len(documents)} documents "
        f"in {TEST_CHROMA_DIR}"
    )

if __name__ == "__main__":
    main()


    

