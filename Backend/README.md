# Civifix Authentication & Authorization Module

A production-ready authentication and authorization system for the Civifix platform - a Tamil Nadu complaint management system.

## Features

✅ **Authentication**
- OTP-based registration and login
- JWT access and refresh tokens
- Secure password/OTP hashing with bcrypt
- Token expiry and refresh mechanisms

✅ **Authorization**
- Role-Based Access Control (RBAC)
- 5 built-in roles: SUPER_ADMIN, DISTRICT_ADMIN, INSPECTOR, WORKER, CITIZEN
- Custom role creation support
- Permission-based authorization
- District-wise access isolation

✅ **Security**
- Bcrypt password hashing
- JWT token encryption
- OTP rate limiting (5 attempts, 3-min cooldown)
- CORS configuration
- Exception handling
- Secure token storage

✅ **Technical**
- Async/await with FastAPI
- MongoDB with Motor driver
- Pydantic validation
- Clean architecture pattern
- Comprehensive error handling
- Logging support

## Project Structure

```
app/
├── api/v1/
│   ├── auth_routes.py          # Auth endpoints
│   ├── admin_routes.py         # Admin management
│   ├── complaint_routes.py     # Complaint management
│   └── user_routes.py          # User management
├── core/
│   ├── config.py               # Settings
│   ├── security.py             # JWT & hashing
│   ├── exceptions.py           # Custom exceptions
│   ├── constants.py            # Constants
│   ├── logger.py               # Logging setup
│   └── response.py             # Response handler
├── models/
│   ├── user_model.py           # User document
│   ├── role_model.py           # Role & permission
│   ├── otp_model.py            # OTP tracking
│   ├── token_model.py          # Token storage
│   └── complaint_model.py      # Complaint document
├── schemas/
│   ├── auth_schema.py          # Auth schemas
│   ├── user_schema.py          # User schemas
│   ├── common_schema.py        # Common schemas
│   ├── otp_schema.py           # OTP schemas
│   └── token_schema.py         # Token schemas
├── services/
│   ├── auth_service.py         # Auth logic
│   ├── user_service.py         # User management
│   ├── role_service.py         # Role management
│   ├── jwt_service.py          # JWT handling
│   ├── otp_service.py          # OTP generation
│   └── email_service.py        # Email sending
├── repositories/
│   ├── user_repository.py      # User CRUD
│   ├── role_repository.py      # Role CRUD
│   ├── otp_repository.py       # OTP tracking
│   └── token_repository.py     # Token storage
├── dependencies/
│   ├── auth_dependency.py      # JWT validation
│   ├── role_dependency.py      # RBAC checks
│   └── district_dependency.py  # District isolation
├── middleware/
│   ├── auth_middleware.py      # Auth middleware
│   └── rbac_middleware.py      # RBAC middleware
├── utils/
│   ├── validators.py           # Validation functions
│   ├── hash.py                 # Hashing utilities
│   ├── otp_generator.py        # OTP generation
│   └── helpers.py              # Helper functions
├── db/
│   ├── mongodb.py              # MongoDB connection
│   └── indexes.py              # Index creation
└── main.py                     # FastAPI app

tests/
├── test_auth.py                # Auth tests
├── test_users.py               # User tests
└── conftest.py                 # Test fixtures
```

## Installation

### Prerequisites
- Python 3.10+
- MongoDB 5.0+
- Docker & Docker Compose (optional)

### Using Docker (Recommended)

1. Clone the repository
```bash
git clone <repo-url>
cd civifix-backend
```

2. Create `.env` file from template
```bash
cp .env.example .env
```

3. Update `.env` with your configuration (change JWT secrets!)

4. Start services
```bash
docker-compose up -d
```

5. Check health
```bash
curl http://localhost:8000/health
```

### Local Installation

1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Start MongoDB
```bash
# Using Docker
docker run -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=mongo_password mongo:7.0
```

4. Create `.env` file
```bash
cp .env.example .env
```

5. Update `.env` with your local MongoDB URL

6. Run application
```bash
uvicorn app.main:app --reload
```

## Configuration

### Environment Variables

```env
# Application
ENV=development                    # development, staging, production
LOG_LEVEL=INFO                     # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Database
MONGODB_URL=mongodb://user:pass@host:27017/db
DATABASE_NAME=civifix_db

# JWT
JWT_SECRET_KEY=your-secret-key     # Change this!
JWT_REFRESH_SECRET=your-refresh-secret  # Change this!
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15     # 15 minutes
REFRESH_TOKEN_EXPIRE_DAYS=7        # 7 days

# OTP
OTP_EXPIRE_MINUTES=5               # 5 minutes
OTP_MAX_ATTEMPTS=5                 # Max verification attempts
OTP_COOLDOWN_MINUTES=3             # Cooldown after failed attempts
OTP_MAX_RESEND=3                   # Max resend requests

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=app-password
SENDER_EMAIL=noreply@civifix.in
```

## API Endpoints

### Authentication

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "name": "Shakthi",
  "email": "user@gmail.com",
  "mobile_number": "9876543210",
  "address": "Chennai",
  "district": "Chennai"
}
```

#### Verify Registration OTP
```http
POST /api/v1/auth/verify-otp
Content-Type: application/json

{
  "email": "user@gmail.com",
  "otp": "123456"
}
```

#### Login (Request OTP)
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@gmail.com"
}
```

#### Verify Login OTP
```http
POST /api/v1/auth/verify-login-otp
Content-Type: application/json

{
  "email": "user@gmail.com",
  "otp": "123456"
}
```

#### Refresh Token
```http
POST /api/v1/auth/refresh-token
Content-Type: application/json

{
  "refresh_token": "eyJ..."
}
```

#### Logout
```http
POST /api/v1/auth/logout
Authorization: Bearer <access_token>
```

#### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

### Admin Management

#### Create User/Inspector/Worker
```http
POST /api/v1/admin/users
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Inspector Name",
  "email": "inspector@gmail.com",
  "mobile_number": "9876543210",
  "role": "INSPECTOR",
  "district": "Chennai",
  "address": "Address"
}
```

#### Get District Users
```http
GET /api/v1/admin/users?skip=0&limit=20&role=INSPECTOR
Authorization: Bearer <admin_token>
```

#### Update User Role
```http
PATCH /api/v1/admin/users/{user_id}/role
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "new_role": "INSPECTOR"
}
```

#### Suspend User
```http
PATCH /api/v1/admin/users/{user_id}/suspend
Authorization: Bearer <admin_token>
```

#### Activate User
```http
PATCH /api/v1/admin/users/{user_id}/activate
Authorization: Bearer <admin_token>
```

## Roles & Permissions

### Built-in Roles

| Role | Permissions |
|------|-------------|
| **SUPER_ADMIN** | Full system access, manage all users, districts, roles |
| **DISTRICT_ADMIN** | Manage district users, create inspectors/workers, view complaints |
| **INSPECTOR** | View assigned complaints, approve/reject, assign workers |
| **WORKER** | View assigned tasks, update status, report progress |
| **CITIZEN** | View own complaints, create new complaints |

### Default Permissions

Each role has predefined permissions that can be extended. See `models/role_model.py` for the complete list.

## Testing

Run tests with pytest:

```bash
pytest app/tests/ -v
```

Run specific test:
```bash
pytest app/tests/test_auth.py::test_register_user -v
```

With coverage:
```bash
pytest app/tests/ --cov=app --cov-report=html
```

## API Documentation

### Swagger UI
```
http://localhost:8000/api/docs
```

### ReDoc
```
http://localhost:8000/api/redoc
```

## Security Checklist

- ✅ OTP hashing with bcrypt (not plaintext)
- ✅ JWT token encryption with secret keys
- ✅ Rate limiting on OTP endpoints
- ✅ Password validation with PBKDF2
- ✅ CORS configuration
- ✅ Exception handling (no stack traces in production)
- ✅ District isolation enforcement
- ✅ Role-based access control
- ✅ Input validation with Pydantic
- ✅ Token expiry enforcement

## Production Deployment

### Pre-deployment Checklist

1. Change all secret keys in `.env`
2. Enable HTTPS/SSL
3. Configure proper CORS origins
4. Set up database backups
5. Enable logging to file
6. Configure email service
7. Update MongoDB authentication
8. Enable database indexes
9. Configure rate limiting
10. Set up monitoring/alerting

### Deployment with Docker

```bash
# Build image
docker build -t civifix-backend:1.0 .

# Push to registry
docker push your-registry/civifix-backend:1.0

# Deploy
docker pull your-registry/civifix-backend:1.0
docker run -d \
  --env-file .env.production \
  -p 8000:8000 \
  --name civifix \
  your-registry/civifix-backend:1.0
```

## Troubleshooting

### MongoDB Connection Error
```bash
# Check MongoDB is running
docker ps | grep mongodb

# Check connection string in .env
MONGODB_URL=mongodb://user:pass@host:27017/db
```

### JWT Token Invalid
- Ensure JWT_SECRET_KEY hasn't changed
- Check token hasn't expired
- Verify Authorization header format: `Bearer <token>`

### OTP Not Received
- Check email service configuration
- Verify SMTP credentials
- Check logs for email service errors

### District Access Denied
- Verify user district matches resource district
- Super admin can access all districts
- Other roles restricted to their own district

## Performance Optimization

- Database indexes on frequently queried fields ✅
- MongoDB connection pooling via Motor
- Async/await for non-blocking operations
- Response caching ready (implement Redis)
- Pagination support on list endpoints

## Contributing

1. Create feature branch
2. Add tests
3. Update documentation
4. Submit pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Create GitHub issue
- Contact: support@civifix.in

---

**Version**: 1.0.0  
**Last Updated**: 2024-05-20  
**Status**: Production Ready
