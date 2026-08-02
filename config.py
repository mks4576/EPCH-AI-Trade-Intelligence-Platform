"""
Configuration
EPCH AI Trade Intelligence Platform
Version 2.0
"""

# ==========================================================
# Application
# ==========================================================

APP_NAME = "EPCH AI Trade Intelligence Platform"
APP_VERSION = "2.0.0"

# ==========================================================
# Google Gemini
# ==========================================================

# Stable model for Buyer Discovery
AI_MODEL = "gemini-2.0-flash"

# ==========================================================
# Buyer Discovery Options
# ==========================================================

COUNTRIES = [
    "United States",
    "United Kingdom",
    "Germany",
    "France",
    "Italy",
    "Spain",
    "Netherlands",
    "Belgium",
    "Sweden",
    "Denmark",
    "Norway",
    "Canada",
    "Australia",
    "Japan",
    "South Korea",
    "UAE",
    "Saudi Arabia",
    "Singapore",
    "Malaysia",
    "South Africa"
]

PRODUCT_CATEGORIES = [
    "Home Decor",
    "Furniture",
    "Textiles",
    "Home Furnishings",
    "Kitchenware",
    "Tableware",
    "Lighting",
    "Garden Decor",
    "Handmade Paper",
    "Gift Items",
    "Fashion Accessories",
    "Jewellery",
    "Leather Products",
    "Wooden Handicrafts",
    "Metal Handicrafts",
    "Stone Handicrafts",
    "Glassware",
    "Christmas Decorations",
    "Eco-friendly Products",
    "Sustainable Products"
]

BUYER_TYPES = [
    "Importer",
    "Wholesaler",
    "Distributor",
    "Retailer",
    "E-commerce",
    "Department Store",
    "Chain Store",
    "Buying House"
]

BUYER_COUNTS = [
    5,
    10,
    15,
    20
]

EXPORT_FORMATS = [
    "CSV",
    "Excel"
]

# ==========================================================
# Buyer Rating Scale
# ==========================================================

MAX_CONFIDENCE = 100
MAX_RATING = 5

# ==========================================================
# Dashboard Theme
# ==========================================================

PRIMARY_COLOR = "#0F62FE"
SUCCESS_COLOR = "#24A148"
WARNING_COLOR = "#F1C21B"
DANGER_COLOR = "#DA1E28"

# ==========================================================
# Default Values
# ==========================================================

DEFAULT_COUNTRY = "United States"
DEFAULT_CATEGORY = "Home Decor"
DEFAULT_BUYERS = 10
DEFAULT_BUYER_TYPE = "Importer"

# ==========================================================
# Retry Configuration
# ==========================================================

MAX_RETRIES = 3
RETRY_DELAY = 2

# ==========================================================
# Supported Export Extensions
# ==========================================================

CSV_FILENAME = "buyers.csv"
EXCEL_FILENAME = "buyers.xlsx"