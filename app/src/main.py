from fastapi import FastAPI
from app.routers import root, documents
from app.src.lifespan import lifespan


def createApplication() -> FastAPI:
    # use lifespan to initialize local models or do other long running init tasks?
    application = FastAPI(lifespan=lifespan)
    application.include_router(root.router)
    application.include_router(documents.router)
    return application


app = createApplication()
