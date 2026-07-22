import requests
import json
import uuid
import os

BASE_URL = "http://0.0.0.0:8000/api/v1"

# Create dummy image
with open("test_img.jpg", "wb") as f:
    f.write(b"dummy image content")

print("--- 1. Login ---")
res = requests.post(f"{BASE_URL}/auth/login", json={"email": "hasinbanu.creator@gmail.com"})
print(res.status_code)
print(res.text[:100])
if res.status_code != 200:
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": "inspector@example.com"})
    print("Fallback Login:", res.status_code)

try:
    token = res.json()["data"]["access_token"]
except:
    token = "TEST_TOKEN"
    print("Failed to get token")

print("\n--- 2. Create Complaint ---")
headers = {"Authorization": f"Bearer {token}"}
files = [
    ("images", ("test_img.jpg", open("test_img.jpg", "rb"), "image/jpeg"))
]
data = {
    "ward_id": "test_ward",
    "complaint_type": "Roads",
    "description": "Test complaint",
    "latitude": "12.9716",
    "longitude": "77.5946",
    "priority": "High"
}

res = requests.post(f"{BASE_URL}/complaints", headers=headers, data=data, files=files)
print("Create Complaint Status:", res.status_code)
print("Response:", res.text[:200])

print("\n--- 3. Inspector Resolve ---")
try:
    complaint_id = res.json()["data"]["_id"]
except:
    complaint_id = "test_id"

resolve_files = [
    ("images", ("test_img.jpg", open("test_img.jpg", "rb"), "image/jpeg"))
]
resolve_data = {
    "note": "Resolved issue"
}
res = requests.put(f"{BASE_URL}/inspector/complaints/{complaint_id}/resolve", headers=headers, data=resolve_data, files=resolve_files)
print("Resolve Status:", res.status_code)
print("Response:", res.text[:200])

os.remove("test_img.jpg")
