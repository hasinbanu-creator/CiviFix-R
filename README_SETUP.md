# CiviFix-pdd Setup Guide

Welcome to the **CiviFix-pdd** project setup guide! This document contains everything you need to know about the architecture, tech stack, and step-by-step instructions to run the application locally.

## 📁 Project Structure

The project is structured into three main applications:

- `Backend/`: Python-based REST API serving the core application logic.
- `civifix-web/`: Web application frontend (Next.js).
- `civifix-frontend/`: Mobile application frontend (React Native/Expo).
- `selenium_tests/` & `security_tests/`: Automation testing and security vulnerabilities testing suites.

## 🛠 Tech Stack

- **Backend**: Python (FastAPI), Uvicorn, Motor (MongoDB Driver).
- **Web Frontend**: TypeScript, React, Next.js, TailwindCSS.
- **Mobile Frontend**: JavaScript, React Native, Expo.
- **Database**: MongoDB.
- **Authentication**: JWT (JSON Web Tokens) with Bcrypt hashing and OTP verification.
- **AI/ML Components**: N/A.

## 🚀 Installation & Run Instructions

### 1. Prerequisites

- Python 3.10+
- Node.js (v18+) and npm/yarn/pnpm
- MongoDB (Running locally or via Docker)

### 2. Setting up the Backend

1. **Navigate to the Backend directory**:
   ```bash
   cd Backend
   ```
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: On Windows, `uvloop` may cause installation errors. It has been removed from the `requirements.txt` for Windows compatibility).*
4. **Environment Variables**:
   Create a `.env` file in the `Backend` directory with the following variables:
   ```env
   ENV=development
   LOG_LEVEL=INFO
   MONGODB_URL=mongodb://localhost:27017/civifix_db
   DATABASE_NAME=civifix_db
   JWT_SECRET_KEY=dummy-secret-key
   JWT_REFRESH_SECRET=dummy-refresh-secret
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   REFRESH_TOKEN_EXPIRE_DAYS=7
   OTP_EXPIRE_MINUTES=5
   OTP_MAX_ATTEMPTS=5
   OTP_COOLDOWN_MINUTES=3
   OTP_MAX_RESEND=3
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=dummy-email@gmail.com
   SMTP_PASSWORD=dummy-password
   SENDER_EMAIL=noreply@civifix.in
   ```
5. **Run the Backend Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

### 3. Setting up the Web Frontend (Next.js)

1. **Navigate to the Web Frontend directory**:
   ```bash
   cd civifix-web
   ```
2. **Install Dependencies**:
   ```bash
   npm install
   ```
3. **Run the Web Server**:
   ```bash
   npm run dev
   ```

### 4. Setting up the Mobile Frontend (React Native)

1. **Navigate to the Mobile Frontend directory**:
   ```bash
   cd civifix-frontend
   ```
2. **Install Dependencies**:
   ```bash
   npm install
   ```
3. **Run the Mobile Bundler**:
   ```bash
   npx expo start
   ```

---

## 🔗 Application URLs

- **Backend API & Swagger UI**: [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)
- **Web Frontend**: [http://localhost:3000](http://localhost:3000)

## 🔑 Default Credentials & Admin Access

- The system operates using an OTP-based registration and login system.
- To use an admin account, you can create a test user through the Registration API, then manually update their role to `SUPER_ADMIN` in MongoDB, or utilize the `POST /api/v1/admin/users` endpoint provided in the API docs if you already have an admin token.

## 🛑 Common Troubleshooting

- **MongoDB Connection Error**:
  Ensure MongoDB is running on port `27017`. If using Docker, run:
  ```bash
  docker run -d -p 27017:27017 --name civifix-mongo mongo:7.0
  ```
- **uvloop Installation Error (Windows)**:
  `uvloop` is not fully supported on Windows. Remove `uvloop` from `requirements.txt` and rerun `pip install -r requirements.txt`. (This has already been fixed in this setup).
- **OTP Not Received**:
  Double-check the `SMTP_USERNAME` and `SMTP_PASSWORD` variables in your `.env` file to ensure the application can send emails properly.

## 📝 Remaining Manual Steps

1. If you don't have MongoDB installed natively or Docker running, you must install MongoDB and start the MongoDB service manually.
2. Update the `SMTP_*` values in `Backend/.env` to a valid SMTP account to receive OTP emails and login successfully.
