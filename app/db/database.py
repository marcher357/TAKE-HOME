import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from app.models.document import Document

DB_USER = os.getenv("MYSQL_USER", "myuser")
DB_PASS = os.getenv("MYSQL_PASSWORD", "mypassword")
DB_HOST = os.getenv("MYSQL_HOST", "mysql")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE", "mydb")

env = os.getenv("ENV", "dev")


print("Environment variables:", env)

if env == "dev":
    DB_URL = "mysql+mysqlconnector://myuser:mypassword@localhost/mydb"  # -> running locally
else:
    DB_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(DB_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "../documents")


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


def create_documents_table_if_not_exists():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS documents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                content TEXT
            );
        """))


def table_exists() -> bool:
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'mydb' AND table_name = 'documents';
        """))
        return result.scalar() > 0
