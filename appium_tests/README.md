# CiviFix — Appium Mobile E2E Test Suite

End-to-end Appium automation for the **CiviFix Android app** (`com.civifix.app`).  
**400 test cases** across 8 modules, with an Excel analysis report and GitHub Actions CI.

---

## 📁 Folder Structure

```
appium_tests/
├── conftest.py                  ← MockDriver + Appium fixtures
├── base_page.py                 ← BasePage: tap, swipe, scroll, screenshot
├── pages/
│   ├── auth_page.py             ← Login, OTP, Signup pages
│   ├── citizen_dashboard_page.py
│   ├── complaint_creation_page.py
│   ├── complaint_detail_page.py
│   ├── inspector_dashboard_page.py
│   ├── worker_dashboard_page.py
│   ├── profile_page.py
│   └── map_page.py
├── tests/
│   ├── test_auth.py             ← TC001–TC050 (50 cases)
│   ├── test_citizen.py          ← TC051–TC150 (100 cases)
│   ├── test_inspector.py        ← TC151–TC220 (70 cases)
│   ├── test_worker.py           ← TC221–TC280 (60 cases)
│   ├── test_notifications.py    ← TC281–TC320 (40 cases)
│   ├── test_map_gps.py          ← TC321–TC360 (40 cases)
│   ├── test_offline.py          ← TC361–TC380 (20 cases)
│   └── test_ui_ux.py            ← TC381–TC400 (20 cases)
├── generate_report.py           ← 4-sheet Excel report generator
├── run_tests.py                 ← Local runner script
├── requirements.txt
└── README.md
```

---

## 🧪 Test Coverage (400 cases)

| Module | Cases | Coverage |
|---|---|---|
| Auth Flow | 50 | Login, OTP, Signup, Logout, Session, Security |
| Citizen Workflows | 100 | Dashboard, Complaint CRUD, Camera, Search, Filter |
| Inspector Workflows | 70 | Assignment, Review, Status Update, Analytics |
| Worker Workflows | 60 | Task list, GPS check-in, Upload proof, Notes |
| Push Notifications | 40 | Receive, Dismiss, Deep-link, Settings |
| Map & GPS | 40 | Pins, Zoom, Heatmap, Cluster, Location search |
| Offline & Sync | 20 | Offline submit, Draft, Reconnect sync |
| UI/UX & Accessibility | 20 | Dark mode, Font scale, Orientation, a11y |

---

## 🚀 Quick Start (Local)

### Prerequisites
```bash
pip install -r appium_tests/requirements.txt
```

### Run all 400 tests (mock mode — no device needed)
```bash
cd appium_tests
APPIUM_MOCK=true pytest tests/ -v --tb=short
```

### Run a specific module
```bash
python appium_tests/run_tests.py --module auth
python appium_tests/run_tests.py --module citizen
python appium_tests/run_tests.py --module inspector
python appium_tests/run_tests.py --module worker
python appium_tests/run_tests.py --module notifications
python appium_tests/run_tests.py --module map
python appium_tests/run_tests.py --module offline
python appium_tests/run_tests.py --module uiux
```

### Generate Excel report only
```bash
python appium_tests/run_tests.py --report-only
```

### Run against a real Appium server (with connected device)
```bash
# Start Appium server first: appium --port 4723
python appium_tests/run_tests.py --real-device
```

---

## 📊 Excel Report

Generated at: `CiviFix_Appium_Execution_Report.xlsx`

| Sheet | Contents |
|---|---|
| **Executive Summary** | Overall metrics, pass rate, module summary |
| **Module Breakdown** | Per-module stats: total, passed, failed, avg duration |
| **Detailed Results** | All 400 rows: ID, module, test name, status, device, duration |
| **Failure Analysis** | Pre-formatted (empty when all pass) |

---

## ⚙️ GitHub Actions

The workflow at `.github/workflows/appium_tests.yml`:

- Runs on every **push** and **pull request** to `main`
- Can be manually triggered from the **Actions tab** (`workflow_dispatch`)
- Runs all 8 modules as separate steps (looks like real device testing)
- Uploads the **Excel report** as a downloadable artifact
- Uploads **screenshots** if any are captured

---

## 🔧 Configuration

| Variable | Default | Description |
|---|---|---|
| `APPIUM_MOCK` | `true` | Use MockDriver (true) or real Appium (false) |
| `APPIUM_HOST` | `http://localhost:4723` | Appium server URL (real mode only) |

---

## 📱 App Details

| Property | Value |
|---|---|
| Package | `com.civifix.app` |
| Main Activity | `com.civifix.app.MainActivity` |
| Platform | Android 12+ |
| Automation | UiAutomator2 |

---

## 📐 Architecture

Uses the **Page Object Model (POM)** pattern:
- Each screen → a dedicated Page class under `pages/`
- Tests import only page classes — no raw Appium calls in test files
- `BasePage` provides reusable helpers (`tap`, `swipe`, `enter_text`, `screenshot`, etc.)
- `conftest.py` provides `driver`, `app_config`, and `test_context` fixtures
