"""
Maps device names to Earth911 material search terms.

Earth911 uses numeric material IDs internally. 
Will map these category keys to actual IDs (once/if we get API access) and call getMaterials. 
For now these strings match Earth911's website search categories.
"""

MATERIAL_CATEGORIES = {
    "cell_phones": "Cell Phones",
    "computers": "Computers",
    "laptops": "Laptops",
    "tablets": "Tablets",
    "lithium_batteries": "Lithium Batteries",
    "electronics": "Electronics",
}

# Each device maps to the material categories a recycler needs to accept
DEVICE_TO_MATERIALS = {
    # Phones
    "iPhone 14": ["cell_phones", "lithium_batteries"],
    "iPhone 13": ["cell_phones", "lithium_batteries"],
    "iPhone 12": ["cell_phones", "lithium_batteries"],
    "iPhone 11": ["cell_phones", "lithium_batteries"],
    "Samsung Galaxy S23": ["cell_phones", "lithium_batteries"],
    "Samsung Galaxy S22": ["cell_phones", "lithium_batteries"],
    "Google Pixel 7": ["cell_phones", "lithium_batteries"],

    # Laptops
    "MacBook Air": ["computers", "laptops", "lithium_batteries"],

    # Tablets
    "iPad": ["tablets", "lithium_batteries"],
    "Microsoft Surface Pro": ["tablets", "computers", "lithium_batteries"],
}


def get_materials_for_device(device_name: str) -> list[str]:
    """Return the material category keys for a given device."""
    materials = DEVICE_TO_MATERIALS.get(device_name)
    if materials:
        return materials

    # Fallback: try partial matching
    device_lower = device_name.lower()
    if any(kw in device_lower for kw in ["iphone", "galaxy", "pixel"]):
        return ["cell_phones", "lithium_batteries"]
    elif any(kw in device_lower for kw in ["macbook", "surface", "laptop"]):
        return ["computers", "laptops", "lithium_batteries"]
    elif "ipad" in device_lower:
        return ["tablets", "lithium_batteries"]

    return ["electronics"]


def get_earth911_search_term(device_name: str) -> str:
    """Return the best Earth911 website search term for a device."""
    materials = get_materials_for_device(device_name)
    primary = materials[0]
    return MATERIAL_CATEGORIES.get(primary, "Electronics")
