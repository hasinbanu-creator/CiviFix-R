import requests

url = "http://localhost:8000/api/v1/complaints"
payload = {
    "ward_id": "123",
    "complaint_type": "ROAD_DAMAGE",
    "description": "test",
    "latitude": "0.0",
    "longitude": "0.0",
    "priority": "MEDIUM"
}
files = [
    ("images", ("test.jpg", b"123", "image/jpeg"))
]

headers = {
    "Authorization": "Bearer TEST" # Might fail auth, but we want to see if it reaches 422 for images first.
}

response = requests.post(url, data=payload, files=files)
print(response.status_code, response.text)
