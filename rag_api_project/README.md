# RAG API Project

A FastAPI-based Retrieval-Augmented Generation API for answering questions over technical PDF documentation.

The project uses ChromaDB for vector search, Sentence Transformers for embeddings, a CrossEncoder reranker for improving context selection, and a lazy-loaded text generation model as a fallback when rule-based answers are not available.

## Current Capabilities

- Ingests PDF documentation into a local ChromaDB vector database.
- Retrieves relevant document chunks for a user question.
- Extracts and reranks candidate context lines.
- Returns an auditable answer with context and source previews.
- Uses high-confidence rule-based answers for known OSPF questions.
- Lazy-loads the fallback generation model only when needed.
- Provides a simple regression test script for key questions.

## Architecture

The application is split into separate modules:

- `app/main.py` - FastAPI entrypoint and HTTP endpoints.
- `app/config.py` - centralized application settings.
- `app/schemas.py` - request and response models.
- `app/retrieval.py` - ChromaDB retrieval, candidate extraction, reranking, and context building.
- `app/generation.py` - fallback text generation model.
- `app/rag.py` - orchestration layer combining retrieval, rules, and generation.
- `scripts/ingest.py` - PDF ingestion into ChromaDB.
- `scripts/test_questions.py` - simple regression test script.

## Tech Stack

- Python
- FastAPI
- Pydantic
- ChromaDB
- Sentence Transformers
- CrossEncoder reranking
- Transformers
- PyTorch
- pypdf

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file from the example:

```bash
copy .env.example .env
```

The `.env` file can be used to override default settings such as model names, retrieval count, returned source count, and generation limits.

## PDF Ingestion

Place PDF files into the local `data/` directory:

```text
data/
└── example.pdf
```

Run the ingestion script:

```bash
python -m scripts.ingest
```

The script reads PDF files from `data/`, splits the extracted text into chunks, creates embeddings, and stores them in a local ChromaDB database.

The generated ChromaDB files are stored in:

```text
chroma_db/
```

Both `data/` and `chroma_db/` are excluded from Git because they may contain large or local-only files.

## Running the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Health check endpoint:

```bash
curl http://127.0.0.1:8000/
```

Ask a question:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"How does OSPF select the router ID?\"}"
```

For a formatted JSON response on Windows CMD:

```bash
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"How does OSPF select the router ID?\"}" | python -m json.tool
```

## Regression Test Script

The project includes a simple script for checking key RAG questions:

```bash
python -m scripts.test_questions
```

The script runs a small set of predefined questions and prints:

- the question
- the generated or rule-based answer
- the selected context
- a short preview of returned source chunks

This is useful after changing retrieval, reranking, chunking, or rule logic, because it helps verify that existing behavior was not accidentally broken.

## API Response Format

The `/ask` endpoint returns an answer together with the selected context and source previews.

Example response:

```json
{
  "question": "How does OSPF select the router ID?",
  "answer": "OSPF selects the router ID using the largest IP address configured on its interfaces. If a loopback interface is configured, OSPF uses the loopback IP address as the router ID.",
  "context": "OSPF uses the largest IP address configured on the interfaces as its router ID.",
  "context_lines": [
    "OSPF uses the largest IP address configured on the interfaces as its router ID."
  ],
  "sources": [
    {
      "text": "Short source preview...",
      "distance": 0.4004
    }
  ]
}
```

Field meaning:

- `question` - the original user question.
- `answer` - the final answer returned by the RAG service.
- `context` - the selected text used as direct support for the answer.
- `context_lines` - the same context split into individual lines for easier inspection.
- `sources` - short previews of retrieved source chunks.
- `distance` - ChromaDB distance score for the retrieved chunk. Lower values generally mean closer semantic similarity.

## Current Limitations

This is an educational RAG API prototype, not a production-ready system.

Known limitations:

- PDF text extraction can produce noisy text, especially from tables or multi-column layouts.
- Current chunking is character-based, so some chunks may start or end in the middle of a word or sentence.
- Source previews may contain imperfect text formatting from the original PDF extraction.
- Rule-based answers currently cover only a small set of known OSPF questions.
- The fallback generation model is relatively small and may produce incomplete answers for unsupported questions.
- The regression script prints results for manual inspection but does not yet perform automated assertions.

## Planned Improvements

Planned next steps:

- Improve PDF text cleaning before chunking.
- Replace character-based chunking with paragraph-based or sentence-aware chunking.
- Store richer metadata for chunks, such as source file, page number, and chunk index.
- Improve source attribution so returned sources are more directly connected to selected context lines.
- Convert the regression script into assertion-based automated tests.
- Add better API error handling for missing ChromaDB collections or missing ingested data.
- Add Docker support for easier setup and deployment.
- Evaluate stronger fallback generation models.

## Project Status

This project is currently a working educational prototype.

The main RAG API pipeline is functional, including retrieval, reranking, context selection, rule-based answers, lazy-loaded fallback generation, and a basic regression test script.


## Docker

The API can also be built and run with Docker.

The Docker image contains the application code and Python dependencies. Runtime data such as the ChromaDB database, PDF files, `.env`, and Hugging Face model cache are kept outside the image and mounted as volumes.

### Run with Docker Compose

Instead of running the long `docker run` command manually, the API can also be started with Docker Compose:

```bash
docker compose up --build

CTRL+C

docker compose down



### Build the image

```bash
docker build -t rag-api .
```

### Run the API

On Windows Command Prompt:

```cmd
docker run --rm -p 8001:8000 -v "%cd%\chroma_db:/app/chroma_db" -v "%cd%\.cache\huggingface:/app/.cache/huggingface" --name rag-api-container rag-api
```

The API will be available at:

```text
http://127.0.0.1:8001
```

The container exposes port `8000` internally, while the host machine uses port `8001`.

### Test the Docker container

Health check:

```bash
curl http://127.0.0.1:8001/health
```

Stats endpoint:

```bash
curl http://127.0.0.1:8001/stats
```

Ask endpoint:

```bash
curl -X POST http://127.0.0.1:8001/ask -H "Content-Type: application/json" -d "{\"question\":\"How do you enable OSPF routing?\"}"
```

The `/stats` endpoint should show a non-zero chunk count if the local `chroma_db` volume is mounted correctly.

Example:

```json
{
  "app_name": "RAG API",
  "environment": "development",
  "collection_name": "ospf",
  "chunks": 1136,
  "retrieval_results": 8,
  "returned_sources": 3
}
```

### Runtime data

The following paths are intentionally not copied into the Docker image:

```text
data/
chroma_db/
.env
.cache/
```

They are ignored because they are local runtime data, not application source code.

## Testing

The project includes two lightweight test scripts:

- `scripts/test_questions.py`
- `scripts/test_api.py`

### RAG evaluation

Run: `python -m scripts.test_questions`

### API smoke tests

Run: `python -m scripts.test_api`

Expected result for both scripts: `RESULT: 5/5 passed`

