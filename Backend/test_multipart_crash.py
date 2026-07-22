import httpx
import asyncio
from app.core.security import SecurityUtils

async def test():
    url = "http://192.168.1.8:8000/api/v1/complaints"
    
    # Create valid token
    token = SecurityUtils.create_access_token({"sub": "7e1152c5-9176-47b7-b77d-2489a8321d61", "role": "CITIZEN", "user_id": "7e1152c5-9176-47b7-b77d-2489a8321d61"})
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    payload = {
        "ward_id": "test_ward",
        "complaint_type": "ROAD_DAMAGE",
        "description": "test_desc12345678",
        "latitude": "10.0",
        "longitude": "20.0"
    }
    files = [
        ("images", ("test.jpg", b"fake_image_data", "image/jpeg"))
    ]
    try:
        async with httpx.AsyncClient() as client:
            print("Sending request...")
            response = await client.post(url, headers=headers, data=payload, files=files)
            print("Status:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(test())
