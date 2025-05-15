from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from app.src.llm import summarize

router = APIRouter()


class NoteInput(BaseModel):
    note: str


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
