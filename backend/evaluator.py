import json
import time

from backend.hybrid_retriever import get_hybrid_results
from backend.reranker import rerank_documents
from backend.llm import get_llm
from backend.utils.prompts import build_prompt

def evaluate():
    with open("testset.json") as f:
        test_data = json.load(f)

    llm = get_llm()

    correct = 0
    refused_correctly = 0
    total_latency = 0

    for item in test_data:
        query = item["question"]
        expected = item["expected"]

        start = time.time()

        raw_docs = get_hybrid_results(query)
        docs = rerank_documents(query, raw_docs)

        context = "\n\n".join([doc.page_content[:400] for doc in docs])
        prompt = build_prompt(context, query)

        response = llm(prompt)

        latency = time.time() - start
        total_latency += latency

        # Check correctness
        if expected == "REFUSE":
            if "don't know" in response.lower():
                refused_correctly += 1
        else:
            if expected.lower() in response.lower():
                correct += 1

    print("\nEvaluation Results:")
    print("Answer Accuracy:", correct / len(test_data))
    print("Refusal Accuracy:", refused_correctly / len(test_data))
    print("Average Latency:", total_latency / len(test_data))

if __name__ == "__main__":
    evaluate()