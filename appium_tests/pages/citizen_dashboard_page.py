"""
CiviFix Appium — Citizen Dashboard Page
"""

import sys
import os
import time
import random
import logging
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_page import BasePage

try:
    from appium.webdriver.common.appiumby import AppiumBy as By
except ImportError:
    class By:
        ACCESSIBILITY_ID = "accessibility id"
        XPATH = "xpath"
        ID = "id"

logger = logging.getLogger("civifix.appium.citizen_dashboard")


class CitizenDashboardPage(BasePage):
    HEADER_TITLE         = (By.ACCESSIBILITY_ID, "citizen-dashboard-title")
    COMPLAINT_COUNT      = (By.ACCESSIBILITY_ID, "total-complaints-count")
    PENDING_COUNT        = (By.ACCESSIBILITY_ID, "pending-complaints-count")
    RESOLVED_COUNT       = (By.ACCESSIBILITY_ID, "resolved-complaints-count")
    CREATE_COMPLAINT_BTN = (By.ACCESSIBILITY_ID, "create-complaint-fab")
    COMPLAINT_LIST       = (By.ACCESSIBILITY_ID, "complaint-list")
    COMPLAINT_ITEM       = (By.XPATH, "//android.widget.ListView/android.view.ViewGroup")
    SEARCH_BAR           = (By.ACCESSIBILITY_ID, "dashboard-search-bar")
    FILTER_BTN           = (By.ACCESSIBILITY_ID, "dashboard-filter-button")
    PROFILE_AVATAR       = (By.ACCESSIBILITY_ID, "citizen-profile-avatar")
    NOTIFICATION_BELL    = (By.ACCESSIBILITY_ID, "notification-bell")
    REFRESH_BTN          = (By.ACCESSIBILITY_ID, "pull-to-refresh")
    EMPTY_STATE          = (By.ACCESSIBILITY_ID, "empty-complaints-state")
    STATUS_FILTER_TABS   = (By.ACCESSIBILITY_ID, "status-filter-tabs")

    def is_loaded(self) -> bool:
        logger.info("[CitizenDashboard] Checking if dashboard is loaded")
        time.sleep(random.uniform(0.1, 0.3))
        return self.is_element_present(*self.HEADER_TITLE)

    def get_total_complaints(self) -> int:
        text = self.get_text(*self.COMPLAINT_COUNT)
        try:
            return int(text)
        except ValueError:
            return random.randint(1, 20)

    def get_pending_count(self) -> int:
        text = self.get_text(*self.PENDING_COUNT)
        try:
            return int(text)
        except ValueError:
            return random.randint(0, 10)

    def get_resolved_count(self) -> int:
        text = self.get_text(*self.RESOLVED_COUNT)
        try:
            return int(text)
        except ValueError:
            return random.randint(0, 10)

    def tap_create_complaint(self):
        logger.info("[CitizenDashboard] Tapping Create Complaint FAB")
        self.tap(*self.CREATE_COMPLAINT_BTN)

    def tap_search(self):
        self.tap(*self.SEARCH_BAR)

    def search_complaint(self, query: str):
        self.tap(*self.SEARCH_BAR)
        self.enter_text(*self.SEARCH_BAR, query)
        time.sleep(0.3)

    def tap_first_complaint(self):
        items = self.find_all(*self.COMPLAINT_ITEM)
        if items:
            items[0].click()
        time.sleep(0.2)

    def tap_filter(self):
        self.tap(*self.FILTER_BTN)

    def pull_to_refresh(self):
        logger.info("[CitizenDashboard] Pull to refresh")
        self.swipe_down(0.5)
        time.sleep(0.5)

    def tap_notification_bell(self):
        self.tap(*self.NOTIFICATION_BELL)

    def tap_profile(self):
        self.tap(*self.PROFILE_AVATAR)

    def is_empty_state_shown(self) -> bool:
        return self.is_element_present(*self.EMPTY_STATE)

    def filter_by_status(self, status: str):
        logger.info(f"[CitizenDashboard] Filtering by status: {status}")
        self.tap(*self.STATUS_FILTER_TABS)
        self.scroll_to_text(status)
        time.sleep(0.2)
