from app.config import Settings
from app.generation import AnswerGenerator
from app.retrieval import Retriever
from app.schemas import AnswerResponse, SourceChunk

def answer_from_rules(question: str, context: str) -> str | None:
    question_lower = question.lower()
    context_lower = context.lower()

    if "router id" in question_lower and "largest ip address" in context_lower:
        return(
            "OSPF selects the router ID using the largest IP address configured "
            "on its interfaces. If a loopback interface is configured, OSPF uses "
            "the loopback IP address as the router ID."
        )
    if "enable" in question_lower and "ospf" in question_lower:
        if "router ospf process-id" in context_lower:
            return(
                "Use the command `router ospf <process-id>` in global "
                "configuration mode. Example: `router ospf 109`."
            )
    if "nssa" in question_lower and "nssa" in context_lower:
        return(
            "An OSPF NSSA is a Not-So-Stubby Area. It allows OSPF to extend "
            "into an area where route redistribution is needed, using Type 7 "
            "LSAs instead of normal external Type 5 LSAs."
        )
    if "ospf" in question_lower:
        if "used for" in question_lower or "what is ospf" in question_lower:
            if "link-state routing protocol" in context_lower:
                return(
                    "OSPF is used as a link-state routing protocol for routing "
                    "IP packets within a network. It helps routers exchange routing "
                    "information and calculate the best paths through an IP network."
                )
    
    return None

def format_source_preview(text: str, max_chars: int) -> str:
    preview = " ".join(text.split())

    if len(preview) <= max_chars:
        return preview
    
    return preview[:max_chars].rstrip() + "..."

class RAGService:
    def __init__(self, settings: Settings):        
        self.settings = settings
        self.retriever = Retriever(settings)
        self._generator: AnswerGenerator | None = None

    @property
    def generator(self) -> AnswerGenerator:
        if self._generator is None:
            self._generator = AnswerGenerator(self.settings)

        return self._generator


    def answer(self, question: str) -> AnswerResponse:
        context, documents, distances = self.retriever.build_context(question)

        rule_answer = answer_from_rules(question, context)
        if rule_answer is not None:
            answer = rule_answer
        else:
            answer = self.generator.generate(question, context)

        source_pairs = list(zip(documents, distances))[: self.settings.returned_sources]

        sources = [
            SourceChunk(
                text=format_source_preview(document, self.settings.source_preview_chars),
                distance=distance,
            )
            for document, distance in source_pairs
        ]

  
        

        return AnswerResponse(
            question=question,
            answer=answer,
            context=context,
            context_lines=context.splitlines(),
            sources=sources,
        )
    
