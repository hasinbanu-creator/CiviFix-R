from app.core.response import _enrich_image_urls
data = {
    "complaints": [
        {"id": 1, "image_urls": ["/uploads/123/images/img.jpg"]},
        {"id": 2, "image_urls": ["https://s3.amazonaws.com/old_bucket/img.jpg"]}
    ]
}
res = _enrich_image_urls(data, "http://localhost:8000/")
print(res)
