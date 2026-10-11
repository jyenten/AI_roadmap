import chromadb

from chromadb.utils import embedding_functions

from app.config import Settings

Metadata = dict[str, str | int | float | bool | None]


class VectorRetriever:
    def __init__(self, settings: Settings):
        self.settings = settings

        self.embedding_function = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=settings.embedding_model_name,
            )
        )

        self.client = chromadb.PersistentClient(
            path=str(settings.chroma_dir),
        )

        self.collection = self.client.get_collection(
            name=settings.collection_name,
            embedding_function=self.embedding_function,
        )

    def search(
        self,
        question: str,
    ) -> tuple[
        list[str],
        list[float],
        list[Metadata]
    ]:
        results = self.collection.query(
            query_texts=[question],
            n_results=self.settings.retrieval_results,
            include=[
                "documents",
                "distances",
                "metadatas",
            ],
        )

        documents = results["documents"][0]
        distances = results["distances"][0]
        metadatas = results["metadatas"][0]

        return documents, distances, metadatas