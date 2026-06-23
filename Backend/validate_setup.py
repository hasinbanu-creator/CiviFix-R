#!/usr/bin/env python3
"""
Validate Civifix Auth Module Setup
"""
import sys
import os
from pathlib import Path

def check_file_exists(path, description):
    """Check if file exists"""
    if Path(path).exists():
        print(f"  ✅ {description}")
        return True
    else:
        print(f"  ❌ {description} - NOT FOUND")
        return False

def check_directory_exists(path, description):
    """Check if directory exists"""
    if Path(path).is_dir():
        print(f"  ✅ {description}")
        return True
    else:
        print(f"  ❌ {description} - NOT FOUND")
        return False

def main():
    print("\n" + "=" * 70)
    print("CIVIFIX AUTHENTICATION MODULE - SETUP VALIDATION")
    print("=" * 70 + "\n")
    
    all_valid = True
    
    # Check directories
    print("📁 Checking Directory Structure...")
    directories = [
        ("app", "Main application directory"),
        ("app/api", "API routes"),
        ("app/api/v1", "API v1 routes"),
        ("app/core", "Core configuration"),
        ("app/models", "Data models"),
        ("app/schemas", "Pydantic schemas"),
        ("app/services", "Business logic services"),
        ("app/repositories", "Data repositories"),
        ("app/dependencies", "FastAPI dependencies"),
        ("app/middleware", "Middleware"),
        ("app/utils", "Utility functions"),
        ("app/db", "Database configuration"),
        ("app/tests", "Test files"),
    ]
    
    for dir_path, desc in directories:
        if not check_directory_exists(dir_path, desc):
            all_valid = False
    
    # Check core files
    print("\n📄 Checking Core Files...")
    files = [
        ("requirements.txt", "Python dependencies"),
        ("Dockerfile", "Docker configuration"),
        ("docker-compose.yml", "Docker Compose setup"),
        (".env", "Environment configuration"),
        (".env.example", "Environment template"),
        ("app/main.py", "FastAPI main app"),
        ("README.md", "Documentation"),
        ("QUICKSTART.md", "Quick start guide"),
        ("IMPLEMENTATION_SUMMARY.md", "Implementation details"),
    ]
    
    for file_path, desc in files:
        if not check_file_exists(file_path, desc):
            all_valid = False
    
    # Check services
    print("\n🔧 Checking Services...")
    services = [
        ("app/services/auth_service.py", "Auth service"),
        ("app/services/jwt_service.py", "JWT service"),
        ("app/services/otp_service.py", "OTP service"),
        ("app/services/user_service.py", "User service"),
        ("app/services/role_service.py", "Role service"),
        ("app/services/email_service.py", "Email service"),
    ]
    
    for file_path, desc in services:
        if not check_file_exists(file_path, desc):
            all_valid = False
    
    # Check repositories
    print("\n📦 Checking Repositories...")
    repos = [
        ("app/repositories/user_repository.py", "User repository"),
        ("app/repositories/role_repository.py", "Role repository"),
        ("app/repositories/otp_repository.py", "OTP repository"),
    ]
    
    for file_path, desc in repos:
        if not check_file_exists(file_path, desc):
            all_valid = False
    
    # Check API routes
    print("\n🛣️  Checking API Routes...")
    routes = [
        ("app/api/v1/auth_routes.py", "Auth routes"),
        ("app/api/v1/admin_routes.py", "Admin routes"),
    ]
    
    for file_path, desc in routes:
        if not check_file_exists(file_path, desc):
            all_valid = False
    
    # Check dependencies
    print("\n🔐 Checking Dependencies...")
    deps = [
        ("app/dependencies/auth_dependency.py", "Auth dependency"),
        ("app/dependencies/role_dependency.py", "Role dependency"),
        ("app/dependencies/district_dependency.py", "District dependency"),
    ]
    
    for file_path, desc in deps:
        if not check_file_exists(file_path, desc):
            all_valid = False
    
    # Check models
    print("\n🗂️  Checking Models...")
    models = [
        ("app/models/user_model.py", "User model"),
        ("app/models/role_model.py", "Role model"),
        ("app/models/otp_model.py", "OTP model"),
        ("app/models/token_model.py", "Token model"),
        ("app/models/complaint_model.py", "Complaint model"),
    ]
    
    for file_path, desc in models:
        if not check_file_exists(file_path, desc):
            all_valid = False
    
    # Check schemas
    print("\n📋 Checking Schemas...")
    schemas = [
        ("app/schemas/auth_schema.py", "Auth schema"),
        ("app/schemas/user_schema.py", "User schema"),
        ("app/schemas/common_schema.py", "Common schema"),
        ("app/schemas/otp_schema.py", "OTP schema"),
        ("app/schemas/token_schema.py", "Token schema"),
    ]
    
    for file_path, desc in schemas:
        if not check_file_exists(file_path, desc):
            all_valid = False
    
    # Check utilities
    print("\n⚙️  Checking Utilities...")
    utils = [
        ("app/utils/validators.py", "Validators"),
        ("app/utils/hash.py", "Hash utilities"),
        ("app/utils/otp_generator.py", "OTP generator"),
        ("app/utils/helpers.py", "Helper functions"),
        ("app/core/security.py", "Security utilities"),
        ("app/core/config.py", "Configuration"),
        ("app/core/exceptions.py", "Exception classes"),
        ("app/core/constants.py", "Constants"),
        ("app/core/logger.py", "Logger setup"),
        ("app/core/response.py", "Response handler"),
    ]
    
    for file_path, desc in utils:
        if not check_file_exists(file_path, desc):
            all_valid = False
    
    # Check database
    print("\n🗄️  Checking Database Setup...")
    db_files = [
        ("app/db/mongodb.py", "MongoDB connection"),
        ("app/db/indexes.py", "MongoDB indexes"),
    ]
    
    for file_path, desc in db_files:
        if not check_file_exists(file_path, desc):
            all_valid = False
    
    # Import validation
    print("\n🔍 Validating Python Imports...")
    try:
        from app.main import app
        print("  ✅ FastAPI app imports")
    except Exception as e:
        print(f"  ❌ FastAPI app import failed: {e}")
        all_valid = False
    
    try:
        from app.services.auth_service import AuthService
        print("  ✅ Auth service imports")
    except Exception as e:
        print(f"  ❌ Auth service import failed: {e}")
        all_valid = False
    
    try:
        from app.dependencies.auth_dependency import get_current_user
        print("  ✅ Auth dependencies import")
    except Exception as e:
        print(f"  ❌ Auth dependencies import failed: {e}")
        all_valid = False
    
    # Summary
    print("\n" + "=" * 70)
    if all_valid:
        print("✅ ALL VALIDATION CHECKS PASSED!")
        print("=" * 70)
        print("\n🎉 Civifix Auth Module is ready for deployment!")
        print("\nNext steps:")
        print("  1. Update .env with your MongoDB URL and JWT secrets")
        print("  2. Run: docker-compose up -d")
        print("  3. Visit: http://localhost:8000/api/docs")
        print("  4. Read: README.md for full documentation")
        print("\n" + "=" * 70 + "\n")
        return 0
    else:
        print("❌ SOME VALIDATION CHECKS FAILED")
        print("=" * 70)
        print("\nPlease review the errors above and fix any missing files.")
        print("\n" + "=" * 70 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
