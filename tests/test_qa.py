import requests

response = requests.post(
    "http://127.0.0.1:8000/answer_question",
    json={"question": "What are the rehab protocols after ACL surgery?"}
)

print("Status:", response.status_code)
print("Response:", response.json())
