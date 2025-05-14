from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0,
    max_tokens=2000,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a medical assistant. Summarize the following medical note provided by the user."),
    ("human", "{note}"),
])


def summarize_note(note: str) -> str:
    """
    Summarize a medical note using OpenAI's GPT-4 model.
    """
    chain = prompt | llm

    try:
        result = chain.invoke({"note": note})

        print('llm result:', result.content)
        return result.content
    except Exception as e:
        print('Error in summarize:', e)
        return "Error: Unable to summarize the note."
