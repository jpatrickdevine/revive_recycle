"""
Recycling Options Service for the Revive-Recycle Scanner.

Gives recycling recommendations through a layered approach:
  1. Brand-specific takeback programs (Apple Trade-In, Samsung, etc.)
  2. Universal retailer drop-off programs (Best Buy, Staples)
  3. Earth911 website search link (pre-filled with device + zip code)
  4. (Future) Earth911 API integration if access becomes available
"""

import os
import requests

from src.data.device_materials import get_materials_for_device
from src.data.takeback_programs import get_takeback_programs
from src.utils.fallback_links import get_fallback_links


BASE_URL = "http://api.earth911.com"


class RecyclingService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("EARTH911_API_KEY")

    def find_recycling_options(self, device_name: str, zip_code: str) -> dict:
        """
        Main entry point. Returns recycling options for a device near a zip code.

        Always returns:
          - Brand-matched take-back programs
          - Universal drop-off programs (Best Buy, Staples)
          - Earth911 search link

        If Earth911 API key is available, also returns:
          - Nearby recycling centers from Earth911's database
        """
        result = {
            "device": device_name,
            "zip_code": zip_code,
            "takeback_programs": get_takeback_programs(device_name),
            "search_links": get_fallback_links(device_name, zip_code),
            "centers": [],
        }

        # If we get an Earth911 API key, enrich with local center data
        if self.api_key:
            api_centers = self._fetch_earth911_centers(device_name, zip_code)
            if api_centers:
                result["centers"] = api_centers

        return result

    # -- Earth911 API Methods (if API key available) --

    def _fetch_earth911_centers(self, device_name: str, zip_code: str,
                                 max_results: int = 5) -> list:
        """Try to get nearby centers from Earth911. Returns empty list on failure."""
        try:
            postal_data = self._api_call("earth911.getPostalData", {
                "postal_code": zip_code,
                "country": "US",
            })
            lat = postal_data.get("latitude")
            lng = postal_data.get("longitude")

            if not lat or not lng:
                return []

            locations = self._api_call("earth911.searchLocations", {
                "latitude": lat,
                "longitude": lng,
            })

            centers = []
            for loc in locations[:max_results]:
                try:
                    details = self._api_call("earth911.getLocationDetails", {
                        "location_id": loc.get("location_id"),
                    })
                    centers.append(self._format_center(details))
                except Exception:
                    continue

            return centers

        except Exception:
            
            return []

    def _api_call(self, method: str, params: dict = None) -> dict:
        """Make a request to the Earth911 API."""
        if params is None:
            params = {}
        params["api_key"] = self.api_key

        response = requests.get(
            f"{BASE_URL}/{method}",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            raise Exception(f"Earth911 API error: {data['error']}")

        return data.get("result", data)

    def _format_center(self, details: dict) -> dict:
        """Format raw Earth911 data into a clean structure."""
        address_parts = [
            details.get("address"),
            details.get("city"),
            details.get("province"),
            details.get("postal_code"),
        ]
        address = ", ".join(part for part in address_parts if part)

        return {
            "name": details.get("description", "Recycling Center"),
            "address": address,
            "phone": details.get("phone"),
            "hours": details.get("hours"),
            "website": details.get("url"),
            "distance": details.get("distance"),
            "accepted_materials": details.get("materials", []),
            "cost": details.get("cost", "Contact for pricing"),
        }
