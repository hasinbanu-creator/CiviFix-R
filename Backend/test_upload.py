from pathlib import Path

from app.api.v1 import upload_routes


def test_build_user_upload_dir_uses_assets_user_images_structure():
    upload_dir = upload_routes.build_user_upload_dir("user-123")

    assert upload_dir.name == "images"
    assert upload_dir.parent.name == "user-123"
    assert upload_dir.parent.parent.name == "assets"
    assert upload_dir.parts[-3:] == ("assets", "user-123", "images")
