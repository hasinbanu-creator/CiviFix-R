import os

base_dir = "mobile_vulnerability_testing"
dirs = [
    f"{base_dir}/config",
    f"{base_dir}/drivers",
    f"{base_dir}/reports/html",
    f"{base_dir}/reports/excel",
    f"{base_dir}/reports/json",
    f"{base_dir}/reports/screenshots",
    f"{base_dir}/reports/logs",
    f"{base_dir}/scripts",
    f"{base_dir}/tests/authentication",
    f"{base_dir}/tests/authorization",
    f"{base_dir}/tests/storage",
    f"{base_dir}/tests/network",
    f"{base_dir}/tests/session",
    f"{base_dir}/tests/input_validation",
    f"{base_dir}/tests/encryption",
    f"{base_dir}/tests/permissions",
    f"{base_dir}/tests/root_detection",
    f"{base_dir}/tests/ssl",
    f"{base_dir}/tests/deep_links",
    f"{base_dir}/tests/webview",
    f"{base_dir}/tests/api_security",
    f"{base_dir}/tests/business_logic",
    f"{base_dir}/utils",
    f"{base_dir}/data",
    f"{base_dir}/evidence",
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    if d.startswith(f"{base_dir}/tests") or d.startswith(f"{base_dir}/utils") or d.startswith(f"{base_dir}/scripts") or d.startswith(f"{base_dir}/config"):
        init_file = os.path.join(d, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                pass

# Also root init
with open(f"{base_dir}/__init__.py", "w") as f:
    pass

print(f"Directory structure created in {base_dir}")
