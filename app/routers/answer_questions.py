from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from app.src.llm import qa

router = APIRouter()


class QuestionInput(BaseModel):
    question: str


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
