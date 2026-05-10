from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

from hybrid_retriever import get_hybrid_results
from reranker import rerank_documents
from llm import get_llm
from utils.prompts import build_prompt

app = FastAPI()

# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- REQUEST MODEL ----------------

class QueryRequest(BaseModel):
    question: str


# ---------------- CONFIDENCE FUNCTION ----------------

def calculate_confidence(docs, response):

    if not docs:
        return 0.0

    if "don't know" in response.lower():
        return 0.2

    score = min(len(docs) / 5, 1.0)

    return round(score, 2)


# ---------------- API ----------------

@app.post("/ask")
def ask_question(request: QueryRequest):

    start_time = time.time()

    query = request.question

    # Retrieval
    raw_docs = get_hybrid_results(query)

    # Reranking
    docs = rerank_documents(query, raw_docs)

    # Context
    context = "\n\n".join([
        doc.page_content[:500]
        for doc in docs
    ])

    # Prompt
    prompt = build_prompt(context, query)

    # LLM
    llm = get_llm()

    response = llm(prompt)

    # Metrics
    latency = round(time.time() - start_time, 2)

    confidence = calculate_confidence(
        docs,
        response
    )

    sources = []

    for doc in docs:
        source = doc.metadata.get("source", "Unknown")

        if source not in sources:
            sources.append(source)

    return {
        "question": query,
        "answer": response,
        "confidence": confidence,
        "latency": latency,
        "sources": sources
    }