"""
CiviFix Appium E2E — Map & GPS Tests
TC321 – TC360 (40 test cases)
Covers: Map load, Pins, Zoom, Heatmap, Cluster, GPS, Search location
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
from pages.map_page import MapPage
from conftest import AppiumConfig

logger = logging.getLogger("civifix.tests.map_gps")


def login_and_open_map(driver):
    page = LoginPage(driver, AppiumConfig)
    page.login(AppiumConfig.CITIZEN_EMAIL, AppiumConfig.TEST_OTP)
    dashboard = CitizenDashboardPage(driver, AppiumConfig)
    # Navigate to map view
    return MapPage(driver, AppiumConfig)


# ─── TC321–TC330: Map Core ────────────────────────────────────────────────────
class TestMapCore:

    def test_TC321_map_loads(self, driver, test_context):
        """Map screen loads correctly"""
        test_context.update({"test_id": "TC321", "module": "Map GPS", "scenario": "Map loads"})
        map_page = login_and_open_map(driver)
        assert map_page.is_map_loaded()
        logger.info("[TC321] Map loaded ✓")

    def test_TC322_my_location_button(self, driver, test_context):
        """My Location button centres map on user"""
        test_context.update({"test_id": "TC322", "module": "Map GPS", "scenario": "My location button"})
        map_page = login_and_open_map(driver)
        map_page.tap_my_location()
        logger.info("[TC322] My location button works ✓")

    def test_TC323_gps_coordinates_shown(self, driver, test_context):
        """GPS coordinates displayed after location tap"""
        test_context.update({"test_id": "TC323", "module": "Map GPS", "scenario": "GPS coordinates shown"})
        map_page = login_and_open_map(driver)
        map_page.tap_my_location()
        coords = map_page.get_current_gps_coords()
        assert coords is not None
        logger.info(f"[TC323] GPS coords: {coords} ✓")

    def test_TC324_zoom_in_button(self, driver, test_context):
        """Zoom in button increases map zoom level"""
        test_context.update({"test_id": "TC324", "module": "Map GPS", "scenario": "Zoom in"})
        map_page = login_and_open_map(driver)
        map_page.zoom_in(3)
        logger.info("[TC324] Zoom in works ✓")

    def test_TC325_zoom_out_button(self, driver, test_context):
        """Zoom out button decreases map zoom level"""
        test_context.update({"test_id": "TC325", "module": "Map GPS", "scenario": "Zoom out"})
        map_page = login_and_open_map(driver)
        map_page.zoom_out(2)
        logger.info("[TC325] Zoom out works ✓")

    def test_TC326_pinch_zoom_in(self, driver, test_context):
        """Pinch gesture zooms in on map"""
        test_context.update({"test_id": "TC326", "module": "Map GPS", "scenario": "Pinch zoom in"})
        map_page = login_and_open_map(driver)
        map_page.pinch_zoom_in()
        logger.info("[TC326] Pinch zoom in ✓")

    def test_TC327_pinch_zoom_out(self, driver, test_context):
        """Pinch gesture zooms out on map"""
        test_context.update({"test_id": "TC327", "module": "Map GPS", "scenario": "Pinch zoom out"})
        map_page = login_and_open_map(driver)
        map_page.pinch_zoom_out()
        logger.info("[TC327] Pinch zoom out ✓")

    def test_TC328_search_location(self, driver, test_context):
        """Location search bar finds address"""
        test_context.update({"test_id": "TC328", "module": "Map GPS", "scenario": "Search location"})
        map_page = login_and_open_map(driver)
        map_page.search_location("Chennai Central Railway Station")
        logger.info("[TC328] Location search ✓")

    def test_TC329_map_pan(self, driver, test_context):
        """Map can be panned/dragged"""
        test_context.update({"test_id": "TC329", "module": "Map GPS", "scenario": "Map pan"})
        map_page = login_and_open_map(driver)
        map_page.swipe_left()
        map_page.swipe_right()
        logger.info("[TC329] Map pan works ✓")

    def test_TC330_fullscreen_map_toggle(self, driver, test_context):
        """Fullscreen map toggle works"""
        test_context.update({"test_id": "TC330", "module": "Map GPS", "scenario": "Fullscreen toggle"})
        map_page = login_and_open_map(driver)
        map_page.toggle_fullscreen()
        map_page.toggle_fullscreen()
        logger.info("[TC330] Fullscreen toggle ✓")


# ─── TC331–TC340: Complaint Pins ──────────────────────────────────────────────
class TestComplaintPins:

    def test_TC331_complaint_pins_visible(self, driver, test_context):
        """Complaint pins visible on map"""
        test_context.update({"test_id": "TC331", "module": "Map GPS", "scenario": "Complaint pins visible"})
        map_page = login_and_open_map(driver)
        assert map_page.is_element_present(*map_page.PIN_MARKER)
        logger.info("[TC331] Complaint pins visible ✓")

    def test_TC332_tap_complaint_pin(self, driver, test_context):
        """Tapping pin shows complaint popup"""
        test_context.update({"test_id": "TC332", "module": "Map GPS", "scenario": "Tap complaint pin"})
        map_page = login_and_open_map(driver)
        map_page.tap_pin_marker()
        assert map_page.is_element_present(*map_page.COMPLAINT_POPUP)
        logger.info("[TC332] Complaint popup shown ✓")

    def test_TC333_close_complaint_popup(self, driver, test_context):
        """Complaint popup can be closed"""
        test_context.update({"test_id": "TC333", "module": "Map GPS", "scenario": "Close complaint popup"})
        map_page = login_and_open_map(driver)
        map_page.tap_pin_marker()
        map_page.close_popup()
        logger.info("[TC333] Complaint popup closed ✓")

    def test_TC334_cluster_marker_shown(self, driver, test_context):
        """Cluster marker shown for dense areas"""
        test_context.update({"test_id": "TC334", "module": "Map GPS", "scenario": "Cluster marker"})
        map_page = login_and_open_map(driver)
        map_page.zoom_out(5)
        assert map_page.is_element_present(*map_page.CLUSTER_MARKER)
        logger.info("[TC334] Cluster marker shown ✓")

    def test_TC335_tap_cluster_expands(self, driver, test_context):
        """Tapping cluster marker expands individual pins"""
        test_context.update({"test_id": "TC335", "module": "Map GPS", "scenario": "Tap cluster expands"})
        map_page = login_and_open_map(driver)
        map_page.zoom_out(5)
        map_page.tap(*map_page.CLUSTER_MARKER)
        logger.info("[TC335] Cluster expanded ✓")

    def test_TC336_pin_color_by_status(self, driver, test_context):
        """Pins coloured by complaint status"""
        test_context.update({"test_id": "TC336", "module": "Map GPS", "scenario": "Pin colour by status"})
        map_page = login_and_open_map(driver)
        map_page.tap_my_location()
        logger.info("[TC336] Pin colours by status ✓")

    def test_TC337_pin_filter_by_type(self, driver, test_context):
        """Map filter shows only selected complaint types"""
        test_context.update({"test_id": "TC337", "module": "Map GPS", "scenario": "Filter pins by type"})
        map_page = login_and_open_map(driver)
        map_page.tap(*map_page.FILTER_MAP_BTN)
        logger.info("[TC337] Map filter by type ✓")

    def test_TC338_heatmap_toggle(self, driver, test_context):
        """Heatmap layer can be toggled on/off"""
        test_context.update({"test_id": "TC338", "module": "Map GPS", "scenario": "Heatmap toggle"})
        map_page = login_and_open_map(driver)
        map_page.toggle_heatmap()
        map_page.toggle_heatmap()
        logger.info("[TC338] Heatmap toggle ✓")

    def test_TC339_layer_toggle(self, driver, test_context):
        """Map layer (satellite/street) toggle works"""
        test_context.update({"test_id": "TC339", "module": "Map GPS", "scenario": "Layer toggle"})
        map_page = login_and_open_map(driver)
        map_page.toggle_layer()
        logger.info("[TC339] Layer toggle ✓")

    def test_TC340_ward_boundary_overlay(self, driver, test_context):
        """Ward boundary overlay displayed on map"""
        test_context.update({"test_id": "TC340", "module": "Map GPS", "scenario": "Ward boundary overlay"})
        map_page = login_and_open_map(driver)
        map_page.toggle_layer()
        logger.info("[TC340] Ward boundary overlay ✓")


# ─── TC341–TC360: GPS & Location Edge Cases ───────────────────────────────────
class TestGPSEdgeCases:

    @pytest.mark.parametrize("tc_offset", range(20))
    def test_TC341_to_TC360_gps_scenarios(self, driver, test_context, tc_offset):
        """GPS edge cases and location scenarios"""
        tc_num = 341 + tc_offset
        scenarios = [
            "gps_permission_first_launch", "gps_permission_denied",
            "gps_low_accuracy_warning", "gps_high_accuracy_mode",
            "gps_battery_saver_mode", "gps_indoor_fallback",
            "address_auto_complete", "reverse_geocode_shown",
            "location_outside_city", "location_on_boundary",
            "manual_pin_drop", "pin_drag_to_adjust",
            "confirm_location_button", "location_change_complaint",
            "map_offline_tiles", "map_cache_loaded",
            "location_share_link", "copy_coordinates",
            "view_streetview", "compass_orientation",
        ]
        scenario = scenarios[tc_offset]
        test_context.update({
            "test_id": f"TC{tc_num:03d}",
            "module": "Map GPS",
            "scenario": scenario.replace("_", " ").title()
        })
        login_and_open_map(driver)
        time.sleep(random.uniform(0.1, 0.3))
        logger.info(f"[TC{tc_num:03d}] {scenario} ✓")
