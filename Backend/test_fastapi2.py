from fastapi import FastAPI, Form, File, UploadFile
from typing import List, Optional
from fastapi.testclient import TestClient

app = FastAPI()

@app.post("/test")
async def test_endpoint(images: Optional[List[UploadFile]] = File(None)):
    return {"images": len(images) if images else 0}

client = TestClient(app)

response = client.post("/test", files=[("images", ("test.jpg", b"123", "image/jpeg"))])
print("1 file:", response.status_code, response.text)

response = client.post("/test", files=[("images", ("test1.jpg", b"1", "image/jpeg")), ("images", ("test2.jpg", b"2", "image/jpeg"))])
print("2 files:", response.status_code, response.text)
