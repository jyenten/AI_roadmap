from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app

client = TestClient(app)
settings = get_settings()


def check_health() -> bool:
    response = client.get("/health")

    if response.status_code != 200:
        print("FAIL: /health")
        print(f" - expected status 200, got {response.status_code}")
        print(response.text)
        print()
        return False
    
    data = response.json()
    failures: list[str] = []

    if data.get("status") != "ok":
        failures.append("status is not ok")

    if data.get("app_name") != settings.app_name:
        failures.append("app_name does not match settings")

    if data.get("environment") != settings.environment:
        failures.append("environment does not match settings")

    if failures:
        print("FAIL: /health")
        for failure in failures:
            print(f" - {failure}")
        print()
        return False

    print("PASS: /health")
    return True


def check_ready() -> bool:
    response = client.get("/ready")

    if response.status_code != 200:
        print("FAIL: /ready")
        print(f"- expected status 200, got {response.status_code}")
        print(response.text)
        print()
        return False

    data = response.json()
    failures: list[str] = []

    if data.get("status") != "ready":
        failures.append("status is not ready")

    if data.get("collection_name") != settings.collection_name:
        failures.append("collection_name does not match settings")

    chunks= data.get("chunks")
    if not isinstance(chunks, int) or chunks <= 0:
        failures.append("chunks is not a positive integer")

    if failures:
        print("FAIL: /ready")
        for failure in failures:
            print(f" - {failure}")
        print()
        return False

    print("PASS: /ready")
    return True

def check_stats() -> bool:
    response = client.get("/stats")

    if response.status_code != 200:
        print("FAIL: /stats")
        print(f"- expected status 200, got {response.status_code}")
        print(response.text)
        print()
        return False

    data = response.json()
    failures: list[str] = []

    if data.get("app_name") != settings.app_name:
        failures.append("app_name does not match settings")

    if data.get("environment") != settings.environment:
        failures.append("environment does not match settings")

    if data.get("collection_name") != settings.collection_name:
        failures.append("collection name does not match settings")

    chunks = data.get("chunks")
    if not isinstance(chunks, int) or chunks <= 0:
        failures.append("chunks is not a positive integer")

    if data.get("retrieval_results") != settings.retrieval_results:
        failures.append("retrieval_results does not match settings")

    if data.get("returned_sources") != settings.returned_sources:
        failures.append("returned_sources does not match settings")

    if failures:
        print("FAIL: /stats")
        for failure in failures:
            print(f" - {failure}")
        print()
        return False

    print("PASS: /stats")
    return True

def check_ask() -> bool:
    response = client.post(
        "/ask",
        json={
            "question": "How do you enable OSPF routing?"
        },
    )

    if response.status_code != 200:
        print("FAIL: /ask")
        print(f" - expected status 200, got {response.status_code}")
        print(response.text)
        print()
        return False
    data = response.json()
    failures: list[str] = []

    if data.get("question") != "How do you enable OSPF routing?":
        failures.append("question does not match request")

    answer = data.get("answer", "")
    if "router ospf" not in answer.lower():
        failures.append("answer does not mention router ospf")

    if "global configuration mode" not in answer.lower():
        failures.append("answer does not mention global configuration mode")

    context_lines = data.get("context_lines")
    if not isinstance(context_lines, list) or not context_lines:
        failures.append("context_lines is empty or invalid")

    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        failures.append("sources is empty or invalid")
    else:
        first_source = sources[0]

        if first_source.get("source") is None:
            failures.append("first source missing source filename")

        if first_source.get("chunk_index") is None:
            failures.append("first source missing chunk_index")

        if first_source.get("page") is None:
            failures.append("first source missing page")

    if failures:
        print("FAIL: /ask")
        for failure in failures:
            print(f" - {failure}")
        print()
        return False

    print("PASS: /ask")
    return True

def check_blank_question() -> bool:
    response = client.post(
        "/ask",
        json={
            "question": "       "
        },
    )

    if response.status_code != 422:
        print("FAIL: blank question validation")
        print(f" - expected status 422, got {response.status_code}")
        print(response.text)
        print()
        return False

    print("PASS: blank question validation")
    return True

def main() -> None:
    results = [
        check_health(),
        check_ready(),
        check_stats(),
        check_ask(),
        check_blank_question(),
    ]

    passed = sum(results) 
    total = len(results)

    print()
    print(f"RESULT: {passed}/{total} passed")

    if passed != total:
        raise SystemExit(1)

if __name__ == "__main__":
    main()

    

        
    