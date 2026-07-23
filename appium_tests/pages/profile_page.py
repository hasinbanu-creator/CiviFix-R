"""
CiviFix Appium — Profile Page
"""

import sys
import os
import time
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

logger = logging.getLogger("civifix.appium.profile")


class ProfilePage(BasePage):
    AVATAR_IMG         = (By.ACCESSIBILITY_ID, "profile-avatar-image")
    NAME_LABEL         = (By.ACCESSIBILITY_ID, "profile-name-label")
    EMAIL_LABEL        = (By.ACCESSIBILITY_ID, "profile-email-label")
    MOBILE_LABEL       = (By.ACCESSIBILITY_ID, "profile-mobile-label")
    ADDRESS_LABEL      = (By.ACCESSIBILITY_ID, "profile-address-label")
    EDIT_PROFILE_BTN   = (By.ACCESSIBILITY_ID, "edit-profile-button")
    CHANGE_AVATAR_BTN  = (By.ACCESSIBILITY_ID, "change-avatar-button")
    LOGOUT_BTN         = (By.ACCESSIBILITY_ID, "logout-button")
    LOGOUT_CONFIRM_BTN = (By.ACCESSIBILITY_ID, "logout-confirm-button")
    DARK_MODE_TOGGLE   = (By.ACCESSIBILITY_ID, "dark-mode-toggle")
    LANGUAGE_PICKER    = (By.ACCESSIBILITY_ID, "language-picker")
    NOTIFICATION_PREF  = (By.ACCESSIBILITY_ID, "notification-preferences")
    VERSION_LABEL      = (By.ACCESSIBILITY_ID, "app-version-label")
    PRIVACY_LINK       = (By.ACCESSIBILITY_ID, "privacy-policy-link")
    TERMS_LINK         = (By.ACCESSIBILITY_ID, "terms-of-service-link")

    def get_profile_name(self) -> str:
        return self.get_text(*self.NAME_LABEL)

    def get_email(self) -> str:
        return self.get_text(*self.EMAIL_LABEL)

    def tap_edit_profile(self):
        self.tap(*self.EDIT_PROFILE_BTN)

    def tap_change_avatar(self):
        self.tap(*self.CHANGE_AVATAR_BTN)

    def logout(self):
        logger.info("[ProfilePage] Logging out")
        self.tap(*self.LOGOUT_BTN)
        time.sleep(0.3)
        self.tap(*self.LOGOUT_CONFIRM_BTN)
        time.sleep(0.4)

    def toggle_dark_mode(self):
        logger.info("[ProfilePage] Toggling dark mode")
        self.tap(*self.DARK_MODE_TOGGLE)
        time.sleep(0.2)

    def is_dark_mode_enabled(self) -> bool:
        el = self.find(*self.DARK_MODE_TOGGLE)
        return el.get_attribute("checked") == "true"

    def change_language(self, lang: str):
        self.tap(*self.LANGUAGE_PICKER)
        self.scroll_to_text(lang)
        time.sleep(0.2)

    def get_app_version(self) -> str:
        return self.get_text(*self.VERSION_LABEL)
