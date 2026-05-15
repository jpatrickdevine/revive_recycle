"""
Builds a pre-filled Earth911 search URL for the user's device and zip code.
"""

from urllib.parse import quote

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data.device_materials import get_earth911_search_term


def build_earth911_search_url(device_name: str, zip_code: str) -> str:
    """Build a pre filled Earth911 web search URL."""
    material_term = get_earth911_search_term(device_name)
    return f"https://search.earth911.com/?what={quote(material_term)}&where={quote(zip_code)}"


def get_fallback_links(device_name: str, zip_code: str) -> list[dict]:
    """Return Earth911 search link for the user's device and location."""
    return [
        {
            "name": "Search Earth911",
            "url": build_earth911_search_url(device_name, zip_code),
        },
    ]
