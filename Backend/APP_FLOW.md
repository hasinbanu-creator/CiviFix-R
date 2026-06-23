# Civifix Backend Application Flow

This document describes the main runtime flow of the Civifix FastAPI application from user registration through complaint completion, with role-specific responsibilities and key endpoints.

## 1. Roles and Access Control

The app defines these primary roles in `app/core/enums.py`:

- `SUPER_ADMIN`
- `ADMIN`
- `DISTRICT_ADMIN`
- `INSPECTOR`
- `WORKER`
- `CITIZEN`

Authorization is enforced through:

- `app.dependencies.auth_dependency.get_current_user` — validates JWT bearer tokens and returns the current user context.
- `app.dependencies.role_dependency.require_role(...)` — protects endpoints so only allowed roles can access them.

## 2. Registration and Authentication Flow

### 2.1 Registration

Endpoint: `POST /api/v1/auth/register`

- Request body: `RegisterSchema`
- Creates a new user as a `CITIZEN` in an inactive state.
- Generates an OTP and stores an OTP hash and expiry in the user record.
- Sends the OTP to the user's email through `EmailService.send_otp_email`.

Service path:

- `AuthService.register_user(...)`
  - validates email and mobile number
  - checks for existing user
  - hashes OTP and stores it
  - inserts a user document
  - returns `user_id` and the generated OTP for email delivery

### 2.2 Verify Registration OTP

Endpoint: `POST /api/v1/auth/verify-otp`

- Request body: `VerifyOTPSchema`
- Validates the OTP against the stored hash and expiry.
- Marks the user as verified and active.
- Generates JWT `access_token` and `refresh_token`.

Service path:

- `AuthService.verify_registration_otp(...)`
  - loads user by email
  - checks expiry and attempt count
  - verifies OTP using `SecurityUtils.verify_otp`
  - calls `UserRepository.verify_user(user_id)`
  - creates tokens via `AuthService._create_tokens(...)`

### 2.3 Login

Endpoint: `POST /api/v1/auth/login`

- Request body: `LoginSchema`
- Sends a login OTP to the registered email.
- Rate-limits OTP requests and checks account active status.

Service path:

- `AuthService.login_user(...)`
  - loads user by email
  - verifies user is active
  - checks resend rate limits
  - updates OTP hash, expiry, and resend metadata

### 2.4 Verify Login OTP

Endpoint: `POST /api/v1/auth/verify-login-otp`

- Request body: `VerifyOTPSchema`
- Validates OTP and returns the JWT session tokens.
- Updates `last_login`.

Service path:

- `AuthService.verify_login_otp(...)`
  - verifies OTP and expiry
  - updates last login timestamp
  - returns new tokens and role/district metadata

## 3. District Management Flow

District management is a SUPER_ADMIN responsibility that defines the districts available for wards, users, and complaints.

### Key District Endpoints

- `POST /api/v1/admin/districts` — create a new district
- `GET /api/v1/admin/districts` — list all districts
- `GET /api/v1/admin/districts/{district_id}` — get district details
- `PATCH /api/v1/admin/districts/{district_id}` — update district details
- `PATCH /api/v1/admin/districts/{district_id}/activate` — activate a district
- `PATCH /api/v1/admin/districts/{district_id}/deactivate` — deactivate a district
- `DELETE /api/v1/admin/districts/{district_id}` — delete a district

### Role

- `SUPER_ADMIN` is the authorized role for district creation, update, activation, deactivation, and deletion.

### District document fields

Districts are stored with fields such as:

- `name`
- `code`
- `state`
- `email`
- `phone`
- `address`
- `is_active`
- `created_by`
- `created_at`
- `updated_at`

### Service logic

`DistrictService` validates:

- uniqueness of district `code`
- uniqueness of district `name`
- district creation and update payloads
- district status changes via activate/deactivate

When a district is created, it is saved through `DistrictRepository` and returned as a JSON-safe document.

### Implementation path

- `app/api/v1/districts_routes.py` — district route definitions
- `app/services/district_service.py` — district business logic
- `app/repositories/district_repository.py` — MongoDB district CRUD
- `app/models/district_model.py` — district document shape
- `app/schemas/district_schema.py` — validation schemas
- `app/main.py` — registers the district router

## 4. Ward Management Flow

Ward management is used by district-level administration to organize inspectors and local areas.

### Key Ward Endpoints

- `POST /api/v1/wards` — create ward
- `PUT /api/v1/wards/{ward_id}` — update ward
- `GET /api/v1/wards/{ward_id}` — get ward details
- `GET /api/v1/wards/district/{district_id}` — list wards in district
- `GET /api/v1/wards/inspector/{inspector_id}` — list inspector wards
- `GET /api/v1/wards/search/{district_id}` — search wards
- `PUT /api/v1/wards/{ward_id}/deactivate` — deactivate ward

### Role

- `DISTRICT_ADMIN` is the expected owner for create/update/deactivate ward operations.

### Service logic

`WardService` validates:

- district existence
- inspector existence and role
- inspector district membership
- duplicate ward numbers within a district
- ward activation state

When a ward is created or updated, it is saved through `WardRepository` and formatted for API responses.

## 5. Complaint Lifecycle

The complaint workflow is the core of the app. It is split into roles and status transitions.

### Complaint statuses

Defined in `ComplaintStatus`:

- `OPEN`
- `WORKING`
- `APPROVAL`
- `CLOSED`
- `REJECTED`

### 5.1 Complaint creation

Endpoint: `POST /api/v1/complaints`

- `CITIZEN` only.
- Uses `ComplaintCreateSchema`.
- Validates GPS coordinates and ward activity.
- Checks duplicate complaints in the same area.
- Enforces per-day and per-week complaint limits.
- Automatically assigns the complaint to the ward inspector.
- Creates a complaint document with status `OPEN`.
- Adds an audit history entry: `CREATED`.
- Updates ward complaint counts and optionally notifies the inspector.

Service path:

- `ComplaintService.create_complaint(...)`
  - verifies role is `CITIZEN`
  - validates ward and spam/duplicate rules
  - writes complaint to database
  - updates ward stats
  - notifies inspector

### 5.2 Inspector assignment

Endpoint: `PUT /api/v1/complaints/{complaint_id}/assign-worker`

- `INSPECTOR` only.
- Only the assigned inspector may perform this action.
- Assigns a `WORKER` to the complaint.
- Updates complaint status to `WORKING`.
- Adds a history entry: `ASSIGNED`.
- Sends a notification to the assigned worker.

### 5.3 Worker submits completion

Endpoint: `PUT /api/v1/complaints/{complaint_id}/submit-work`

- `WORKER` only.
- The assigned worker must match the complaint's `worker_id`.
- Allowed only when complaint status is `WORKING`.
- Adds worker notes and proof images.
- Changes status to `APPROVAL`.
- Adds a history entry: `STATUS_CHANGED`.
- Notifies the inspector.

### 5.4 Inspector approves completion

Endpoint: `PUT /api/v1/complaints/{complaint_id}/approve`

- `INSPECTOR` only.
- The same inspector who owns the complaint must approve.
- Allowed only when status is `APPROVAL`.
- Changes status to `CLOSED`.
- Adds `inspector_note`, `closed_at`, and history entry `APPROVED`.
- Updates ward complaint counts for closed complaints.
- Optionally notifies citizen and worker.

### 5.5 Inspector rejects completion

Endpoint: `PUT /api/v1/complaints/{complaint_id}/reject`

- `INSPECTOR` only.
- Allowed only when status is `APPROVAL`.
- Returns complaint to `WORKING` status.
- Stores the rejection reason.
- Adds a history entry `REJECTED`.
- Notifies the worker to continue work.

### 5.6 Complaint viewing and dashboards

Citizen and other authenticated users can view:

- `GET /api/v1/complaints/{complaint_id}` — complaint details + history.
- `GET /api/v1/complaints/my/dashboard` — current user complaints.
- `GET /api/v1/complaints/ward/{ward_id}` — complaints by ward.
- `GET /api/v1/complaints/inspector/dashboard` — inspector dashboard stats.

## 6. Notification and audit support

`ComplaintService` records history for actions including:

- `CREATED`
- `ASSIGNED`
- `STATUS_CHANGED`
- `APPROVED`
- `REJECTED`

Notifications are triggered during:

- complaint creation (to inspector)
- worker assignment
- work submission
- complaint approval
- complaint rejection

## 7. Final flow summary

1. Citizen registers via `POST /api/v1/auth/register`.
2. Citizen verifies OTP via `POST /api/v1/auth/verify-otp` and obtains JWT tokens.
3. Citizen logs in via OTP and receives access tokens.
4. District admin creates wards and assigns inspectors.
5. Citizen files a complaint against a ward.
6. Inspector assigns a worker and moves the complaint to `WORKING`.
7. Worker submits completion and the complaint moves to `APPROVAL`.
8. Inspector reviews the submission and either:
   - approves it, closing the complaint, or
   - rejects it, returning work to the worker.

## 8. Key modules

- `app/api/v1/auth_routes.py` — registration, OTP verification, login, token refresh.
- `app/api/v1/wards_routes.py` — ward lifecycle management.
- `app/api/v1/complaints_routes.py` — complaint creation, assignment, submission, approval, rejection.
- `app/services/auth_service.py` — auth business rules and token generation.
- `app/services/ward_service.py` — ward validation and lifecycle.
- `app/services/complaint_service.py` — complaint state machine and role authorization.
- `app/dependencies/auth_dependency.py` — global JWT auth dependency.
- `app/dependencies/role_dependency.py` — role-level access enforcement.
