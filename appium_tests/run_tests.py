"""
CiviFix Appium — Local Test Runner
Usage:
    python run_tests.py                   # run all 400 tests (mock mode)
    python run_tests.py --real-device     # run against real Appium server
    python run_tests.py --module auth     # run only auth tests
    python run_tests.py --report-only     # only generate Excel report
"""

import subprocess
import sys
import os
import argparse
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

MODULE_MAP = {
    "auth":          "tests/test_auth.py",
    "citizen":       "tests/test_citizen.py",
    "inspector":     "tests/test_inspector.py",
    "worker":        "tests/test_worker.py",
    "notifications": "tests/test_notifications.py",
    "map":           "tests/test_map_gps.py",
    "offline":       "tests/test_offline.py",
    "uiux":          "tests/test_ui_ux.py",
}

REPORT_SCRIPT = os.path.join(BASE_DIR, "generate_report.py")
REPORT_OUTPUT = os.path.join(PROJECT_ROOT, "CiviFix_Appium_Execution_Report.xlsx")


def run_tests(module: str = None, real_device: bool = False, verbose: bool = True):
    env = os.environ.copy()
    env["APPIUM_MOCK"] = "false" if real_device else "true"

    if module:
        target = os.path.join(BASE_DIR, MODULE_MAP[module])
        print(f"\n🚀 Running module: {module.upper()} → {target}")
    else:
        target = os.path.join(BASE_DIR, "tests/")
        print(f"\n🚀 Running ALL 400 Appium E2E tests (mock={not real_device})")

    args = [
        sys.executable, "-m", "pytest",
        target,
        "-v" if verbose else "-q",
        "--tb=short",
        "-s",
        f"--rootdir={BASE_DIR}",
    ]

    print(f"   Command: {' '.join(args)}\n{'─' * 70}")
    start = time.time()
    result = subprocess.run(args, env=env, cwd=BASE_DIR)
    elapsed = time.time() - start

    print(f"\n{'─' * 70}")
    print(f"✅ Tests complete in {elapsed:.1f}s | Exit code: {result.returncode}")
    return result.returncode


def run_report():
    print(f"\n📊 Generating Excel report → {REPORT_OUTPUT}")
    result = subprocess.run(
        [sys.executable, REPORT_SCRIPT, REPORT_OUTPUT],
        cwd=PROJECT_ROOT,
    )
    if result.returncode == 0:
        print(f"✅ Report generated: {REPORT_OUTPUT}")
    else:
        print(f"❌ Report generation failed (exit {result.returncode})")
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="CiviFix Appium Test Runner")
    parser.add_argument("--real-device",  action="store_true",  help="Use real Appium server instead of mock")
    parser.add_argument("--module",       choices=list(MODULE_MAP.keys()), help="Run specific module only")
    parser.add_argument("--report-only",  action="store_true",  help="Only generate report, skip tests")
    parser.add_argument("--quiet",        action="store_true",  help="Less verbose output")
    args = parser.parse_args()

    if args.report_only:
        sys.exit(run_report())

    exit_code = run_tests(
        module=args.module,
        real_device=args.real_device,
        verbose=not args.quiet,
    )

    report_code = run_report()
    sys.exit(exit_code or report_code)


if __name__ == "__main__":
    main()
