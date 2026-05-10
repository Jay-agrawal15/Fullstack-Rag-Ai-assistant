from langchain.llms import Ollama

def get_llm():
    return Ollama(
        model="llama3:8b",
        temperature=0.2
    )