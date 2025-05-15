from fastapi import APIRouter, Depends, HTTPException, Request

from app.db.database import session_local

from sqlalchemy.orm import Session
from app.models.document import Document

router = APIRouter()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@router.get("/documents")
def get_document_ids(db: Session = Depends(get_db)):
    document_ids = db.query(Document.id).all()
    return {"document_ids": [doc.id for doc in document_ids]}
