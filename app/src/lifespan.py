from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.src.rag import build_store

import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event for FastAPI to initialize resources.
    """
    print("Initializing creating the vectordb...")

    app.state.vector_store = build_store.build_vector_store()

    print("Vector store created successfully.", app.state.vector_store)

    yield

    print("Cleaning up resources...")
