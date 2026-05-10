from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

DB_PATH = "db/"

def get_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)

    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    return retriever