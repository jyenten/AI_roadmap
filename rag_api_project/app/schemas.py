from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1)

class SourceChunk(BaseModel):
    text: str
    distance: float | None = None
    source: str | None = None
    chunk_index: int | None = None
    page: int | None = None



class AnswerResponse(BaseModel):
    question: str
    answer: str
    context: str
    context_lines: list[str] = Field(default_factory=list)
    sources: list[SourceChunk] = Field(default_factory=list)

    
    

    