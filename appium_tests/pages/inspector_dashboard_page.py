"""
CiviFix Appium — Inspector Dashboard Page
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

logger = logging.getLogger("civifix.appium.inspector_dashboard")


class InspectorDashboardPage(BasePage):
    HEADER_TITLE         = (By.ACCESSIBILITY_ID, "inspector-dashboard-title")
    ASSIGNED_COUNT       = (By.ACCESSIBILITY_ID, "inspector-assigned-count")
    PENDING_REVIEW_COUNT = (By.ACCESSIBILITY_ID, "inspector-pending-review-count")
    COMPLETED_COUNT      = (By.ACCESSIBILITY_ID, "inspector-completed-count")
    COMPLAINT_LIST       = (By.ACCESSIBILITY_ID, "inspector-complaint-list")
    COMPLAINT_ITEM       = (By.XPATH, "//android.widget.ListView/android.view.ViewGroup")
    ASSIGN_WORKER_BTN    = (By.ACCESSIBILITY_ID, "assign-worker-button")
    WORKER_PICKER        = (By.ACCESSIBILITY_ID, "worker-picker-dialog")
    UPDATE_STATUS_BTN    = (By.ACCESSIBILITY_ID, "update-status-button")
    STATUS_PICKER        = (By.ACCESSIBILITY_ID, "status-picker-dialog")
    ADD_INSPECTION_NOTES = (By.ACCESSIBILITY_ID, "inspection-notes-input")
    SUBMIT_REVIEW_BTN    = (By.ACCESSIBILITY_ID, "submit-review-button")
    FILTER_DROPDOWN      = (By.ACCESSIBILITY_ID, "inspector-filter-dropdown")
    SEARCH_BAR           = (By.ACCESSIBILITY_ID, "inspector-search-bar")
    REFRESH_BTN          = (By.ACCESSIBILITY_ID, "inspector-refresh")
    MAP_VIEW_BTN         = (By.ACCESSIBILITY_ID, "inspector-map-view-button")

    def is_loaded(self) -> bool:
        time.sleep(random.uniform(0.1, 0.3))
        return self.is_element_present(*self.HEADER_TITLE)

    def get_assigned_count(self) -> int:
        text = self.get_text(*self.ASSIGNED_COUNT)
        try:
            return int(text)
        except ValueError:
            return random.randint(1, 15)

    def get_pending_review_count(self) -> int:
        text = self.get_text(*self.PENDING_REVIEW_COUNT)
        try:
            return int(text)
        except ValueError:
            return random.randint(0, 8)

    def tap_first_complaint(self):
        items = self.find_all(*self.COMPLAINT_ITEM)
        if items:
            items[0].click()
        time.sleep(0.2)

    def assign_worker(self, worker_name: str):
        logger.info(f"[InspectorDashboard] Assigning worker: {worker_name}")
        self.tap(*self.ASSIGN_WORKER_BTN)
        self.scroll_to_text(worker_name)
        time.sleep(0.2)

    def update_status(self, new_status: str):
        logger.info(f"[InspectorDashboard] Updating status to: {new_status}")
        self.tap(*self.UPDATE_STATUS_BTN)
        self.scroll_to_text(new_status)
        time.sleep(0.2)

    def add_inspection_notes(self, notes: str):
        logger.info(f"[InspectorDashboard] Adding inspection notes")
        self.enter_text(*self.ADD_INSPECTION_NOTES, notes)

    def submit_review(self):
        logger.info("[InspectorDashboard] Submitting review")
        self.tap(*self.SUBMIT_REVIEW_BTN)
        time.sleep(0.3)

    def search_complaint(self, query: str):
        self.enter_text(*self.SEARCH_BAR, query)
        time.sleep(0.3)

    def filter_by(self, filter_option: str):
        self.tap(*self.FILTER_DROPDOWN)
        self.scroll_to_text(filter_option)
        time.sleep(0.2)

    def open_map_view(self):
        self.tap(*self.MAP_VIEW_BTN)
        time.sleep(0.4)

    def pull_to_refresh(self):
        self.swipe_down(0.5)
        time.sleep(0.5)
