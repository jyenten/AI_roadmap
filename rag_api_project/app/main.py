from functools import lru_cache
from pathlib import Path

from pydantic import Field
from fastapi import FastAPI

from app.config import get_settings
from app.rag import RAGService
from app.schemas import AnswerResponse, QuestionRequest

settings = get_settings()

app = FastAPI(
    title=settings.app_name,

)

rag_service = RAGService(settings)

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
    return rag_service.answer(request.question)


