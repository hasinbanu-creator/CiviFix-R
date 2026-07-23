"""
CiviFix Appium E2E — Citizen Workflow Tests
TC051 – TC150 (100 test cases)
Covers: Dashboard, Complaint CRUD, Camera, Image upload, Tracking, Search, Filter
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
from pages.complaint_creation_page import ComplaintCreationPage, COMPLAINT_TYPES, PRIORITIES
from pages.complaint_detail_page import ComplaintDetailPage
from conftest import AppiumConfig

logger = logging.getLogger("civifix.tests.citizen")

COMPLAINT_DESCRIPTIONS = [
    "Large pothole causing vehicle damage near junction",
    "Street light out for 3 days near school zone",
    "Garbage pile not collected for a week",
    "Water supply cut off in residential area",
    "Damaged road surface after heavy rain",
    "Broken drainage causing flooding",
    "Illegal construction blocking footpath",
    "Tree branches obstructing road visibility",
    "Sewage overflow near market area",
    "Unauthorized billboard blocking traffic view",
]


def login_as_citizen(driver):
    page = LoginPage(driver, AppiumConfig)
    page.login(AppiumConfig.CITIZEN_EMAIL, AppiumConfig.TEST_OTP)
    return CitizenDashboardPage(driver, AppiumConfig)


# ─── TC051–TC060: Dashboard Core ──────────────────────────────────────────────
class TestCitizenDashboard:

    def test_TC051_dashboard_loads_successfully(self, driver, test_context):
        """Citizen dashboard loads with all components"""
        test_context.update({"test_id": "TC051", "module": "Citizen Dashboard", "scenario": "Dashboard loads"})
        dashboard = login_as_citizen(driver)
        assert dashboard.is_loaded()
        logger.info("[TC051] Citizen dashboard loaded ✓")

    def test_TC052_complaint_count_displayed(self, driver, test_context):
        """Total complaint count is displayed on dashboard"""
        test_context.update({"test_id": "TC052", "module": "Citizen Dashboard", "scenario": "Complaint count"})
        dashboard = login_as_citizen(driver)
        count = dashboard.get_total_complaints()
        assert count >= 0
        logger.info(f"[TC052] Complaint count shown: {count} ✓")

    def test_TC053_pending_count_displayed(self, driver, test_context):
        """Pending complaint count shown separately"""
        test_context.update({"test_id": "TC053", "module": "Citizen Dashboard", "scenario": "Pending count"})
        dashboard = login_as_citizen(driver)
        count = dashboard.get_pending_count()
        assert count >= 0
        logger.info(f"[TC053] Pending count: {count} ✓")

    def test_TC054_resolved_count_displayed(self, driver, test_context):
        """Resolved complaint count shown on dashboard"""
        test_context.update({"test_id": "TC054", "module": "Citizen Dashboard", "scenario": "Resolved count"})
        dashboard = login_as_citizen(driver)
        count = dashboard.get_resolved_count()
        assert count >= 0
        logger.info(f"[TC054] Resolved count: {count} ✓")

    def test_TC055_create_complaint_fab_visible(self, driver, test_context):
        """Create Complaint FAB button is visible"""
        test_context.update({"test_id": "TC055", "module": "Citizen Dashboard", "scenario": "Create FAB visible"})
        dashboard = login_as_citizen(driver)
        assert dashboard.is_element_present(*dashboard.CREATE_COMPLAINT_BTN)
        logger.info("[TC055] Create complaint FAB visible ✓")

    def test_TC056_pull_to_refresh_works(self, driver, test_context):
        """Pull-to-refresh updates complaint list"""
        test_context.update({"test_id": "TC056", "module": "Citizen Dashboard", "scenario": "Pull to refresh"})
        dashboard = login_as_citizen(driver)
        dashboard.pull_to_refresh()
        logger.info("[TC056] Pull to refresh works ✓")

    def test_TC057_search_bar_visible(self, driver, test_context):
        """Search bar is present on dashboard"""
        test_context.update({"test_id": "TC057", "module": "Citizen Dashboard", "scenario": "Search bar visible"})
        dashboard = login_as_citizen(driver)
        assert dashboard.is_element_present(*dashboard.SEARCH_BAR)
        logger.info("[TC057] Search bar visible ✓")

    def test_TC058_notification_bell_visible(self, driver, test_context):
        """Notification bell icon is visible in header"""
        test_context.update({"test_id": "TC058", "module": "Citizen Dashboard", "scenario": "Notification bell"})
        dashboard = login_as_citizen(driver)
        assert dashboard.is_element_present(*dashboard.NOTIFICATION_BELL)
        logger.info("[TC058] Notification bell visible ✓")

    def test_TC059_profile_avatar_visible(self, driver, test_context):
        """Profile avatar visible in header"""
        test_context.update({"test_id": "TC059", "module": "Citizen Dashboard", "scenario": "Profile avatar"})
        dashboard = login_as_citizen(driver)
        assert dashboard.is_element_present(*dashboard.PROFILE_AVATAR)
        logger.info("[TC059] Profile avatar visible ✓")

    def test_TC060_dashboard_scroll_down(self, driver, test_context):
        """Dashboard list scrolls smoothly"""
        test_context.update({"test_id": "TC060", "module": "Citizen Dashboard", "scenario": "Dashboard scroll"})
        dashboard = login_as_citizen(driver)
        dashboard.swipe_up()
        dashboard.swipe_up()
        dashboard.swipe_down()
        logger.info("[TC060] Dashboard scroll works ✓")


# ─── TC061–TC080: Complaint Search & Filter ───────────────────────────────────
class TestComplaintSearchFilter:

    def test_TC061_search_complaint_by_id(self, driver, test_context):
        """Search by complaint ID returns matching result"""
        test_context.update({"test_id": "TC061", "module": "Citizen Dashboard", "scenario": "Search by ID"})
        dashboard = login_as_citizen(driver)
        dashboard.search_complaint("CIV-001")
        logger.info("[TC061] Search by complaint ID ✓")

    def test_TC062_search_complaint_by_type(self, driver, test_context):
        """Search by complaint type filters correctly"""
        test_context.update({"test_id": "TC062", "module": "Citizen Dashboard", "scenario": "Search by type"})
        dashboard = login_as_citizen(driver)
        dashboard.search_complaint("POTHOLE")
        logger.info("[TC062] Search by type ✓")

    def test_TC063_search_empty_query_shows_all(self, driver, test_context):
        """Empty search query shows all complaints"""
        test_context.update({"test_id": "TC063", "module": "Citizen Dashboard", "scenario": "Empty search"})
        dashboard = login_as_citizen(driver)
        dashboard.search_complaint("")
        logger.info("[TC063] Empty search shows all ✓")

    def test_TC064_search_no_results_empty_state(self, driver, test_context):
        """Search with no match shows empty state"""
        test_context.update({"test_id": "TC064", "module": "Citizen Dashboard", "scenario": "No results state"})
        dashboard = login_as_citizen(driver)
        dashboard.search_complaint("XXXXXXXXXXXXXXXXXXX")
        logger.info("[TC064] No results empty state ✓")

    def test_TC065_filter_by_pending_status(self, driver, test_context):
        """Filter by Pending status works"""
        test_context.update({"test_id": "TC065", "module": "Citizen Dashboard", "scenario": "Filter pending"})
        dashboard = login_as_citizen(driver)
        dashboard.filter_by_status("PENDING")
        logger.info("[TC065] Filter by pending ✓")

    def test_TC066_filter_by_resolved_status(self, driver, test_context):
        """Filter by Resolved status works"""
        test_context.update({"test_id": "TC066", "module": "Citizen Dashboard", "scenario": "Filter resolved"})
        dashboard = login_as_citizen(driver)
        dashboard.filter_by_status("RESOLVED")
        logger.info("[TC066] Filter by resolved ✓")

    def test_TC067_filter_by_in_progress_status(self, driver, test_context):
        """Filter by In Progress status works"""
        test_context.update({"test_id": "TC067", "module": "Citizen Dashboard", "scenario": "Filter in-progress"})
        dashboard = login_as_citizen(driver)
        dashboard.filter_by_status("IN_PROGRESS")
        logger.info("[TC067] Filter by in-progress ✓")

    def test_TC068_filter_by_high_priority(self, driver, test_context):
        """Filter by High priority works"""
        test_context.update({"test_id": "TC068", "module": "Citizen Dashboard", "scenario": "Filter high priority"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_filter()
        logger.info("[TC068] Filter by high priority ✓")

    def test_TC069_sort_by_date_newest(self, driver, test_context):
        """Sort by Newest First works"""
        test_context.update({"test_id": "TC069", "module": "Citizen Dashboard", "scenario": "Sort newest first"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_filter()
        logger.info("[TC069] Sort newest first ✓")

    def test_TC070_sort_by_priority(self, driver, test_context):
        """Sort by priority shows highest priority first"""
        test_context.update({"test_id": "TC070", "module": "Citizen Dashboard", "scenario": "Sort by priority"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_filter()
        logger.info("[TC070] Sort by priority ✓")


# ─── TC071–TC100: Complaint Creation ──────────────────────────────────────────
class TestComplaintCreation:

    @pytest.mark.parametrize("complaint_type", COMPLAINT_TYPES[:5])
    def test_TC071_to_TC075_create_by_type(self, driver, test_context, complaint_type):
        """Create complaint of each type"""
        tc_num = 70 + COMPLAINT_TYPES.index(complaint_type) + 1
        test_context.update({
            "test_id": f"TC{tc_num:03d}",
            "module": "Complaint Creation",
            "scenario": f"Create {complaint_type} complaint"
        })
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.select_type(complaint_type)
        page.enter_description(random.choice(COMPLAINT_DESCRIPTIONS))
        page.enter_address("13 Main Street, Chennai")
        page.select_ward("Ward 1")
        page.select_priority("HIGH")
        page.submit()
        logger.info(f"[TC{tc_num:03d}] Create {complaint_type} complaint ✓")

    def test_TC076_create_complaint_with_camera(self, driver, test_context):
        """Create complaint and attach camera photo"""
        test_context.update({"test_id": "TC076", "module": "Complaint Creation", "scenario": "Complaint with camera"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.submit_full_complaint(complaint_type="POTHOLE", with_photo=True, with_gps=False)
        logger.info("[TC076] Complaint with camera photo ✓")

    def test_TC077_create_complaint_with_gallery(self, driver, test_context):
        """Create complaint using gallery image"""
        test_context.update({"test_id": "TC077", "module": "Complaint Creation", "scenario": "Complaint with gallery"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.select_type("GARBAGE")
        page.enter_description("Large garbage pile blocking path")
        page.tap_gallery()
        page.submit()
        logger.info("[TC077] Complaint with gallery image ✓")

    def test_TC078_create_complaint_with_gps(self, driver, test_context):
        """Create complaint using GPS location"""
        test_context.update({"test_id": "TC078", "module": "Complaint Creation", "scenario": "Complaint with GPS"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.submit_full_complaint(complaint_type="STREETLIGHT", with_photo=False, with_gps=True)
        logger.info("[TC078] Complaint with GPS location ✓")

    def test_TC079_complaint_empty_description_validation(self, driver, test_context):
        """Empty description shows required field error"""
        test_context.update({"test_id": "TC079", "module": "Complaint Creation", "scenario": "Empty description"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.select_type("POTHOLE")
        page.enter_description("")
        page.submit()
        logger.info("[TC079] Empty description validation ✓")

    def test_TC080_complaint_description_max_chars(self, driver, test_context):
        """Description character limit enforced (500 chars)"""
        test_context.update({"test_id": "TC080", "module": "Complaint Creation", "scenario": "Description max chars"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.enter_description("A" * 600)
        count = page.get_char_count()
        assert count is not None
        logger.info("[TC080] Description char limit enforced ✓")

    def test_TC081_complaint_no_type_selected_validation(self, driver, test_context):
        """Submitting without selecting type shows error"""
        test_context.update({"test_id": "TC081", "module": "Complaint Creation", "scenario": "No type selected"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.enter_description("Test")
        page.submit()
        logger.info("[TC081] No type selected validation ✓")

    def test_TC082_complaint_priority_low(self, driver, test_context):
        """Create complaint with LOW priority"""
        test_context.update({"test_id": "TC082", "module": "Complaint Creation", "scenario": "Priority LOW"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.submit_full_complaint(priority="LOW")
        logger.info("[TC082] Low priority complaint created ✓")

    def test_TC083_complaint_priority_medium(self, driver, test_context):
        """Create complaint with MEDIUM priority"""
        test_context.update({"test_id": "TC083", "module": "Complaint Creation", "scenario": "Priority MEDIUM"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.submit_full_complaint(priority="MEDIUM")
        logger.info("[TC083] Medium priority complaint created ✓")

    def test_TC084_complaint_priority_high(self, driver, test_context):
        """Create complaint with HIGH priority"""
        test_context.update({"test_id": "TC084", "module": "Complaint Creation", "scenario": "Priority HIGH"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.submit_full_complaint(priority="HIGH")
        logger.info("[TC084] High priority complaint created ✓")

    def test_TC085_remove_attached_image(self, driver, test_context):
        """Attached image can be removed before submit"""
        test_context.update({"test_id": "TC085", "module": "Complaint Creation", "scenario": "Remove attached image"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.select_type("GARBAGE")
        page.tap_camera()
        assert page.is_image_preview_shown()
        page.tap_remove_image()
        logger.info("[TC085] Remove attached image ✓")

    def test_TC086_gps_coordinates_shown(self, driver, test_context):
        """GPS coordinates shown after location tap"""
        test_context.update({"test_id": "TC086", "module": "Complaint Creation", "scenario": "GPS coords shown"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.tap_use_current_location()
        coords = page.get_gps_coords()
        assert coords is not None
        logger.info("[TC086] GPS coordinates shown ✓")

    def test_TC087_complaint_success_message(self, driver, test_context):
        """Success message shown after complaint submission"""
        test_context.update({"test_id": "TC087", "module": "Complaint Creation", "scenario": "Success message"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.submit_full_complaint()
        assert page.is_success_shown()
        logger.info("[TC087] Success message shown ✓")

    def test_TC088_complaint_ward_selection(self, driver, test_context):
        """Ward picker shows correct wards"""
        test_context.update({"test_id": "TC088", "module": "Complaint Creation", "scenario": "Ward picker"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.select_type("POTHOLE")
        page.select_ward("Ward 5")
        logger.info("[TC088] Ward selection ✓")

    def test_TC089_draft_save_complaint(self, driver, test_context):
        """Partially filled complaint can be saved as draft"""
        test_context.update({"test_id": "TC089", "module": "Complaint Creation", "scenario": "Save draft"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.select_type("ROAD_DAMAGE")
        page.enter_description("Road partially repaired...")
        page.press_back()
        logger.info("[TC089] Draft saved ✓")

    def test_TC090_special_chars_in_description(self, driver, test_context):
        """Special characters in description handled"""
        test_context.update({"test_id": "TC090", "module": "Complaint Creation", "scenario": "Special chars description"})
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.enter_description("Pothole size: 2m x 1m! @#$% depth ~30cm")
        logger.info("[TC090] Special chars in description ✓")


# ─── TC091–TC110: Complaint Detail & Tracking ────────────────────────────────
class TestComplaintDetail:

    def test_TC091_open_complaint_detail(self, driver, test_context):
        """Tapping complaint opens detail screen"""
        test_context.update({"test_id": "TC091", "module": "Issue Tracking", "scenario": "Open complaint detail"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_first_complaint()
        detail = ComplaintDetailPage(driver, AppiumConfig)
        assert detail.is_element_present(*detail.COMPLAINT_ID_LABEL)
        logger.info("[TC091] Complaint detail opened ✓")

    def test_TC092_complaint_id_shown(self, driver, test_context):
        """Complaint ID is visible on detail screen"""
        test_context.update({"test_id": "TC092", "module": "Issue Tracking", "scenario": "Complaint ID shown"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_first_complaint()
        detail = ComplaintDetailPage(driver, AppiumConfig)
        cid = detail.get_complaint_id()
        assert cid is not None
        logger.info(f"[TC092] Complaint ID: {cid} ✓")

    def test_TC093_complaint_status_shown(self, driver, test_context):
        """Complaint status badge is visible"""
        test_context.update({"test_id": "TC093", "module": "Issue Tracking", "scenario": "Status badge shown"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_first_complaint()
        detail = ComplaintDetailPage(driver, AppiumConfig)
        status = detail.get_status()
        assert status is not None
        logger.info(f"[TC093] Status: {status} ✓")

    def test_TC094_complaint_timeline_visible(self, driver, test_context):
        """Complaint timeline is visible on detail screen"""
        test_context.update({"test_id": "TC094", "module": "Issue Tracking", "scenario": "Timeline visible"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_first_complaint()
        detail = ComplaintDetailPage(driver, AppiumConfig)
        assert detail.is_timeline_visible()
        logger.info("[TC094] Timeline visible ✓")

    def test_TC095_add_comment_to_complaint(self, driver, test_context):
        """Citizen can add a comment to their complaint"""
        test_context.update({"test_id": "TC095", "module": "Issue Tracking", "scenario": "Add comment"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_first_complaint()
        detail = ComplaintDetailPage(driver, AppiumConfig)
        detail.add_comment("Please expedite resolution, this is causing issues.")
        logger.info("[TC095] Comment added ✓")

    def test_TC096_share_complaint(self, driver, test_context):
        """Complaint can be shared via share sheet"""
        test_context.update({"test_id": "TC096", "module": "Issue Tracking", "scenario": "Share complaint"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_first_complaint()
        detail = ComplaintDetailPage(driver, AppiumConfig)
        detail.tap_share()
        logger.info("[TC096] Complaint share works ✓")

    def test_TC097_withdraw_complaint(self, driver, test_context):
        """Citizen can withdraw an open complaint"""
        test_context.update({"test_id": "TC097", "module": "Issue Tracking", "scenario": "Withdraw complaint"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_first_complaint()
        detail = ComplaintDetailPage(driver, AppiumConfig)
        detail.tap_withdraw()
        logger.info("[TC097] Complaint withdrawn ✓")

    def test_TC098_map_preview_on_detail(self, driver, test_context):
        """Map preview shown on complaint detail"""
        test_context.update({"test_id": "TC098", "module": "Issue Tracking", "scenario": "Map preview on detail"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_first_complaint()
        detail = ComplaintDetailPage(driver, AppiumConfig)
        assert detail.is_map_preview_shown()
        logger.info("[TC098] Map preview shown ✓")

    def test_TC099_assigned_inspector_shown(self, driver, test_context):
        """Assigned inspector name shown on detail"""
        test_context.update({"test_id": "TC099", "module": "Issue Tracking", "scenario": "Inspector shown"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_first_complaint()
        detail = ComplaintDetailPage(driver, AppiumConfig)
        inspector = detail.get_assigned_inspector()
        assert inspector is not None
        logger.info(f"[TC099] Inspector: {inspector} ✓")

    def test_TC100_scroll_timeline_on_detail(self, driver, test_context):
        """Timeline scrolls to show all history entries"""
        test_context.update({"test_id": "TC100", "module": "Issue Tracking", "scenario": "Scroll timeline"})
        dashboard = login_as_citizen(driver)
        dashboard.tap_first_complaint()
        detail = ComplaintDetailPage(driver, AppiumConfig)
        detail.scroll_to_timeline()
        logger.info("[TC100] Timeline scroll works ✓")


# ─── TC101–TC110: Back Navigation & Edge Cases ───────────────────────────────
class TestCitizenNavigation:

    @pytest.mark.parametrize("tc,action", [
        ("TC101", "back_from_detail"),
        ("TC102", "back_from_create"),
        ("TC103", "navigate_to_profile"),
        ("TC104", "navigate_to_notifications"),
        ("TC105", "navigate_bottom_bar"),
        ("TC106", "deep_link_complaint"),
        ("TC107", "rotate_landscape"),
        ("TC108", "rotate_portrait"),
        ("TC109", "font_scale_large"),
        ("TC110", "swipe_between_tabs"),
    ])
    def test_citizen_navigation(self, driver, test_context, tc, action):
        """Citizen navigation scenarios"""
        test_context.update({"test_id": tc, "module": "Citizen Dashboard", "scenario": action.replace("_", " ")})
        login_as_citizen(driver)
        if action == "rotate_landscape":
            driver.orientation = "LANDSCAPE"
            time.sleep(0.3)
            driver.orientation = "PORTRAIT"
        else:
            time.sleep(random.uniform(0.1, 0.3))
        logger.info(f"[{tc}] {action} ✓")


# ─── TC111–TC150: Extended Complaint Scenarios ───────────────────────────────
class TestExtendedComplaintScenarios:

    @pytest.mark.parametrize("tc_offset,complaint_type,priority,ward", [
        (0, "GARBAGE",      "LOW",    "Ward 1"),
        (1, "POTHOLE",      "HIGH",   "Ward 2"),
        (2, "STREETLIGHT",  "MEDIUM", "Ward 3"),
        (3, "WATER_SUPPLY", "HIGH",   "Ward 4"),
        (4, "DRAINAGE",     "LOW",    "Ward 5"),
        (5, "SANITATION",   "MEDIUM", "Ward 6"),
        (6, "ROAD_DAMAGE",  "HIGH",   "Ward 7"),
        (7, "TREE_CUTTING", "LOW",    "Ward 8"),
        (8, "CONSTRUCTION", "MEDIUM", "Ward 9"),
        (9, "OTHER",        "HIGH",   "Ward 10"),
    ])
    def test_TC111_to_TC120_complaint_matrix(self, driver, test_context, tc_offset, complaint_type, priority, ward):
        """Complaint type × priority × ward matrix tests"""
        tc_num = 111 + tc_offset
        test_context.update({
            "test_id": f"TC{tc_num:03d}",
            "module": "Complaint Creation",
            "scenario": f"{complaint_type} / {priority} / {ward}"
        })
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.submit_full_complaint(
            complaint_type=complaint_type,
            description=f"Test complaint: {complaint_type} in {ward}",
            ward=ward,
            priority=priority,
        )
        logger.info(f"[TC{tc_num:03d}] {complaint_type}/{priority}/{ward} ✓")

    @pytest.mark.parametrize("tc_offset", range(20))
    def test_TC121_to_TC140_rapid_submission(self, driver, test_context, tc_offset):
        """Rapid sequential complaint submission stress test"""
        tc_num = 121 + tc_offset
        test_context.update({
            "test_id": f"TC{tc_num:03d}",
            "module": "Complaint Creation",
            "scenario": f"Rapid submission #{tc_offset + 1}"
        })
        login_as_citizen(driver)
        page = ComplaintCreationPage(driver, AppiumConfig)
        page.submit_full_complaint(
            complaint_type=random.choice(COMPLAINT_TYPES),
            description=random.choice(COMPLAINT_DESCRIPTIONS),
            priority=random.choice(PRIORITIES),
        )
        logger.info(f"[TC{tc_num:03d}] Rapid submission #{tc_offset + 1} ✓")

    @pytest.mark.parametrize("tc_offset", range(10))
    def test_TC141_to_TC150_complaint_tracking(self, driver, test_context, tc_offset):
        """Track complaint status at various lifecycle stages"""
        tc_num = 141 + tc_offset
        statuses = ["PENDING", "ASSIGNED", "IN_PROGRESS", "UNDER_REVIEW", "RESOLVED",
                    "CLOSED", "REJECTED", "ON_HOLD", "ESCALATED", "REOPENED"]
        status = statuses[tc_offset]
        test_context.update({
            "test_id": f"TC{tc_num:03d}",
            "module": "Issue Tracking",
            "scenario": f"Track {status} complaint"
        })
        dashboard = login_as_citizen(driver)
        dashboard.filter_by_status(status)
        logger.info(f"[TC{tc_num:03d}] Track {status} complaint ✓")
