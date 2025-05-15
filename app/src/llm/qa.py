from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from langchain_community.vectorstores import Chroma

load_dotenv()

llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0,
    max_tokens=2000,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a medical assistant. 
     Bellow are documents from your knowledge base that are most similar to the question that the user is asking.
     {similar_docs}
     
     You will use these documents to answer the users question.
     
     RESPONSE GUIDELINES:
     - Your answers are based only on the data found in the documents in your knowledgebase
     - Do not make up any information or provide any opinions."""),
    ("human", "{question}"),
])


def answer_question(question: str, vector_store: Chroma) -> str:
    """
    Answer a question using OpenAI's GPT-4 model and knowledgebase
    """
    chain = prompt | llm

    try:
        # do a similarity search to find the most relevant documents
        top_docs = vector_store.similarity_search(question, k=3)
        print('top_docs:', top_docs)

        # Prepare source text
        context = "\n\n".join([
            f"{doc.metadata.get('title', 'Unknown')}:\n{doc.page_content}"
            for doc in top_docs
        ])

        result = chain.invoke({"question": question, "similar_docs": context})

        # Package source info
        sources = [
            {
                "id": doc.metadata.get("id"),
                "title": doc.metadata.get("title"),
                "snippet": doc.page_content[:300] + "..."
            }
            for doc in top_docs
        ]

        print('llm result:', result.content)

        return {
            "question": question,
            "answer": result.content,
            "sources": sources
        }
    except Exception as e:
        print('Error in qa:', e)
        raise e
