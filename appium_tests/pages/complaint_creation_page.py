"""
CiviFix Appium — Complaint Creation Page
Covers: Type selection, description, location, camera, image, submit
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

logger = logging.getLogger("civifix.appium.complaint_creation")

COMPLAINT_TYPES = [
    "GARBAGE", "POTHOLE", "STREETLIGHT", "WATER_SUPPLY",
    "DRAINAGE", "SANITATION", "ROAD_DAMAGE", "TREE_CUTTING",
    "CONSTRUCTION", "OTHER"
]
PRIORITIES = ["LOW", "MEDIUM", "HIGH"]


class ComplaintCreationPage(BasePage):
    # ── Locators ─────────────────────────────────────────────────────────
    SCREEN_TITLE        = (By.ACCESSIBILITY_ID, "create-complaint-title")
    TYPE_PICKER         = (By.ACCESSIBILITY_ID, "complaint-type-picker")
    DESCRIPTION_INPUT   = (By.ACCESSIBILITY_ID, "complaint-description-input")
    ADDRESS_INPUT       = (By.ACCESSIBILITY_ID, "complaint-address-input")
    WARD_PICKER         = (By.ACCESSIBILITY_ID, "complaint-ward-picker")
    PRIORITY_PICKER     = (By.ACCESSIBILITY_ID, "complaint-priority-picker")
    CAMERA_BTN          = (By.ACCESSIBILITY_ID, "complaint-camera-button")
    GALLERY_BTN         = (By.ACCESSIBILITY_ID, "complaint-gallery-button")
    LOCATION_BTN        = (By.ACCESSIBILITY_ID, "complaint-location-button")
    MAP_PIN             = (By.ACCESSIBILITY_ID, "complaint-map-pin")
    SUBMIT_BTN          = (By.ACCESSIBILITY_ID, "complaint-submit-button")
    SUCCESS_MSG         = (By.ACCESSIBILITY_ID, "complaint-success-message")
    ERROR_MSG           = (By.ACCESSIBILITY_ID, "complaint-error-message")
    CHAR_COUNT_LABEL    = (By.ACCESSIBILITY_ID, "description-char-count")
    REQUIRED_ERROR      = (By.XPATH, "//android.widget.TextView[contains(@text,'required')]")
    IMAGE_PREVIEW       = (By.ACCESSIBILITY_ID, "complaint-image-preview")
    REMOVE_IMAGE_BTN    = (By.ACCESSIBILITY_ID, "remove-image-button")
    GPS_COORDS_LABEL    = (By.ACCESSIBILITY_ID, "gps-coordinates-label")

    def select_type(self, complaint_type: str):
        logger.info(f"[ComplaintCreation] Selecting type: {complaint_type}")
        self.tap(*self.TYPE_PICKER)
        self.scroll_to_text(complaint_type)
        time.sleep(0.2)

    def enter_description(self, text: str):
        logger.info(f"[ComplaintCreation] Entering description ({len(text)} chars)")
        self.enter_text(*self.DESCRIPTION_INPUT, text)

    def enter_address(self, address: str):
        self.enter_text(*self.ADDRESS_INPUT, address)

    def select_ward(self, ward: str):
        self.tap(*self.WARD_PICKER)
        self.scroll_to_text(ward)
        time.sleep(0.15)

    def select_priority(self, priority: str):
        self.tap(*self.PRIORITY_PICKER)
        self.scroll_to_text(priority)
        time.sleep(0.15)

    def tap_camera(self):
        logger.info("[ComplaintCreation] Tapping Camera button")
        self.tap(*self.CAMERA_BTN)
        time.sleep(random.uniform(0.3, 0.6))

    def tap_gallery(self):
        logger.info("[ComplaintCreation] Tapping Gallery button")
        self.tap(*self.GALLERY_BTN)
        time.sleep(random.uniform(0.2, 0.4))

    def tap_use_current_location(self):
        logger.info("[ComplaintCreation] Tapping Use Current Location")
        self.tap(*self.LOCATION_BTN)
        time.sleep(random.uniform(0.4, 0.8))  # GPS acquisition

    def submit(self):
        logger.info("[ComplaintCreation] Submitting complaint")
        self.tap(*self.SUBMIT_BTN)
        time.sleep(random.uniform(0.3, 0.6))

    def submit_full_complaint(
        self,
        complaint_type: str = "POTHOLE",
        description: str = "Large pothole affecting traffic flow",
        address: str = "13 Main Street, Chennai",
        ward: str = "Ward 1",
        priority: str = "HIGH",
        with_photo: bool = True,
        with_gps: bool = True,
    ):
        self.select_type(complaint_type)
        self.enter_description(description)
        self.enter_address(address)
        self.select_ward(ward)
        self.select_priority(priority)
        if with_photo:
            self.tap_camera()
        if with_gps:
            self.tap_use_current_location()
        self.submit()

    def is_success_shown(self) -> bool:
        return self.is_element_present(*self.SUCCESS_MSG)

    def is_error_shown(self) -> bool:
        return self.is_element_present(*self.ERROR_MSG)

    def get_error_message(self) -> str:
        if self.is_error_shown():
            return self.get_text(*self.ERROR_MSG)
        return ""

    def is_image_preview_shown(self) -> bool:
        return self.is_element_present(*self.IMAGE_PREVIEW)

    def tap_remove_image(self):
        self.tap(*self.REMOVE_IMAGE_BTN)

    def get_char_count(self) -> str:
        return self.get_text(*self.CHAR_COUNT_LABEL)

    def get_gps_coords(self) -> str:
        return self.get_text(*self.GPS_COORDS_LABEL)
