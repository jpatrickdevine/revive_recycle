"""
Testing recycling service.

Run from project root:
  python -m tests.test_recycling_service
"""

import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

from src.data.device_materials import get_materials_for_device, get_earth911_search_term
from src.data.takeback_programs import get_takeback_programs
from src.utils.fallback_links import build_earth911_search_url, get_fallback_links

from src.services.recycling_service import RecyclingService


def pretty(data):
    print(json.dumps(data, indent=2, default=str))


def test_device_materials():
    print("=" * 55)
    print("TEST 1: Device Material Mapping")
    print("=" * 55)
    test_devices = ["iPhone 11", "MacBook Air", "iPad", "Samsung Galaxy S23", "Unknown Device"]
    for device in test_devices:
        materials = get_materials_for_device(device)
        search_term = get_earth911_search_term(device)
        print(f"\n  {device}")
        print(f"    Materials:    {materials}")
        print(f"    Search term:  {search_term}")
    print()


def test_takeback_programs():
    print("=" * 55)
    print("TEST 2: Brand Matching Take-Back Programs")
    print("=" * 55)
    test_devices = ["iPhone 11", "Samsung Galaxy S23", "MacBook Air", "Google Pixel 7"]
    for device in test_devices:
        programs = get_takeback_programs(device)
        print(f"\n  {device} -> {len(programs)} program(s):")
        for p in programs:
            print(f"    - {p['name']}")
            print(f"      {p['url']}")
    print()


def test_search_links():
    print("=" * 55)
    print("TEST 3: Earth911 Search Link")
    print("=" * 55)
    links = get_fallback_links("iPhone 11", "95616")
    for link in links:
        print(f"\n  {link['name']}")
        print(f"    URL:  {link['url']}")
    print()


def test_full_pipeline():
    print("=" * 55)
    print("TEST 4: Full Pipeline — find_recycling_options()")
    print("=" * 55)

    service = RecyclingService()

    test_cases = [
        ("iPhone 11", "10001"),     # New York
        ("Samsung Galaxy S23", "90210"),  # Beverly Hills
        ("MacBook Air", "60601"),   # Chicago
    ]

    for device, zip_code in test_cases:
        print(f"\n  --- {device} near {zip_code} ---\n")
        result = service.find_recycling_options(device, zip_code)
        pretty(result)
    print()


def test_all_devices():
    print("=" * 55)
    print("TEST 5: All MVP Device Coverage")
    print("=" * 55)
    all_devices = [
        "iPhone 14", "iPhone 13", "iPhone 12", "iPhone 11",
        "Samsung Galaxy S23", "Samsung Galaxy S22",
        "Google Pixel 7", "MacBook Air", "iPad", "Microsoft Surface Pro",
    ]
    zip_code = "95616"

    for device in all_devices:
        result = RecyclingService().find_recycling_options(device, zip_code)
        n_programs = len(result["takeback_programs"])
        n_links = len(result["search_links"])
        brand_program = result["takeback_programs"][0]["name"]
        print(f"  {device:<25} -> {brand_program:<25} + {n_programs - 1} universal + {n_links} search link(s)")
    print()


if __name__ == "__main__":
    test_device_materials()
    test_takeback_programs()
    test_search_links()
    test_full_pipeline()
    test_all_devices()
