# 🔍 EVA Agent – A Modular Python AI Agent with LangChain & FastAPI

A flexible and scalable AI agent built using FastAPI, LangChain, ChromaDB, and Docker — designed for real-world question answering, summarization, and semantic document search.

---

## 🚀 Highlights

### 🔧 Modular Architecture
- `app/routers/`: Routes for document ingestion, summarization, and Q&A.
- `app/src/`: Core agent logic, lifecycle management, and utility modules.
- `app/src/llm/`: LangChain-powered LLM interface layer (model-agnostic).

### ⚙️ Lifecycle-aware Startup
- Initializes vector store and MySQL using FastAPI’s `lifespan` context.
- Ensures shared state (like ChromaDB and SQL sessions) is bootstrapped before serving traffic.

### 🧠 LLM Abstraction with LangChain
- Supports easy swapping between OpenAI, Claude, Gemini, or LLaMA.
- Custom RAG pipeline (instead of LangChain’s default) to keep full control.

---

## 🗄️ Database & Storage

- **Relational Layer**: MySQL via SQLAlchemy (Dockerized)
- **Vector Store**: Embedded **ChromaDB** for lightweight local RAG
- 💡 Designed to optionally swap in **Pinecone**, **FAISS**, or **Weaviate** if needed for scale

---

## 🧪 Testable from Day One

Test suite available in `/tests`:
- `test_documents.py` – document ingestion & listing
- `test_llm.py` – summarization and language model sanity tests
- `test_qa.py` – full RAG pipeline question-answering

---
### Design Philosophy & Tech Choices

#### Modular and Maintainable Architecture

The project is structured for clarity and scalability, with separate directories for:

- `app/routers/`: Contains API route handlers for question answering, summarization, and document management.
- `app/src/`: Contains core logic and lifecycle hooks, including vector store setup and model initialization.
- `app/src/llm/`: Contains language model abstraction utilities (currently using LangChain).

The FastAPI `lifespan` context manager is used to initialize long-lived resources (like vector stores) during application startup. This ensures shared state is ready before requests are handled, enabling clean separation of concerns and robust startup logic.

`lifespan` also initialized the mysql database if required.

#### Language Model Abstraction with LangChain

LangChain provides a unified interface to interact with various LLMs. It's used here to:

- Allow easy swapping of backend models (e.g., OpenAI, Claude, LLaMA, Gemini)
- I could have also implemented RAG with the available langchain tooling but, I prefered to do it myself. 

This abstraction helps ensure the system is model-agnostic and adaptable to evolving LLM tooling.

#### Database Design & Preferences

The application currently uses a **MySQL** database managed via Docker and accessed using SQLAlchemy. It’s suitable for handling structured medical documents in development. However, for scalability and flexibility, a NoSQL alternative might be preferred in production:

- **Firebase Cloud Firestore**: Serverless, great for real-time updates and mobile integration
- **Amazon DynamoDB**: Scalable and highly available with predictable performance
- **Redis with RedisJSON**: Ultra-fast storage for semi-structured data

These options would be more suitable for storing diverse note formats, flexible schemas, and high-throughput workloads.

#### Vector Store Integration

The project uses **ChromaDB** as an embedded vector store to support RAG workflows and semantic search. It was chosen for its ease of use and local storage capabilities. 

Other options like **FAISS** and **Pinecone** are supported by LangChain and could be integrated with minimal changes if scaling or cloud hosting is required. FAISS presented installation challenges locally, which is why ChromaDB was used for prototyping.


### ENV Variables
create a .env file and place it in the project root.
```sh
OPENAI_API_KEY=...

MYSQL_USER=myuser
MYSQL_PASSWORD=mypassword
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DATABASE=mydb

ENV=dev
```

## Running Locally

```sh
pip install -r requirements.txt
uvicorn app.src.main:app
```

### Local Testing

Some files for local testing are included in the `/tests` folder

Part 1 -> `test_documents.py`
Part 2 -> `test_llm.py`
Part 3 -> `test_qa.py`

### Containerized Deployment with Docker

This project includes a full Dockerized setup for local development and deployment using **Docker Compose**. It defines two core services:

---

#### `fastapi` — Application Service

- **Base Image:** `python:3.11-slim`
- **Build Context:** Uses the local `Dockerfile` to install dependencies and copy application code.
- **Exposed Port:** `8000` (mapped from host to container)
- **Entrypoint:** Runs `uvicorn` with the FastAPI app entry point at `app.src.main:app`.
- **Wait Script:** Uses a custom `wait-for-mysql.sh` script that blocks FastAPI startup until MySQL is ready.
- **Volumes:**
  - `./app:/app/app` — Mounts source code for hot reloading in development
  - `chroma_data:/app/chroma_db` — Persists the embedded ChromaDB vector store
- **Environment:**
  - Reads from a `.env` file (e.g., `MYSQL_USER`, `OPENAI_API_KEY`)
  - Injects these into the container at runtime
- **Depends On:**
  - Ensures MySQL container starts first

---

#### `mysql` — Relational Database Service

- **Image:** `mysql:8.0`
- **Exposed Port:** `3306`
- **Initial Data:**
  - Runs `./init.sql` on startup via `docker-entrypoint-initdb.d`
- **Volumes:**
  - `mysql_data:/var/lib/mysql` — Persists MySQL database
- **Environment:**
  - Sets root and user credentials (`MYSQL_ROOT_PASSWORD`, `MYSQL_USER`, etc.)

### Startup Coordination with `wait-for-mysql.sh`

To ensure that FastAPI doesn't start before the MySQL container is ready to accept connections, this project uses a shell script named `wait-for-mysql.sh`.

## Docker Deployment

```sh
docker compose build
docker compose up
``` 

## Testing using docker

curl scripts are provided to test parts 1-3 using the docker deployment.

*NOTE*: Docker deployment presented some interesting problems as the mysql database was deployed as its own service and needed to be accessible for the fastapi service to load correctly. Before the fastapi service could be deployed, the mysql service had to *complete starting*. To acommplish this I wrote a shell script to wait for the mydqwl service to start prior to starting the fastapi service. 

### Health Endpoint (Part - 1a)
```curl
curl --location 'http://0.0.0.0:8000/health'
```
#### Response
```json
{
    "status": "OK"
}
```

### Documents Endpoint (Part - 1b)
```curl
curl --location 'http://0.0.0.0:8000/documents'
```
#### Response
```json
{
    "document_ids": [
        1,
        2,
        3,
        4,
        5,
        6
    ]
}
```

### Summarize
```curl
curl --location 'http://0.0.0.0:8000/summarize_note' \
--header 'Content-Type: application/json' \
--data '{
    "note": "SOAP Note - Encounter Date: 2024-06-20 (Physical Therapy Appointment)\nPatient: Emily Williams - DOB 1996-12-02\nS:\nPt returns for initial PT appt. approx. 6 months post left knee arthroscopy for meniscal repair. Reports overall satisfaction with surgical outcome, minimal daily pain; intermittent stiffness and mild discomfort noted mainly after extended periods of sitting or physical activity. Pt keen on resuming full recreational activity (running, yoga). Currently performing routine strengthening and stretching at home, compliant with recommendations thus far.\n\nO:\nVitals:\n\nBP: 116/72 mmHg\nHR: 68 bpm\nLeft knee assessment:\n\nSurgical scars fully healed, no swelling, warmth or erythema.\nKnee ROM improved,\n    0° to 130°, minor end-range stiffness in flexion.\nQuadriceps & hamstring strength improved,\n    4+/5\nFunctional assessment: mild difficulty/pain w/ deep squatting; normal gait and balance, no instability.\n\nA:\n\nS/P left knee arthroscopy, excellent recovery, minimal residual stiffness and mild strength deficits\nPt motivated, good candidate for return to previous activities after specific strengthening and mobility protocols.\n\nP:\n\nInitiate formal PT program:\nStrengthening (quad/hamstring/gluteal activation & stability exercises)\nStretching/mobility & proprioception activities\nIncremental running protocol as tolerated by progress over next 4-6 weeks.\nPT sessions: 2x weekly for 6 weeks.\nHome exercises provided today, pt educated and demonstrated good understanding.\nRTC as scheduled for reassessment at end of PT regimen or sooner if issues arise.\nNo Rx prescribed today.\n\nSigned:\nAlex Carter, PT, DPT\nPhysical Therapist"
}'
```
#### Response
```json
{
    "summary": "Emily Williams attended her initial physical therapy appointment approximately six months after undergoing left knee arthroscopy for meniscal repair. She reports satisfaction with the surgical outcome, experiencing minimal daily pain, with intermittent stiffness and mild discomfort after prolonged sitting or physical activity. Emily is eager to resume running and yoga. Her home exercise compliance has been good.\n\nUpon examination, her surgical scars are healed, and there is no swelling or warmth. Her knee range of motion has improved, with minor stiffness at the end of flexion. Quadriceps and hamstring strength are rated at 4+/5. She experiences mild difficulty and pain with deep squatting but has a normal gait and balance without instability.\n\nThe assessment indicates an excellent recovery with minimal stiffness and mild strength deficits. Emily is motivated and a good candidate for returning to her previous activities. The plan includes initiating a formal physical therapy program focusing on strengthening, stretching, mobility, and proprioception exercises, along with an incremental running protocol over the next 4-6 weeks. She will attend PT sessions twice weekly for six weeks and has been provided with home exercises. No medications were prescribed. Emily will return for reassessment at the end of the PT regimen or sooner if needed."
}
```

### Question Answer - RAG Pipelie
```curl
curl --location 'http://0.0.0.0:8000/answer_question' \
--header 'Content-Type: application/json' \
--data '{"question": "What are the rehab protocols after ACL surgery?"}'
```
#### Response
```json
{
    "answer": {
        "question": "What are the rehab protocols after ACL surgery?",
        "answer": "Rehabilitation protocols after ACL (anterior cruciate ligament) surgery typically involve several phases, each with specific goals and exercises to ensure proper healing and return to activity. Here is a general outline of the rehab process:\n\n1. **Immediate Post-Operative Phase (0-2 weeks):**\n   - Focus on reducing swelling and pain.\n   - Begin gentle range of motion (ROM) exercises.\n   - Use crutches to assist with walking.\n   - Start quadriceps activation exercises (e.g., quad sets, straight leg raises).\n\n2. **Early Rehabilitation Phase (2-6 weeks):**\n   - Gradually increase weight-bearing as tolerated.\n   - Continue ROM exercises to achieve full extension and flexion.\n   - Begin closed kinetic chain exercises (e.g., mini squats, leg presses).\n   - Incorporate balance and proprioception exercises.\n\n3. **Strengthening Phase (6-12 weeks):**\n   - Increase intensity of strengthening exercises for quadriceps, hamstrings, and gluteal muscles.\n   - Introduce more dynamic exercises (e.g., step-ups, lunges).\n   - Continue to work on balance and proprioception.\n\n4. **Advanced Strengthening and Neuromuscular Control Phase (3-6 months):**\n   - Focus on sport-specific drills and exercises.\n   - Increase agility and plyometric exercises.\n   - Begin running and jumping activities as tolerated.\n\n5. **Return to Sport Phase (6-12 months):**\n   - Gradual return to full sports participation.\n   - Continue with maintenance exercises to ensure strength and stability.\n   - Regular assessment by a physical therapist to monitor progress and adjust the program as needed.\n\nIt's important to note that the specific timeline and exercises may vary based on individual progress, surgeon recommendations, and physical therapist guidance. Always follow the advice of healthcare professionals involved in your care.",
        "sources": [
            {
                "id": 4,
                "title": "soap_06.txt",
                "snippet": "S/P left knee arthroscopy, excellent recovery, minimal residual stiffness and mild strength deficits\nPt motivated, good candidate for return to previous activities after specific strengthening and mobility protocols.\nP:\n\nInitiate formal PT program:\nStrengthening (quad/hamstring/gluteal activation & ..."
            },
            {
                "id": 5,
                "title": "soap_05.txt",
                "snippet": "A:\n\nStatus-post left knee arthroscopic meniscal repair, healing well\nExpected mild discomfort, consistent with post-op recovery period\nP:\n\nContinue ibuprofen 400mg-600mg PO q6-8h PRN for pain/discomfort\nRemove sutures today.\nCleared to gradually increase ROM and begin physical therapy program (refer..."
            },
            {
                "id": 4,
                "title": "soap_06.txt",
                "snippet": "SOAP Note - Encounter Date: 2024-06-20 (Physical Therapy Appointment)\nPatient: Emily Williams - DOB 1996-12-02\nS:\nPt returns for initial PT appt. approx. 6 months post left knee arthroscopy for meniscal repair. Reports overall satisfaction with surgical outcome, minimal daily pain; intermittent stif..."
            }
        ]
    }
}
```
