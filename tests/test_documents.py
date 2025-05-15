import requests

response = requests.get(
    "http://127.0.0.1:8000/documents")

print("Status:", response.status_code)
print("Response:", response.json())
