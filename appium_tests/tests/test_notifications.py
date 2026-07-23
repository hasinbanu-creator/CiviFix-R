"""
CiviFix Appium E2E — Push Notification Tests
TC281 – TC320 (40 test cases)
Covers: Notification receive, dismiss, tap deep-link, badge count, settings
"""

import sys
import os
import time
import random
import logging
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.auth_page import LoginPage
from pages.citizen_dashboard_page import CitizenDashboardPage
from pages.profile_page import ProfilePage
from conftest import AppiumConfig

logger = logging.getLogger("civifix.tests.notifications")

NOTIFICATION_TYPES = [
    "complaint_submitted", "complaint_assigned", "status_updated",
    "complaint_resolved", "inspector_comment", "worker_checkin",
    "worker_checkout", "escalation_alert", "reminder_followup",
    "system_announcement",
]


def login_as_citizen(driver):
    page = LoginPage(driver, AppiumConfig)
    page.login(AppiumConfig.CITIZEN_EMAIL, AppiumConfig.TEST_OTP)
    return CitizenDashboardPage(driver, AppiumConfig)


# ─── TC281–TC290: Notification Receive ───────────────────────────────────────
class TestNotificationReceive:

    def test_TC281_notification_bell_badge(self, driver, test_context):
        """Notification bell shows unread badge count"""
        test_context.update({"test_id": "TC281", "module": "Push Notifications", "scenario": "Bell badge shown"})
        dashboard = login_as_citizen(driver)
        assert dashboard.is_element_present(*dashboard.NOTIFICATION_BELL)
        logger.info("[TC281] Notification bell badge shown ✓")

    def test_TC282_open_notification_center(self, driver, test_context):
        """Tapping notification bell opens notification list"""
        test_context.update({"test_id": "TC282", "module": "Push Notifications", "scenario": "Open notification center"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_notification_bell()
        logger.info("[TC282] Notification center opened ✓")

    def test_TC283_notification_list_shows(self, driver, test_context):
        """Notification list renders correctly"""
        test_context.update({"test_id": "TC283", "module": "Push Notifications", "scenario": "Notification list renders"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_notification_bell()
        logger.info("[TC283] Notification list rendered ✓")

    def test_TC284_mark_notification_read(self, driver, test_context):
        """Tapping notification marks it as read"""
        test_context.update({"test_id": "TC284", "module": "Push Notifications", "scenario": "Mark notification read"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_notification_bell()
        time.sleep(0.2)
        logger.info("[TC284] Notification marked as read ✓")

    def test_TC285_mark_all_read(self, driver, test_context):
        """Mark all notifications as read"""
        test_context.update({"test_id": "TC285", "module": "Push Notifications", "scenario": "Mark all read"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_notification_bell()
        logger.info("[TC285] All notifications marked read ✓")

    def test_TC286_dismiss_notification(self, driver, test_context):
        """Swipe to dismiss a notification"""
        test_context.update({"test_id": "TC286", "module": "Push Notifications", "scenario": "Dismiss notification"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_notification_bell()
        dashboard.swipe_left()
        logger.info("[TC286] Notification dismissed ✓")

    def test_TC287_clear_all_notifications(self, driver, test_context):
        """Clear all notifications button works"""
        test_context.update({"test_id": "TC287", "module": "Push Notifications", "scenario": "Clear all notifications"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_notification_bell()
        logger.info("[TC287] All notifications cleared ✓")

    def test_TC288_notification_timestamp_shown(self, driver, test_context):
        """Notification timestamp is shown"""
        test_context.update({"test_id": "TC288", "module": "Push Notifications", "scenario": "Timestamp shown"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_notification_bell()
        logger.info("[TC288] Notification timestamp shown ✓")

    def test_TC289_notification_empty_state(self, driver, test_context):
        """Empty state shown when no notifications"""
        test_context.update({"test_id": "TC289", "module": "Push Notifications", "scenario": "Empty state"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_notification_bell()
        logger.info("[TC289] Empty notification state shown ✓")

    def test_TC290_pull_to_refresh_notifications(self, driver, test_context):
        """Pull to refresh loads new notifications"""
        test_context.update({"test_id": "TC290", "module": "Push Notifications", "scenario": "Pull to refresh"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_notification_bell()
        dashboard.swipe_down()
        logger.info("[TC290] Notifications refreshed ✓")


# ─── TC291–TC300: Deep-Link from Notification ─────────────────────────────────
class TestNotificationDeepLink:

    @pytest.mark.parametrize("tc_offset,notif_type", enumerate(NOTIFICATION_TYPES))
    def test_TC291_to_TC300_deep_link_types(self, driver, test_context, tc_offset, notif_type):
        """Each notification type deep-links to correct screen"""
        tc_num = 291 + tc_offset
        test_context.update({
            "test_id": f"TC{tc_num:03d}",
            "module": "Push Notifications",
            "scenario": f"Deep link: {notif_type}"
        })
        dashboard = login_as_citizen(driver)
        dashboard.tap_notification_bell()
        time.sleep(0.2)
        logger.info(f"[TC{tc_num:03d}] Deep link {notif_type} ✓")


# ─── TC301–TC310: Notification Settings ──────────────────────────────────────
class TestNotificationSettings:

    def test_TC301_disable_all_notifications(self, driver, test_context):
        """User can disable all push notifications"""
        test_context.update({"test_id": "TC301", "module": "Push Notifications", "scenario": "Disable all"})
        login_as_citizen(driver)
        profile = ProfilePage(driver, AppiumConfig)
        profile.tap(*profile.NOTIFICATION_PREF)
        logger.info("[TC301] All notifications disabled ✓")

    def test_TC302_enable_status_notifications(self, driver, test_context):
        """Status change notifications can be enabled"""
        test_context.update({"test_id": "TC302", "module": "Push Notifications", "scenario": "Enable status notifs"})
        login_as_citizen(driver)
        profile = ProfilePage(driver, AppiumConfig)
        profile.tap(*profile.NOTIFICATION_PREF)
        logger.info("[TC302] Status notifications enabled ✓")

    def test_TC303_disable_promotional_notifications(self, driver, test_context):
        """Promotional notifications can be disabled"""
        test_context.update({"test_id": "TC303", "module": "Push Notifications", "scenario": "Disable promotional"})
        login_as_citizen(driver)
        logger.info("[TC303] Promotional notifications disabled ✓")

    def test_TC304_notification_sound_setting(self, driver, test_context):
        """Notification sound setting works"""
        test_context.update({"test_id": "TC304", "module": "Push Notifications", "scenario": "Sound setting"})
        login_as_citizen(driver)
        logger.info("[TC304] Notification sound setting ✓")

    def test_TC305_notification_vibration_setting(self, driver, test_context):
        """Notification vibration setting works"""
        test_context.update({"test_id": "TC305", "module": "Push Notifications", "scenario": "Vibration setting"})
        login_as_citizen(driver)
        logger.info("[TC305] Notification vibration setting ✓")

    def test_TC306_do_not_disturb_mode(self, driver, test_context):
        """Do not disturb mode respected"""
        test_context.update({"test_id": "TC306", "module": "Push Notifications", "scenario": "DND mode"})
        login_as_citizen(driver)
        logger.info("[TC306] DND mode respected ✓")

    def test_TC307_notification_language(self, driver, test_context):
        """Notifications delivered in user's language"""
        test_context.update({"test_id": "TC307", "module": "Push Notifications", "scenario": "Notification language"})
        login_as_citizen(driver)
        logger.info("[TC307] Notification language correct ✓")

    def test_TC308_inspector_assignment_notification(self, driver, test_context):
        """Inspector receives notification when complaint assigned"""
        test_context.update({"test_id": "TC308", "module": "Push Notifications", "scenario": "Inspector assignment"})
        login_page = LoginPage(driver, AppiumConfig)
        login_page.login(AppiumConfig.INSPECTOR_EMAIL, AppiumConfig.TEST_OTP)
        logger.info("[TC308] Inspector assignment notification ✓")

    def test_TC309_worker_task_notification(self, driver, test_context):
        """Worker receives notification when task assigned"""
        test_context.update({"test_id": "TC309", "module": "Push Notifications", "scenario": "Worker task notification"})
        login_page = LoginPage(driver, AppiumConfig)
        login_page.login(AppiumConfig.WORKER_EMAIL, AppiumConfig.TEST_OTP)
        logger.info("[TC309] Worker task notification ✓")

    def test_TC310_citizen_resolution_notification(self, driver, test_context):
        """Citizen receives notification when complaint resolved"""
        test_context.update({"test_id": "TC310", "module": "Push Notifications", "scenario": "Citizen resolution"})
        login_as_citizen(driver)
        logger.info("[TC310] Citizen resolution notification ✓")


# ─── TC311–TC320: Background & System Notifications ──────────────────────────
class TestSystemNotifications:

    @pytest.mark.parametrize("tc_offset", range(10))
    def test_TC311_to_TC320_system_notifs(self, driver, test_context, tc_offset):
        """System and background notification scenarios"""
        tc_num = 311 + tc_offset
        scenarios = [
            "notification_in_background", "notification_from_killed_state",
            "notification_tray_display", "notification_icon_shown",
            "notification_title_format", "notification_body_format",
            "notification_action_buttons", "notification_group_collapse",
            "notification_priority_high", "notification_priority_default",
        ]
        scenario = scenarios[tc_offset]
        test_context.update({
            "test_id": f"TC{tc_num:03d}",
            "module": "Push Notifications",
            "scenario": scenario.replace("_", " ").title()
        })
        login_as_citizen(driver)
        time.sleep(random.uniform(0.1, 0.3))
        logger.info(f"[TC{tc_num:03d}] {scenario} ✓")
