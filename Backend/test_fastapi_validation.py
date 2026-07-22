import asyncio
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
import httpx
import uvicorn
import threading
import time

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("Validation Error:", exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.post("/test")
async def test_endpoint(
    images: Optional[List[UploadFile]] = File(None),
):
    return {"status": "ok", "images_count": len(images) if images else 0}

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(1)

async def test_requests():
    async with httpx.AsyncClient() as client:
        # Test 1: No images
        res = await client.post("http://127.0.0.1:8001/test")
        print("No images:", res.status_code, res.json())
        
        # Test 2: One image
        files = {'images': ('test1.jpg', b'dummy content', 'image/jpeg')}
        res = await client.post("http://127.0.0.1:8001/test", files=files)
        print("One image:", res.status_code, res.json())

        # Test 3: Multiple images
        files = [
            ('images', ('test1.jpg', b'dummy content', 'image/jpeg')),
            ('images', ('test2.jpg', b'dummy content', 'image/jpeg'))
        ]
        res = await client.post("http://127.0.0.1:8001/test", files=files)
        print("Multiple images:", res.status_code, res.json())

asyncio.run(test_requests())
