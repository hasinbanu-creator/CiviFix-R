"""
CiviFix Appium — Complaint Detail Page
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

logger = logging.getLogger("civifix.appium.complaint_detail")


class ComplaintDetailPage(BasePage):
    COMPLAINT_ID_LABEL  = (By.ACCESSIBILITY_ID, "complaint-id-label")
    STATUS_BADGE        = (By.ACCESSIBILITY_ID, "complaint-status-badge")
    DESCRIPTION_TEXT    = (By.ACCESSIBILITY_ID, "complaint-description-text")
    COMPLAINT_TYPE      = (By.ACCESSIBILITY_ID, "complaint-type-label")
    PRIORITY_BADGE      = (By.ACCESSIBILITY_ID, "complaint-priority-badge")
    LOCATION_TEXT       = (By.ACCESSIBILITY_ID, "complaint-location-text")
    SUBMITTED_DATE      = (By.ACCESSIBILITY_ID, "complaint-submitted-date")
    PHOTO_THUMBNAIL     = (By.ACCESSIBILITY_ID, "complaint-photo-thumbnail")
    TIMELINE_VIEW       = (By.ACCESSIBILITY_ID, "complaint-timeline")
    COMMENTS_SECTION    = (By.ACCESSIBILITY_ID, "complaint-comments")
    ADD_COMMENT_INPUT   = (By.ACCESSIBILITY_ID, "add-comment-input")
    POST_COMMENT_BTN    = (By.ACCESSIBILITY_ID, "post-comment-button")
    BACK_BTN            = (By.ACCESSIBILITY_ID, "back-button")
    SHARE_BTN           = (By.ACCESSIBILITY_ID, "share-complaint-button")
    WITHDRAW_BTN        = (By.ACCESSIBILITY_ID, "withdraw-complaint-button")
    MAP_PREVIEW         = (By.ACCESSIBILITY_ID, "complaint-map-preview")
    INSPECTOR_LABEL     = (By.ACCESSIBILITY_ID, "assigned-inspector-label")
    WORKER_LABEL        = (By.ACCESSIBILITY_ID, "assigned-worker-label")

    def get_complaint_id(self) -> str:
        return self.get_text(*self.COMPLAINT_ID_LABEL)

    def get_status(self) -> str:
        return self.get_text(*self.STATUS_BADGE)

    def get_priority(self) -> str:
        return self.get_text(*self.PRIORITY_BADGE)

    def add_comment(self, comment: str):
        logger.info(f"[ComplaintDetail] Adding comment: {comment}")
        self.enter_text(*self.ADD_COMMENT_INPUT, comment)
        self.tap(*self.POST_COMMENT_BTN)
        time.sleep(0.3)

    def tap_back(self):
        self.tap(*self.BACK_BTN)

    def tap_share(self):
        self.tap(*self.SHARE_BTN)

    def tap_withdraw(self):
        logger.info("[ComplaintDetail] Withdrawing complaint")
        self.tap(*self.WITHDRAW_BTN)
        time.sleep(0.2)

    def is_timeline_visible(self) -> bool:
        return self.is_element_present(*self.TIMELINE_VIEW)

    def is_photo_shown(self) -> bool:
        return self.is_element_present(*self.PHOTO_THUMBNAIL)

    def is_map_preview_shown(self) -> bool:
        return self.is_element_present(*self.MAP_PREVIEW)

    def scroll_to_timeline(self):
        self.scroll_to_text("Timeline")

    def get_assigned_inspector(self) -> str:
        return self.get_text(*self.INSPECTOR_LABEL)

    def get_assigned_worker(self) -> str:
        return self.get_text(*self.WORKER_LABEL)
