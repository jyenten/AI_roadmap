import re
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import CrossEncoder
from app.config import Settings

STOPWORDS = {
    "how", "do", "you", "the", "is", "an", "a",
    "what", "does", "to", "of", "and", "or",
    "in", "on", "for",
}
def extract_keywords(question: str) -> list[str]:
    words = re.findall(r"\b[a-zA-Z0-9]+\b", question.lower())
    return [
        word for word in words
        if word not in STOPWORDS
    ]
def expand_question_for_search(question: str) -> str:
    question_lower = question.lower()

    if "ospf" in question_lower:
        if "used for" in question_lower or "what is ospf" in question_lower:
            return(
                question
                + "Open Shortest Path First Interior Gateway Protocol"
                + "IP networks routing protocol link-state"
            )
    return question


SKIP_PHRASES = [
    "ip routing: ospf configuration guide",
    "restrictions for ipv6 routing",
    "information about ipv6 routing",
    "ospfv3 is a routing protocol",
    "the defaults for commands",
    "you can use this feature to more easily identify",
    "forcing the router id choice",
    "because loopback interfaces never go down",
    "by name rather than",
    "if an ospf process does not already exist",
    "router ospf command will now be accepted",
    "please provide a router-id",
    "memory and cpu are constrained",
    "ospf nsf",
]

def score_line(question: str, line: str) -> int:
    keywords = extract_keywords(question)
    line_lower = line.lower()
    question_lower = question.lower()

    if any(phrase in line_lower for phrase in SKIP_PHRASES):
        return 0
    
    if "router id" in question_lower:
        if "router-id" in line_lower:
            return 0
        if "process-id" in line_lower:
            return 0
        if "process id" in line_lower:
            return 0
        if "address-family" in line_lower:
            return 0
        if "routing loops" in line_lower:
            return 0
        if "multi-vrf" in line_lower:
            return 0
        if "provider edge" in line_lower:
            return 0
        if "route source represents" in line_lower:
            return 0
        if "ospf router id of the lsa" in line_lower:
            return 0
    
    score = 0

    for keyword in keywords:
        if keyword in line_lower:
            score += 1
    if "router id" in question_lower:
        if "ospf uses the largest ip address" in line_lower:
            score += 20
        if "largest ip address" in line_lower and " router id" in line_lower:
            score += 15
        if "loopback interface" in line_lower and "router id" in line_lower:
            score += 8
    
    if "nssa" in question_lower:
        if "nssa" in line_lower:
            score += 10
        if "type 7" in line_lower:
            score += 8
        if "stub area" in line_lower:
            score += 5

    if "enable" in question_lower and "ospf" in question_lower:
        if "router ospf process-id" in line_lower:
            score +=25
        if "device(config)# router ospf" in line_lower:
            score += 20
        if "enables ospf routing" in line_lower:
            score += 15

        if "configure terminal" in line_lower:
            score += 5

    if "ospf" in question_lower:
        if "used for" in question_lower or "what is ospf" in question_lower:
            if "interior gateway protocol" in line_lower:
                score += 25
            if "routing protocol" in line_lower:
                score += 15
            if "ip networks" in line_lower:
                score += 15
            if "shortest path first" in line_lower:
                score += 10
            if "customer edge" in line_lower:
                score -= 10
            if "pe and ce" in line_lower:
                score -= 10

    return score

def collect_candidate_lines(question: str, documents: list[str]) -> list[str]:
    text = "\n".join(documents)
    candidates = re.split(r"\n+|(?<=[.!?])\s+", text)
    scored_lines: list[tuple[int, str]] = []
    seen: set[str] = set()

    for candidate in candidates:
        line = candidate.strip()

        if len(line) < 20 or line in seen:
            continue

        score = score_line(question, line)

        if score > 0:
            scored_lines.append((score, line))
            seen.add(line)
    
    scored_lines.sort(key=lambda item: item[0], reverse=True)
    return [
        line for score,
        line in scored_lines
    ]

def select_relevant_lines(
    question: str,
    documents: list[str],
    max_lines: int,
) -> str:
    text = "\n".join(documents)
    candidates = re.split(r"\n|(?<=[.!?])\s+", text)
    scored_lines: list[tuple[int, str]] = []

    for candidate in candidates:
        line = candidate.strip()

        if len(line) < 20:
            continue

        score = score_line(question, line)

        if score > 0:
            scored_lines.append((score, line))

    scored_lines.sort(
        key=lambda item:item[0],
        reverse=True,
    )

    selected_lines = [
        line for score, line in scored_lines[:max_lines]
    ]

    return "\n".join(selected_lines)



class Retriever:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.reranker = CrossEncoder(
            settings.reranker_model_name
        )
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.embedding_model_name
        )
        self.client = chromadb.PersistentClient(
            path=str(settings.chroma_dir)
        )
        self.collection = self.client.get_collection(
            name=settings.collection_name,
            embedding_function=self.embedding_function,
        )
    
    def search(self, question: str) -> tuple[list[str], list[float]]:
        search_question = expand_question_for_search(question)


        results = self.collection.query(
            query_texts=[question],
            n_results=self.settings.retrieval_results,
            include=["documents", "distances"],
        )
        documents = results["documents"][0]
        distances = results["distances"][0]

        return documents, distances
    
    def rerank_lines(self, question: str, lines: list[str]) -> list[str]:
        if not lines:
            return[]
        
        pairs = [(question, line) for line in lines]
        scores = self.reranker.predict(pairs)

        ranked = []

        for model_score, line in zip(scores, lines):
            heuristic_score = score_line(question, line)
            combined_score = float(model_score) + heuristic_score
            ranked.append((combined_score, line))

        ranked.sort(key=lambda item: item[0], reverse=True)
        
        best_score = ranked[0][0]
        minimum_score = best_score * 0.5

        selected_lines = [
            line for score, line in ranked
            if score >= minimum_score
        ]
        
        return selected_lines[: self.settings.max_context_lines]
    


    def build_context(self, question: str) -> tuple[str, list[str], list[float]]:
        documents, distances = self.search(question)

        candidate_lines = collect_candidate_lines(question, documents)
        candidate_lines = candidate_lines[: self.settings.reranker_candidate_lines]

        selected_lines = self.rerank_lines(question, candidate_lines)
        context = "\n".join(selected_lines)

        if not context:
            context = select_relevant_lines(
                question,
                documents,
                self.settings.max_context_lines
            )
        return context, documents, distances