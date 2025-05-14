import os
from sqlalchemy import create_engine, text
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from langchain.schema import Document

from app.db.database import engine


VECTOR_DIR = "./chroma_db"


def fetch_documents():
    """
    Build a vector store from the database.
    """
    # Create a session
    with engine.connect() as connection:
        # Fetch all documents from the database
        result = connection.execute(
            text("SELECT id, title, content FROM documents"))
        documents = result.fetchall()
        return documents


def build_vector_store():
    """
    Build a vector store from the database documents.
    """

    print("🔄 Building vector store...")

    # Fetch documents from the database
    documents = fetch_documents()

    # Convert to langchain Document format
    docs = [
        Document(page_content=doc.content, metadata={
                 "id": doc.id, "title": doc.title})
        for doc in documents
    ]

    # Split the documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)

    # Create embeddings
    embeddings = OpenAIEmbeddings()

    # Create a vector store
    vector_store = Chroma.from_documents(split_docs, embeddings)

    print("✅ Chroma vector store built and persisted.")

    return vector_store
