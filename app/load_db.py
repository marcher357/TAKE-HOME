# load documents into the database
import os
from sqlalchemy.orm import Session
from models.document import Document
from db.database import session_local

DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "./documents")


def load_documents():
    session: Session = session_local()

    print("Loading documents into the database...", DOCUMENTS_DIR)

    try:
        for filename in os.listdir(DOCUMENTS_DIR):
            if filename.endswith(".txt"):
                file_path = os.path.join(DOCUMENTS_DIR, filename)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                doc = Document(title=filename, content=content)
                print(doc.id, doc.title)
                session.add(doc)

        session.commit()
        print("✅ Documents loaded into the database.")

    except Exception as e:
        session.rollback()
        print("❌ Failed to load documents:", e, DOCUMENTS_DIR)

    finally:
        session.close()


if __name__ == "__main__":
    load_documents()
