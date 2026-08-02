"""
Configuration File
EPCH AI Trade Intelligence Platform
"""

# --------------------------------------------------------
# Application
# --------------------------------------------------------

APP_NAME = "Export Promotion Council of India : AI Trade Intelligence Platform"

APP_ICON = "🌍"

PAGE_LAYOUT = "wide"

# --------------------------------------------------------
# Product Categories
# --------------------------------------------------------

CATEGORIES = [
    "Home Decor",
    "Furniture",
    "Lighting",
    "Kitchenware",
    "Fashion Accessories",
    "Textiles",
    "Carpets & Rugs",
    "Christmas Decorations",
    "Garden Decor",
    "Gifts & Crafts",
]

# --------------------------------------------------------
# Target Countries
# --------------------------------------------------------

QUICK_COUNTRIES = [
    "USA",
    "Canada",
    "Germany",
    "France",
    "United Kingdom",
    "Australia",
    "Japan",
    "UAE",
]

# --------------------------------------------------------
# Fair Information
# --------------------------------------------------------

FAIR_INFO = {
    "name": "IHGF Delhi Fair",
    "organizer": "Export Promotion Council for Handicrafts (EPCH)",
    "venue": "India Expo Centre & Mart, Greater Noida",
    "website": "https://ihgfdelhifair.in",
}

# --------------------------------------------------------
# Gemini
# --------------------------------------------------------

MODEL_NAME = "gemini-flash-latest"

DEFAULT_BUYERS = 10

MAX_BUYERS = 25