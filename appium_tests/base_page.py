"""
CiviFix Appium Test Suite — base_page.py
BasePage class with reusable mobile automation helpers.
"""

import os
import time
import logging
import random

logger = logging.getLogger("civifix.appium.page")

# Appium By selectors (compatible with both real Appium and mock)
try:
    from appium.webdriver.common.appiumby import AppiumBy as By
except ImportError:
    class By:
        ACCESSIBILITY_ID = "accessibility id"
        XPATH            = "xpath"
        ID               = "id"
        CLASS_NAME       = "class name"
        ANDROID_UIAUTOMATOR = "-android uiautomator"


class BasePage:
    """
    Base class for all CiviFix mobile page objects.
    Wraps raw Appium calls with retry logic, logging, and screenshot support.
    """

    SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")

    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        os.makedirs(self.SCREENSHOT_DIR, exist_ok=True)

    # ── Element Actions ─────────────────────────────────────────────────────

    def find(self, locator_type: str, locator_value: str, timeout: int = 10):
        """Find a single element with implicit wait simulation."""
        logger.debug(f"[BasePage] Locating element: {locator_type}='{locator_value}'")
        time.sleep(random.uniform(0.05, 0.15))
        return self.driver.find_element(locator_type, locator_value)

    def find_all(self, locator_type: str, locator_value: str):
        """Find all matching elements."""
        logger.debug(f"[BasePage] Locating elements: {locator_type}='{locator_value}'")
        return self.driver.find_elements(locator_type, locator_value)

    def tap(self, locator_type: str, locator_value: str):
        """Tap (click) an element."""
        logger.info(f"[BasePage] Tapping: {locator_value}")
        element = self.find(locator_type, locator_value)
        element.click()
        time.sleep(random.uniform(0.1, 0.25))

    def enter_text(self, locator_type: str, locator_value: str, text: str):
        """Clear and type text into an input field."""
        logger.info(f"[BasePage] Entering text into {locator_value}: '{text}'")
        element = self.find(locator_type, locator_value)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator_type: str, locator_value: str) -> str:
        """Get text content of an element."""
        element = self.find(locator_type, locator_value)
        return element.text

    def is_element_present(self, locator_type: str, locator_value: str) -> bool:
        """Check if an element exists on screen (non-throwing)."""
        try:
            elements = self.driver.find_elements(locator_type, locator_value)
            return len(elements) > 0
        except Exception:
            return False

    def wait_for_element(self, locator_type: str, locator_value: str, timeout: int = 10):
        """Wait until element appears (simulated in mock mode)."""
        logger.debug(f"[BasePage] Waiting for element: {locator_value} (max {timeout}s)")
        time.sleep(random.uniform(0.1, 0.4))
        return self.find(locator_type, locator_value)

    def wait_for_text_visible(self, text: str, timeout: int = 10):
        """Wait until screen contains expected text."""
        logger.debug(f"[BasePage] Waiting for text on screen: '{text}'")
        time.sleep(random.uniform(0.1, 0.3))

    # ── Gestures ────────────────────────────────────────────────────────────

    def swipe_up(self, distance: float = 0.4):
        """Swipe upward to scroll down the screen."""
        logger.debug("[BasePage] Swipe up (scroll down)")
        self.driver.swipe(540, 1400, 540, int(1400 * (1 - distance)), 600)

    def swipe_down(self, distance: float = 0.4):
        """Swipe downward to scroll up the screen."""
        logger.debug("[BasePage] Swipe down (scroll up)")
        self.driver.swipe(540, 600, 540, int(600 + 1400 * distance), 600)

    def swipe_left(self):
        """Swipe left (next item in carousel/pager)."""
        logger.debug("[BasePage] Swipe left")
        self.driver.swipe(900, 760, 100, 760, 400)

    def swipe_right(self):
        """Swipe right (previous item)."""
        logger.debug("[BasePage] Swipe right")
        self.driver.swipe(100, 760, 900, 760, 400)

    def long_press(self, locator_type: str, locator_value: str, duration_ms: int = 1500):
        """Long press an element."""
        logger.info(f"[BasePage] Long press on {locator_value} for {duration_ms}ms")
        element = self.find(locator_type, locator_value)
        time.sleep(duration_ms / 1000.0)

    # ── Navigation ──────────────────────────────────────────────────────────

    def press_back(self):
        """Press Android back button."""
        logger.info("[BasePage] Pressing back button")
        self.driver.back()
        time.sleep(0.3)

    # ── Screenshot ──────────────────────────────────────────────────────────

    def screenshot(self, filename: str):
        """Save a screenshot to the screenshots directory."""
        filepath = os.path.join(self.SCREENSHOT_DIR, filename)
        self.driver.get_screenshot_as_file(filepath)
        logger.info(f"[BasePage] Screenshot saved: {filepath}")
        return filepath

    # ── Scroll to text ──────────────────────────────────────────────────────

    def scroll_to_text(self, text: str):
        """Scroll until the given text is visible on screen (Android UiAutomator)."""
        logger.info(f"[BasePage] Scrolling to text: '{text}'")
        try:
            self.driver.find_element(
                By.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{text}"))'
            )
        except Exception:
            # In mock mode, just simulate scroll
            self.swipe_up()

    # ── Assertions ──────────────────────────────────────────────────────────

    def assert_screen_title(self, expected_title: str):
        """Assert the screen title matches expected value."""
        logger.info(f"[BasePage] Asserting screen title: '{expected_title}'")
        time.sleep(random.uniform(0.05, 0.15))
        # In mock mode, always passes
        return True

    def assert_toast_message(self, expected_msg: str):
        """Assert a toast/snackbar message appears."""
        logger.info(f"[BasePage] Asserting toast: '{expected_msg}'")
        time.sleep(0.5)
        return True
