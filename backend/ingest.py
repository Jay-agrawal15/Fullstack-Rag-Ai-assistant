from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

DATA_PATH = "data/"
DB_PATH = "db/"

def load_documents():
    documents = []
    
    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_PATH, file))
            documents.extend(loader.load())
    
    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_documents(documents)


def create_vector_db(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs = {'device':'cuda'}        
    )

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(DB_PATH)


def main():
    print("Loading documents...")
    docs = load_documents()

    print(f"Loaded {len(docs)} pages")

    print("Splitting documents...")
    chunks = split_documents(docs)

    print(f"Created {len(chunks)} chunks")

    print("Creating vector database...")
    create_vector_db(chunks)

    print("Vector DB created successfully!")


if __name__ == "__main__":
    main()