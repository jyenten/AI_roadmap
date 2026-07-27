from app.config import get_settings
from app.rag import RAGService


QUESTIONS = [
    "How does OSPF select the router ID?",
    "How do you enable OSPF routing?",
    "What is an OSPF NSSA?",
    "What is OSPF used for?",
]

def main() -> None:
    settings = get_settings()
    service = RAGService(settings)

    for question in QUESTIONS:
        response = service.answer(question)
        print("=" * 80)

        print("\nQUESTION:")
        print(question)

        print("ANSWER:")
        print(response.answer)

        print("CONTEXT:")
        print(response.context)

        print(f"SOURCES ({len(response.sources)}):")
        for index, source in enumerate(response.sources, start=1):
            preview = source.text[:160]
            print(f"{index}. distance={source.distance:.4f}")
            print(f"{preview}...")

if __name__ == "__main__":
    main()