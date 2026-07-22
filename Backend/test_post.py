import httpx
import asyncio

async def test():
    url = "http://192.168.1.8:8000/api/v1/complaints"
    
    payload = {
        "ward_id": "test_ward",
        "complaint_type": "test_type",
        "description": "test_desc",
        "latitude": "10.0",
        "longitude": "20.0"
    }
    files = [
        ("images", ("test.jpg", b"fake_image_data", "image/jpeg"))
    ]
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=payload, files=files)
            print("Status:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print("Error:", e)

asyncio.run(test())
