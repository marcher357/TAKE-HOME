from fastapi import FastAPI
from app.routers import root, documents, answer_questions, summarize
from app.src.lifespan import lifespan


def createApplication() -> FastAPI:
    # use lifespan to initialize local models or do other long running init tasks?
    application = FastAPI(lifespan=lifespan)
    application.include_router(root.router)
    application.include_router(documents.router)
    application.include_router(summarize.router)
    application.include_router(answer_questions.router)
    return application


app = createApplication()
