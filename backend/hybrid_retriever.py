from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from rank_bm25 import BM25Okapi

DB_PATH = "db/"


def get_hybrid_results(query):
    
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    # ---------------- FAISS SEARCH ----------------
    faiss_docs = db.similarity_search(query, k=5)

    # ---------------- BM25 SEARCH ----------------
    all_docs = db.similarity_search("", k=100)

    corpus = [doc.page_content for doc in all_docs]

    tokenized_corpus = [
        doc.split() for doc in corpus
    ]

    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query = query.split()

    bm25_scores = bm25.get_scores(tokenized_query)

    top_n = 5

    bm25_indices = sorted(
        range(len(bm25_scores)),
        key=lambda i: bm25_scores[i],
        reverse=True
    )[:top_n]

    bm25_docs = [all_docs[i] for i in bm25_indices]

    # ---------------- MERGE RESULTS ----------------
    combined_docs = faiss_docs + bm25_docs

    unique_docs = []
    seen = set()

    for doc in combined_docs:

        if doc.page_content not in seen:
            unique_docs.append(doc)
            seen.add(doc.page_content)

    return unique_docs[:5]