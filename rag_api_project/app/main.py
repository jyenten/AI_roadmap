from functools import lru_cache
from pathlib import Path

from pydantic import Field
from fastapi import FastAPI, HTTPException, status

from app.config import get_settings
from app.rag import RAGService
from app.schemas import AnswerResponse, QuestionRequest

settings = get_settings()

app = FastAPI(
    title=settings.app_name,

)

@lru_cache
def get_rag_service() -> RAGService:
    """
    Lazily creates and caches the RAG service.
    """

    return RAGService(settings)

def require_rag_service() -> RAGService:
    try:
        return get_rag_service()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"RAG service is not available: {exc}",
        ) from exc

@app.get("/")
def health_check() -> dict[str, str]:
    return{
        "status": "ok",
        "message": "RAG API is running",
    }

@app.get("/health")
def health() -> dict[str, str]:
    return{
        "status": "ok",
        "app_name": settings.app_name,
        "environment": settings.environment,
    }

@app.get("/stats")
def stats() -> dict[str, str | int]:
    rag_service = require_rag_service()


    return{
        "app_name": settings.app_name,
        "environment": settings.environment,
        "collection_name": settings.collection_name,
        "chunks": rag_service.retriever.collection.count(),
        "retrieval_results": settings.retrieval_results,
        "returned_sources": settings.returned_sources,
    }

    
@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest) -> AnswerResponse:
    rag_service = require_rag_service()
    return rag_service.answer(request.question)


