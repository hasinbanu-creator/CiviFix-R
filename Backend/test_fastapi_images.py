import asyncio
from fastapi import FastAPI, UploadFile, File, Form
from typing import List, Optional
from fastapi.testclient import TestClient

app = FastAPI()

@app.post("/test1")
async def test1(images: Optional[List[UploadFile]] = File(None)):
    return {"status": "ok"}

@app.post("/test2")
async def test2(images: List[UploadFile] = File(default=[])):
    return {"status": "ok"}

client = TestClient(app)

def test_single_file_test1():
    res = client.post("/test1", files={"images": ("test.jpg", b"abc")})
    print("test1 (Optional[List[UploadFile]] = File(None)): ", res.status_code, res.json())

def test_single_file_test2():
    res = client.post("/test2", files={"images": ("test.jpg", b"abc")})
    print("test2 (List[UploadFile] = File(default=[])): ", res.status_code, res.json())

test_single_file_test1()
test_single_file_test2()
