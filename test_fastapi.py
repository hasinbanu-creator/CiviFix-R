import requests

try:
    print("Testing backend...")
    res = requests.get("http://0.0.0.0:8000/api/v1/auth/me", headers={"Authorization": "Bearer BAD_TOKEN"})
    print("Status:", res.status_code)
except Exception as e:
    print("Backend unreachable", e)
