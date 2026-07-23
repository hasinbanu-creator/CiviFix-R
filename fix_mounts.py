with open("Backend/app/main.py", "r") as f:
    content = f.read()

# Add the /api/v1/uploads alias
if "/api/v1/uploads" not in content:
    content = content.replace(
        'app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")',
        'app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")\napp.mount("/api/v1/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="api_v1_uploads")'
    )
    with open("Backend/app/main.py", "w") as f:
        f.write(content)
    print("Mounted /api/v1/uploads.")
else:
    print("Already mounted.")
