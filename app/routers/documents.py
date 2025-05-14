from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from app.db.database import session_local
from app.src.llm import summarize
from app.src.llm import qa

from sqlalchemy.orm import Session
from app.models.document import Document

router = APIRouter()


class NoteInput(BaseModel):
    note: str


class QuestionInput(BaseModel):
    question: str


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


@router.post("/answer_question")
def answer_question(request: Request, question: QuestionInput):
    """
    Answer a question based on a medical note using OpenAI's GPT-4 model.

    Args:
        question (str): The medical note to analyze.

    Returns:
        str: The answer to the question based on the medical note.
    """
    if not question:
        print("❌ No question provided in request.")
        raise HTTPException(status_code=400, detail="Question is required")

    print("📥 Received question:")
    print(question.question)

    try:
        print("🤖 Sending question to RAG...")
        vector_store = request.app.state.vector_store
        answer = qa.answer_question(
            question.question, vector_store)

        if not answer:
            print("❌ LLM returned an empty or null answer.")
            raise HTTPException(
                status_code=500, detail="Error: Unable to analyze the note.")

        print("✅ LLM analysis successful.")
        print("📝 Answer:", answer)
        return {"answer": answer}

    except Exception as e:
        print('Error in answer:', e)
        raise HTTPException(
            status_code=500, detail=e)


@router.post("/summarize_note")
def summarize_note(note: NoteInput):
    """
    Summarize a medical note using OpenAI's GPT-4 model.

    Args:
        note (str): The medical note to summarize.

    Returns:
        str: The summarized version of the medical note.
    """
    if not note:
        print("❌ No note provided in request.")
        raise HTTPException(status_code=400, detail="Note is required")

    print("📥 Received note for summarization:")
    print(note.note)

    try:
        print("🤖 Sending note to LLM for summarization...")
        note_summary = summarize.summarize_note(note.note)

        if not note_summary:
            print("❌ LLM returned an empty or null summary.")
            raise HTTPException(
                status_code=500, detail="Error: Unable to summarize the note.")

        print("✅ LLM summarization successful.")
        print("📝 Summary:", note_summary)
        return {"summary": note_summary}

    except Exception as e:
        print('Error in summarize:', e)
        raise HTTPException(
            status_code=500, detail=e)
