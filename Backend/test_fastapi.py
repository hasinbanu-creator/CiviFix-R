from fastapi.testclient import TestClient
from app.main import app
from app.dependencies.auth_dependency import get_current_user

def override_get_current_user():
    return {"user_id": "123", "role": "CITIZEN"}

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

response = client.post(
    "/api/v1/complaints",
    data={
        "ward_id": "507f1f77bcf86cd799439011",
        "complaint_type": "ROAD_DAMAGE",
        "description": "This is a detailed description over 10 chars",
        "latitude": 13.0,
        "longitude": 80.0,
        "priority": "MEDIUM"
    },
    files=[
        ("images", ("test1.jpg", b"123", "image/jpeg")),
        ("images", ("test2.jpg", b"123", "image/jpeg"))
    ]
)
print(response.status_code)
print(response.json())
