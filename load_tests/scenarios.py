import typing

class Scenario:
    def __init__(self, tc_id: str, module: str, name: str, method: str, endpoint: str):
        self.tc_id = tc_id
        self.module = module
        self.name = name
        self.method = method
        self.endpoint = endpoint

def generate_scenarios() -> typing.List[Scenario]:
    scenarios = []
    
    # 1. Auth Flow (TC001 - TC050: 50 cases)
    for i in range(1, 51):
        tc_id = f"TC{i:03d}"
        if i <= 10:
            scenarios.append(Scenario(tc_id, "Auth Flow", f"Login Validation {i}", "POST", f"/api/v1/auth/login?variation={i}"))
        elif i <= 25:
            scenarios.append(Scenario(tc_id, "Auth Flow", f"Signup flow step {i}", "POST", f"/api/v1/auth/signup?step={i}"))
        elif i <= 35:
            scenarios.append(Scenario(tc_id, "Auth Flow", f"OTP Verification {i}", "POST", f"/api/v1/auth/otp/verify?attempt={i}"))
        else:
            scenarios.append(Scenario(tc_id, "Auth Flow", f"Profile Session {i}", "GET", f"/api/v1/auth/session/status?chk={i}"))
            
    # 2. Citizen Workflows (TC051 - TC150: 100 cases)
    for i in range(51, 151):
        tc_id = f"TC{i:03d}"
        if i <= 80:
            scenarios.append(Scenario(tc_id, "Citizen Workflows", f"Fetch dashboard data {i}", "GET", f"/api/v1/citizen/dashboard?region={i}"))
        elif i <= 120:
            scenarios.append(Scenario(tc_id, "Citizen Workflows", f"Submit complaint type {i}", "POST", f"/api/v1/citizen/complaints?type={i}"))
        else:
            scenarios.append(Scenario(tc_id, "Citizen Workflows", f"View complaint detail {i}", "GET", f"/api/v1/citizen/complaints/detail?id={i}"))

    # 3. Inspector (TC151 - TC220: 70 cases)
    for i in range(151, 221):
        tc_id = f"TC{i:03d}"
        if i <= 180:
            scenarios.append(Scenario(tc_id, "Inspector", f"Inspector dashboard metrics {i}", "GET", f"/api/v1/inspector/metrics?view={i}"))
        elif i <= 200:
            scenarios.append(Scenario(tc_id, "Inspector", f"Assign worker to complaint {i}", "PUT", f"/api/v1/inspector/assignments?id={i}"))
        else:
            scenarios.append(Scenario(tc_id, "Inspector", f"Approve resolution {i}", "POST", f"/api/v1/inspector/resolutions/approve?id={i}"))

    # 4. Worker (TC221 - TC280: 60 cases)
    for i in range(221, 281):
        tc_id = f"TC{i:03d}"
        if i <= 240:
            scenarios.append(Scenario(tc_id, "Worker", f"Worker task list {i}", "GET", f"/api/v1/worker/tasks?filter={i}"))
        elif i <= 260:
            scenarios.append(Scenario(tc_id, "Worker", f"Upload resolution evidence {i}", "POST", f"/api/v1/worker/tasks/evidence?id={i}"))
        else:
            scenarios.append(Scenario(tc_id, "Worker", f"Update task status {i}", "PUT", f"/api/v1/worker/tasks/status?id={i}"))

    # 5. Push Notifications (TC281 - TC320: 40 cases)
    for i in range(281, 321):
        tc_id = f"TC{i:03d}"
        scenarios.append(Scenario(tc_id, "Push Notifications", f"Register device token {i}", "POST", f"/api/v1/notifications/register?token={i}"))

    # 6. Map & GPS (TC321 - TC360: 40 cases)
    for i in range(321, 361):
        tc_id = f"TC{i:03d}"
        scenarios.append(Scenario(tc_id, "Map & GPS", f"Fetch nearby complaints {i}", "GET", f"/api/v1/map/nearby?lat=13.08&lng=80.27&radius={i}"))

    # 7. Offline Sync (TC361 - TC380: 20 cases)
    for i in range(361, 381):
        tc_id = f"TC{i:03d}"
        scenarios.append(Scenario(tc_id, "Offline Sync", f"Sync queued actions {i}", "POST", f"/api/v1/sync/push?batch={i}"))

    # 8. UI/UX & Misc (TC381 - TC400: 20 cases)
    for i in range(381, 401):
        tc_id = f"TC{i:03d}"
        scenarios.append(Scenario(tc_id, "Misc API", f"Fetch config {i}", "GET", f"/api/v1/config/app?version={i}"))

    assert len(scenarios) == 400, f"Expected 400 scenarios, got {len(scenarios)}"
    return scenarios

SCENARIOS = generate_scenarios()
