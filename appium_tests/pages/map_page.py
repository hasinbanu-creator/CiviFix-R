"""
CiviFix Appium — Map / GPS Page
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

logger = logging.getLogger("civifix.appium.map")


class MapPage(BasePage):
    MAP_VIEW           = (By.ACCESSIBILITY_ID, "map-view-container")
    MY_LOCATION_BTN    = (By.ACCESSIBILITY_ID, "map-my-location-button")
    ZOOM_IN_BTN        = (By.ACCESSIBILITY_ID, "map-zoom-in")
    ZOOM_OUT_BTN       = (By.ACCESSIBILITY_ID, "map-zoom-out")
    PIN_MARKER         = (By.ACCESSIBILITY_ID, "map-complaint-pin")
    COMPLAINT_POPUP    = (By.ACCESSIBILITY_ID, "map-complaint-popup")
    CLOSE_POPUP_BTN    = (By.ACCESSIBILITY_ID, "map-popup-close")
    SEARCH_LOCATION    = (By.ACCESSIBILITY_ID, "map-search-location")
    LAYER_TOGGLE       = (By.ACCESSIBILITY_ID, "map-layer-toggle")
    HEATMAP_TOGGLE     = (By.ACCESSIBILITY_ID, "heatmap-toggle")
    GPS_COORDS_LABEL   = (By.ACCESSIBILITY_ID, "gps-coordinates-display")
    CLUSTER_MARKER     = (By.ACCESSIBILITY_ID, "map-cluster-marker")
    FILTER_MAP_BTN     = (By.ACCESSIBILITY_ID, "map-filter-button")
    FULL_SCREEN_BTN    = (By.ACCESSIBILITY_ID, "map-fullscreen-button")

    def is_map_loaded(self) -> bool:
        time.sleep(random.uniform(0.2, 0.5))
        return self.is_element_present(*self.MAP_VIEW)

    def tap_my_location(self):
        logger.info("[MapPage] Tapping My Location button")
        self.tap(*self.MY_LOCATION_BTN)
        time.sleep(random.uniform(0.4, 0.8))

    def zoom_in(self, times: int = 1):
        for _ in range(times):
            self.tap(*self.ZOOM_IN_BTN)
            time.sleep(0.15)

    def zoom_out(self, times: int = 1):
        for _ in range(times):
            self.tap(*self.ZOOM_OUT_BTN)
            time.sleep(0.15)

    def tap_pin_marker(self):
        logger.info("[MapPage] Tapping complaint pin marker")
        self.tap(*self.PIN_MARKER)
        time.sleep(0.3)

    def close_popup(self):
        self.tap(*self.CLOSE_POPUP_BTN)

    def search_location(self, query: str):
        self.enter_text(*self.SEARCH_LOCATION, query)
        time.sleep(0.4)

    def toggle_heatmap(self):
        logger.info("[MapPage] Toggling heatmap layer")
        self.tap(*self.HEATMAP_TOGGLE)
        time.sleep(0.2)

    def toggle_layer(self):
        self.tap(*self.LAYER_TOGGLE)
        time.sleep(0.2)

    def get_current_gps_coords(self) -> str:
        return self.get_text(*self.GPS_COORDS_LABEL)

    def toggle_fullscreen(self):
        self.tap(*self.FULL_SCREEN_BTN)
        time.sleep(0.2)

    def pinch_zoom_in(self):
        logger.debug("[MapPage] Pinch zoom in (simulated)")
        time.sleep(0.2)

    def pinch_zoom_out(self):
        logger.debug("[MapPage] Pinch zoom out (simulated)")
        time.sleep(0.2)
