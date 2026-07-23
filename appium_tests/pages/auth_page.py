"""
CiviFix Appium — Auth Page
Covers: Login screen, OTP screen, Signup flow, Logout
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

logger = logging.getLogger("civifix.appium.auth")


class LoginPage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────
    EMAIL_INPUT       = (By.ACCESSIBILITY_ID, "login-email-input")
    CONTINUE_BTN      = (By.ACCESSIBILITY_ID, "login-continue-button")
    OTP_INPUT_1       = (By.ACCESSIBILITY_ID, "otp-input-0")
    OTP_VERIFY_BTN    = (By.ACCESSIBILITY_ID, "otp-verify-button")
    ERROR_TOAST       = (By.ACCESSIBILITY_ID, "error-toast")
    LOGO              = (By.ACCESSIBILITY_ID, "civifix-logo")
    SIGNUP_LINK       = (By.ACCESSIBILITY_ID, "go-to-signup")
    FORGOT_PWD_LINK   = (By.ACCESSIBILITY_ID, "forgot-password")

    def navigate(self):
        logger.info("[LoginPage] Launching login screen")
        time.sleep(random.uniform(0.1, 0.3))

    def enter_email(self, email: str):
        logger.info(f"[LoginPage] Entering email: {email}")
        self.enter_text(*self.EMAIL_INPUT, email)

    def tap_continue(self):
        logger.info("[LoginPage] Tapping Continue button")
        self.tap(*self.CONTINUE_BTN)

    def enter_otp(self, otp: str = "123456"):
        logger.info(f"[LoginPage] Entering OTP: {otp}")
        for i, digit in enumerate(otp[:6]):
            self.find(By.ACCESSIBILITY_ID, f"otp-input-{i}").send_keys(digit)
            time.sleep(0.05)

    def tap_verify(self):
        logger.info("[LoginPage] Tapping Verify OTP button")
        self.tap(*self.OTP_VERIFY_BTN)

    def login(self, email: str, otp: str = "123456"):
        self.navigate()
        self.enter_email(email)
        self.tap_continue()
        self.wait_for_element(*self.OTP_INPUT_1)
        self.enter_otp(otp)
        self.tap_verify()
        logger.info("[LoginPage] Login flow complete")
        time.sleep(random.uniform(0.2, 0.5))

    def get_error_message(self) -> str:
        if self.is_element_present(*self.ERROR_TOAST):
            return self.get_text(*self.ERROR_TOAST)
        return ""

    def tap_signup_link(self):
        self.tap(*self.SIGNUP_LINK)

    def is_logo_visible(self) -> bool:
        return self.is_element_present(*self.LOGO)


class SignupPage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────
    NAME_INPUT        = (By.ACCESSIBILITY_ID, "signup-name-input")
    EMAIL_INPUT       = (By.ACCESSIBILITY_ID, "signup-email-input")
    MOBILE_INPUT      = (By.ACCESSIBILITY_ID, "signup-mobile-input")
    NEXT_BTN          = (By.ACCESSIBILITY_ID, "signup-next-button")
    ADDRESS_INPUT     = (By.ACCESSIBILITY_ID, "signup-address-input")
    DISTRICT_DROPDOWN = (By.ACCESSIBILITY_ID, "signup-district-picker")
    WARD_DROPDOWN     = (By.ACCESSIBILITY_ID, "signup-ward-picker")
    SUBMIT_BTN        = (By.ACCESSIBILITY_ID, "signup-submit-button")
    OTP_INPUT         = (By.ACCESSIBILITY_ID, "otp-input-0")

    def navigate(self):
        logger.info("[SignupPage] Launching signup screen")
        time.sleep(random.uniform(0.1, 0.3))

    def fill_step_one(self, name: str, email: str, mobile: str):
        logger.info(f"[SignupPage] Step 1: name={name}, email={email}, mobile={mobile}")
        self.enter_text(*self.NAME_INPUT, name)
        self.enter_text(*self.EMAIL_INPUT, email)
        self.enter_text(*self.MOBILE_INPUT, mobile)
        self.tap(*self.NEXT_BTN)

    def fill_step_two(self, address: str, district: str = "Chennai", ward: str = "Ward 1"):
        logger.info(f"[SignupPage] Step 2: address={address}, district={district}")
        self.enter_text(*self.ADDRESS_INPUT, address)
        self.tap(*self.DISTRICT_DROPDOWN)
        self.scroll_to_text(district)
        self.tap(*self.WARD_DROPDOWN)
        self.scroll_to_text(ward)
        self.tap(*self.SUBMIT_BTN)

    def is_otp_screen_shown(self) -> bool:
        return self.is_element_present(*self.OTP_INPUT)


class OTPPage(BasePage):
    OTP_INPUTS    = [(By.ACCESSIBILITY_ID, f"otp-input-{i}") for i in range(6)]
    RESEND_BTN    = (By.ACCESSIBILITY_ID, "otp-resend-button")
    VERIFY_BTN    = (By.ACCESSIBILITY_ID, "otp-verify-button")
    TIMER_LABEL   = (By.ACCESSIBILITY_ID, "otp-timer-label")

    def enter_otp(self, otp: str):
        for i, digit in enumerate(otp[:6]):
            self.find(By.ACCESSIBILITY_ID, f"otp-input-{i}").send_keys(digit)
            time.sleep(0.05)

    def tap_resend(self):
        self.tap(*self.RESEND_BTN)

    def tap_verify(self):
        self.tap(*self.VERIFY_BTN)

    def get_timer_text(self) -> str:
        return self.get_text(*self.TIMER_LABEL)
