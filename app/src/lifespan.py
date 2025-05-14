from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.src.rag import build_store

from sqlalchemy import text
from app.db.database import create_documents_table_if_not_exists, table_exists, load_documents

import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event for FastAPI to initialize resources.
    """

    if table_exists():
        print("Table already exists.")
    else:
        print("Table does not exist. Creating it...")
        create_documents_table_if_not_exists()
        print("Table created successfully.")
        print("Populating the table with initial data...")
        load_documents()

    print("Initializing creating the vectordb...")

    app.state.vector_store = build_store.build_vector_store()

    print("Vector store created successfully.", app.state.vector_store)

    yield

    print("Cleaning up resources...")
