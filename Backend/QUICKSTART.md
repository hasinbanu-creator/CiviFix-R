# Civifix Authentication Module - Quick Start Guide

## 30-Second Setup

### 1. Using Docker (Easiest)
```bash
docker-compose up -d
# Wait for MongoDB to start...
# API available at http://localhost:8000
```

### 2. Local Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start MongoDB (separate terminal)
docker run -p 27017:27017 mongo:7.0

# Run app
uvicorn app.main:app --reload
```

## Test the API

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "mobile_number": "9876543210",
    "address": "123 Main St",
    "district": "Chennai"
  }'
```

### 2. Verify OTP (Check logs for OTP)
```bash
curl -X POST http://localhost:8000/api/v1/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "otp": "123456"
  }'
```

### 3. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com"
  }'
```

### 4. Use Token
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## API Documentation

Visit: **http://localhost:8000/api/docs**

## Important Files

- **README.md** - Complete documentation
- **.env** - Configuration (update before deployment)
- **docker-compose.yml** - Docker setup
- **requirements.txt** - Python dependencies

## Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/auth/register` | POST | Register new user |
| `/api/v1/auth/verify-otp` | POST | Verify OTP |
| `/api/v1/auth/login` | POST | Request login OTP |
| `/api/v1/auth/verify-login-otp` | POST | Verify login |
| `/api/v1/auth/refresh-token` | POST | Refresh access token |
| `/api/v1/auth/logout` | POST | Logout |
| `/api/v1/auth/me` | GET | Get current user |
| `/api/v1/admin/users` | POST | Create admin/inspector |
| `/api/v1/admin/users` | GET | List users |

## Roles Available

- **CITIZEN** - Regular users
- **WORKER** - Field workers
- **INSPECTOR** - Complaint inspectors
- **DISTRICT_ADMIN** - District administrators
- **SUPER_ADMIN** - System administrators

## Default Credentials

For development/testing:
- Use any email address
- OTP is logged in console (dev mode)
- Each registration creates a CITIZEN account

## Common Issues & Solutions

### "Connection refused" Error
**Solution**: Ensure MongoDB is running
```bash
# Check MongoDB
docker ps | grep mongodb
# Or start it
docker run -d -p 27017:27017 mongo:7.0
```

### JWT Token Errors
**Solution**: Token may have expired (15 min expiry)
- Use refresh endpoint to get new token
- Or login again

### OTP Issues
**Solution**: Check console logs for OTP
- In dev mode, OTP is printed to console
- OTP expires in 5 minutes
- Max 5 attempts

## Next Steps

1. **Read** `README.md` for detailed documentation
2. **Configure** `.env` with your settings
3. **Test** all endpoints using Swagger UI
4. **Create** admin users via `/api/v1/admin/users`
5. **Deploy** using docker-compose or Kubernetes

## Security Notes

For **PRODUCTION**:
- ✅ Change JWT_SECRET_KEY in `.env`
- ✅ Change JWT_REFRESH_SECRET in `.env`
- ✅ Set ENV=production
- ✅ Enable HTTPS/SSL
- ✅ Configure proper CORS
- ✅ Setup email service
- ✅ Enable database backups

---

**Questions?** Check `README.md` or `IMPLEMENTATION_SUMMARY.md`
