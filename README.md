# TAKE-HOME - Akshay Panchavatri

## Running Locally

```sh
pip install -r requirements.txt
uvicorn app.src.main:app
```

## Docker Deployment

```sh
docker compose build
docker compose up
``` 

## Take Home - Solutions
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

### Summarize (Part 2)
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

### Question Answer - RAG Pipeline (Part 3)
```curl
curl --location 'http://127.0.0.1:8000/answer_question' \
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