from sentence_transformers import CrossEncoder

# Load once (global)
reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_documents(query, docs, top_k=5):
    pairs = [(query, doc.page_content) for doc in docs]

    scores = reranker_model.predict(pairs)

    # Combine docs with scores
    scored_docs = list(zip(docs, scores))

    # Sort by score (descending)
    ranked_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)

    # Return top_k docs
    return [doc for doc, score in ranked_docs[:top_k]]