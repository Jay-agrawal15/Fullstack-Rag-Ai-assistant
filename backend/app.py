import streamlit as st
import time

from backend.hybrid_retriever import get_hybrid_results
from backend.llm import get_llm
from backend.utils.prompts import build_prompt
from backend.reranker import rerank_documents


def calculate_confidence(docs,response):
    if not docs:
        return 0.0
    
    if "don't know" in response.lower():
        return 0.2
    
    score = len(docs) / 3   # max docs = 3
    return round(score, 2)


st.title("AI Tech Knowledge Assistant (RAG)")

query = st.text_input("Ask your question:")

if query:
    start_time =  time.time()  #start time
    raw_docs = get_hybrid_results(query)
    docs = rerank_documents(query, raw_docs)

    context = "\n\n".join([doc.page_content[:400] for doc in docs])

    prompt = build_prompt(context, query)

    llm = get_llm()
    response = llm(prompt)
    
    #end time
    end_time = time.time()
    latency = round(end_time - start_time,2)
    
    confidence = calculate_confidence(docs,response)

    st.write("### Answer:")
    st.write(response)
    
    st.write('### Confidence Score:')
    st.write(confidence)

    st.write('### Latency:')
    st.write(latency)
    
    
    st.write("### Sources:")
    for doc in docs:
        st.write(doc.metadata.get("source", "Unknown"))
        
   