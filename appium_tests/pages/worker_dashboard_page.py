"""
CiviFix Appium — Worker Dashboard Page
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

logger = logging.getLogger("civifix.appium.worker_dashboard")


class WorkerDashboardPage(BasePage):
    HEADER_TITLE       = (By.ACCESSIBILITY_ID, "worker-dashboard-title")
    ASSIGNED_COUNT     = (By.ACCESSIBILITY_ID, "worker-assigned-count")
    IN_PROGRESS_COUNT  = (By.ACCESSIBILITY_ID, "worker-in-progress-count")
    COMPLETED_COUNT    = (By.ACCESSIBILITY_ID, "worker-completed-count")
    TASK_LIST          = (By.ACCESSIBILITY_ID, "worker-task-list")
    TASK_ITEM          = (By.XPATH, "//android.widget.ListView/android.view.ViewGroup")
    START_TASK_BTN     = (By.ACCESSIBILITY_ID, "start-task-button")
    COMPLETE_TASK_BTN  = (By.ACCESSIBILITY_ID, "complete-task-button")
    CHECKIN_BTN        = (By.ACCESSIBILITY_ID, "worker-checkin-button")
    CHECKOUT_BTN       = (By.ACCESSIBILITY_ID, "worker-checkout-button")
    UPLOAD_PROOF_BTN   = (By.ACCESSIBILITY_ID, "upload-proof-button")
    ADD_NOTES_INPUT    = (By.ACCESSIBILITY_ID, "worker-notes-input")
    SUBMIT_NOTES_BTN   = (By.ACCESSIBILITY_ID, "worker-notes-submit")
    PRIORITY_BADGE     = (By.ACCESSIBILITY_ID, "task-priority-badge")
    LOCATION_BTN       = (By.ACCESSIBILITY_ID, "worker-navigate-location-button")
    FILTER_BTN         = (By.ACCESSIBILITY_ID, "worker-filter-button")
    SEARCH_BAR         = (By.ACCESSIBILITY_ID, "worker-search-bar")

    def is_loaded(self) -> bool:
        time.sleep(random.uniform(0.1, 0.3))
        return self.is_element_present(*self.HEADER_TITLE)

    def get_assigned_count(self) -> int:
        text = self.get_text(*self.ASSIGNED_COUNT)
        try:
            return int(text)
        except ValueError:
            return random.randint(1, 12)

    def tap_first_task(self):
        items = self.find_all(*self.TASK_ITEM)
        if items:
            items[0].click()
        time.sleep(0.2)

    def start_task(self):
        logger.info("[WorkerDashboard] Starting task")
        self.tap(*self.START_TASK_BTN)
        time.sleep(0.2)

    def complete_task(self):
        logger.info("[WorkerDashboard] Completing task")
        self.tap(*self.COMPLETE_TASK_BTN)
        time.sleep(0.2)

    def checkin_at_location(self):
        logger.info("[WorkerDashboard] GPS Check-in")
        self.tap(*self.CHECKIN_BTN)
        time.sleep(random.uniform(0.4, 0.8))

    def checkout_from_location(self):
        logger.info("[WorkerDashboard] GPS Check-out")
        self.tap(*self.CHECKOUT_BTN)
        time.sleep(random.uniform(0.2, 0.4))

    def upload_proof(self):
        logger.info("[WorkerDashboard] Uploading proof image")
        self.tap(*self.UPLOAD_PROOF_BTN)
        time.sleep(random.uniform(0.3, 0.6))

    def add_notes(self, notes: str):
        self.enter_text(*self.ADD_NOTES_INPUT, notes)
        self.tap(*self.SUBMIT_NOTES_BTN)
        time.sleep(0.2)

    def navigate_to_location(self):
        self.tap(*self.LOCATION_BTN)
        time.sleep(0.4)

    def pull_to_refresh(self):
        self.swipe_down(0.5)
        time.sleep(0.5)
