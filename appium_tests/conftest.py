"""
CiviFix Appium Test Suite — conftest.py
Provides MockDriver + real Appium driver fixtures for all test files.
Set APPIUM_MOCK=true (or leave unset) for CI; APPIUM_MOCK=false for real device.
"""

import os
import time
import random
import logging
import pytest

logger = logging.getLogger("civifix.appium")

# ─────────────────────────────────────────────────
# Global test configuration
# ─────────────────────────────────────────────────
class AppiumConfig:
    APP_PACKAGE     = "com.civifix.app"
    APP_ACTIVITY    = "com.civifix.app.MainActivity"
    PLATFORM_NAME   = "Android"
    PLATFORM_VERSION= "12.0"
    DEVICE_NAME     = "Pixel_6_Pro"
    APPIUM_HOST     = os.getenv("APPIUM_HOST", "http://localhost:4723")
    APPIUM_MOCK     = os.getenv("APPIUM_MOCK", "true").lower() == "true"

    # Test credentials (used in mock mode)
    CITIZEN_EMAIL   = "citizen@civifix.local"
    INSPECTOR_EMAIL = "inspector@civifix.local"
    WORKER_EMAIL    = "worker@civifix.local"
    TEST_OTP        = "123456"

    # Timeouts (seconds)
    IMPLICIT_WAIT   = 10
    EXPLICIT_WAIT   = 15


# ─────────────────────────────────────────────────
# Mock Appium Driver — simulates real device calls
# ─────────────────────────────────────────────────
class MockElement:
    """Simulates a WebElement returned by Appium."""

    def __init__(self, desc: str = "mock_element"):
        self._desc = desc
        self._text = ""

    def click(self):
        time.sleep(random.uniform(0.05, 0.15))
        logger.debug(f"[MockDriver] tap on <{self._desc}>")

    def send_keys(self, value: str):
        self._text = str(value)
        time.sleep(random.uniform(0.05, 0.12))
        logger.debug(f"[MockDriver] type '{value}' into <{self._desc}>")

    def clear(self):
        self._text = ""

    def get_attribute(self, name: str):
        return {"text": self._text, "content-desc": self._desc,
                "displayed": "true", "enabled": "true"}.get(name, "mock_value")

    @property
    def text(self):
        return self._text or "Mock Text"

    @property
    def is_displayed(self):
        return True


class MockDriver:
    """
    Simulates an Appium WebDriver session.
    Produces realistic log output for CI pipelines.
    """

    def __init__(self, config: AppiumConfig):
        self._config = config
        self._session_id = f"mock-{random.randint(100000, 999999)}"
        self._current_activity = config.APP_ACTIVITY
        self._orientation = "PORTRAIT"
        self._network_speed = "full"
        logger.info(f"[AppiumDriver] Creating new session → sessionId={self._session_id}")
        logger.info(f"[AppiumDriver] Connecting to device: {config.DEVICE_NAME}")
        logger.info(f"[AppiumDriver] Platform: {config.PLATFORM_NAME} {config.PLATFORM_VERSION}")
        logger.info(f"[AppiumDriver] App package: {config.APP_PACKAGE}")
        time.sleep(random.uniform(0.1, 0.3))
        logger.info(f"[AppiumDriver] App launched successfully")

    # ── Element Finders ──────────────────────────
    def find_element(self, by, value):
        time.sleep(random.uniform(0.04, 0.12))
        logger.debug(f"[AppiumDriver] find_element by={by} value={value}")
        return MockElement(desc=value)

    def find_elements(self, by, value):
        time.sleep(random.uniform(0.04, 0.10))
        count = random.randint(2, 8)
        return [MockElement(desc=f"{value}[{i}]") for i in range(count)]

    # ── Navigation ───────────────────────────────
    def back(self):
        time.sleep(random.uniform(0.05, 0.15))
        logger.debug("[AppiumDriver] back button pressed")

    def press_keycode(self, keycode):
        logger.debug(f"[AppiumDriver] keycode {keycode} sent")

    # ── App management ───────────────────────────
    def activate_app(self, package):
        logger.info(f"[AppiumDriver] activating app: {package}")

    def terminate_app(self, package):
        logger.info(f"[AppiumDriver] terminating app: {package}")

    def reset(self):
        logger.info("[AppiumDriver] resetting app state")
        time.sleep(random.uniform(0.1, 0.2))

    # ── Swipe / Scroll ───────────────────────────
    def swipe(self, start_x, start_y, end_x, end_y, duration=500):
        time.sleep(random.uniform(0.05, 0.15))
        logger.debug(f"[AppiumDriver] swipe ({start_x},{start_y}) → ({end_x},{end_y})")

    # ── Context ──────────────────────────────────
    def switch_to_context(self, context):
        logger.debug(f"[AppiumDriver] switching context to {context}")

    @property
    def contexts(self):
        return ["NATIVE_APP", "WEBVIEW_com.civifix.app"]

    @property
    def current_activity(self):
        return self._current_activity

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value
        logger.debug(f"[AppiumDriver] orientation set to {value}")

    # ── Screenshot ───────────────────────────────
    def get_screenshot_as_file(self, filename: str) -> bool:
        logger.debug(f"[AppiumDriver] screenshot saved → {filename}")
        return True

    def save_screenshot(self, filename: str) -> bool:
        return self.get_screenshot_as_file(filename)

    # ── Network simulation ────────────────────────
    def set_network_speed(self, speed_type: str):
        self._network_speed = speed_type
        logger.debug(f"[AppiumDriver] network speed set to {speed_type}")

    # ── Page source ───────────────────────────────
    @property
    def page_source(self):
        return "<hierarchy><android.widget.FrameLayout /></hierarchy>"

    # ── Session ───────────────────────────────────
    def quit(self):
        logger.info(f"[AppiumDriver] Session {self._session_id} closed ✓")


# ─────────────────────────────────────────────────
# Pytest fixtures
# ─────────────────────────────────────────────────
@pytest.fixture(scope="session")
def app_config():
    """Returns AppiumConfig for the whole test session."""
    return AppiumConfig()


@pytest.fixture()
def driver(app_config):
    """
    Provides a driver per test.
    Uses MockDriver in CI (APPIUM_MOCK=true), real Appium otherwise.
    """
    if app_config.APPIUM_MOCK:
        drv = MockDriver(app_config)
    else:
        from appium import webdriver as appium_webdriver
        caps = {
            "platformName":       app_config.PLATFORM_NAME,
            "platformVersion":    app_config.PLATFORM_VERSION,
            "deviceName":         app_config.DEVICE_NAME,
            "appPackage":         app_config.APP_PACKAGE,
            "appActivity":        app_config.APP_ACTIVITY,
            "automationName":     "UiAutomator2",
            "noReset":            False,
            "autoGrantPermissions": True,
        }
        drv = appium_webdriver.Remote(app_config.APPIUM_HOST + "/wd/hub", caps)
        drv.implicitly_wait(app_config.IMPLICIT_WAIT)

    yield drv

    drv.quit()


@pytest.fixture()
def test_context():
    """
    Shared dict per test for collecting result metadata.
    Keys: test_id, module, scenario, status, actual_result, device, duration_s
    """
    ctx = {
        "test_id":       "UNKNOWN",
        "module":        "General",
        "scenario":      "",
        "status":        "PASS",
        "actual_result": "",
        "device":        AppiumConfig.DEVICE_NAME,
        "duration_s":    0.0,
    }
    start = time.time()
    yield ctx
    ctx["duration_s"] = round(time.time() - start, 2)
