from fastapi import FastAPI
from app.routers import root, documents


def createApplication() -> FastAPI:
    # use lifespan to initialize local models or do other long running init tasks?
    application = FastAPI()
    application.include_router(root.router)
    application.include_router(documents.router)
    return application


app = createApplication()
