"""Tests for authentication endpoints"""
import pytest
from httpx import AsyncClient
from app.main import app
from datetime import datetime


@pytest.mark.asyncio
async def test_register_user():
    """Test user registration"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "mobile_number": "9876543210",
                "address": "Test Address",
                "district": "Chennai"
            }
        )
        
        assert response.status_code in [200, 201]
        data = response.json()
        assert data.get("success") is True
        assert "user_id" in data.get("data", {})


@pytest.mark.asyncio
async def test_register_duplicate_email():
    """Test duplicate email registration"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Register first user
        await client.post(
            "/api/v1/auth/register",
            json={
                "name": "User 1",
                "email": "duplicate@example.com",
                "mobile_number": "9876543210",
                "address": "Address",
                "district": "Chennai"
            }
        )
        
        # Try to register with same email
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "name": "User 2",
                "email": "duplicate@example.com",
                "mobile_number": "9876543211",
                "address": "Address 2",
                "district": "Chennai"
            }
        )
        
        assert response.status_code in [400, 409]
        data = response.json()
        assert data.get("success") is False


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data.get("success") is True
        assert "Civifix Backend Running" in data.get("message", "")
