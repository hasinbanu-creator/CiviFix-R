import urllib.request
import json
import urllib.parse

def req(url, data, token=None):
    if data:
        data = json.dumps(data).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())

# 1. Login
login = req("http://127.0.0.1:8000/api/v1/auth/login", {"email": "citizen@example.com"})
print("Login:", login)

# 2. Verify
verify = req("http://127.0.0.1:8000/api/v1/auth/verify", {"email": "citizen@example.com", "otp": "123456"})
print("Verify:", verify)
token = verify["data"]["access_token"]

# 3. Create complaint (multipart form-data without file)
import mimetypes
import uuid

boundary = uuid.uuid4().hex
body = bytearray()
form_data = {
    "ward_id": "60d5ecb8b392d21234567890",
    "complaint_type": "GARBAGE",
    "description": "Garbage hasn't been collected for a week",
    "priority": "MEDIUM",
    "latitude": "12.9716",
    "longitude": "77.5946",
    "address": "123 MG Road"
}
for key, value in form_data.items():
    body.extend(f"--{boundary}\r\n".encode('utf-8'))
    body.extend(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode('utf-8'))
    body.extend(f"{value}\r\n".encode('utf-8'))
body.extend(f"--{boundary}--\r\n".encode('utf-8'))

headers = {
    'Content-Type': f'multipart/form-data; boundary={boundary}',
    'Authorization': f'Bearer {token}'
}
req_obj = urllib.request.Request("http://127.0.0.1:8000/api/v1/complaints/", data=bytes(body), headers=headers, method='POST')
try:
    with urllib.request.urlopen(req_obj) as response:
        print("Success:", json.loads(response.read().decode()))
except urllib.error.HTTPError as e:
    print("Error:", json.loads(e.read().decode()))
