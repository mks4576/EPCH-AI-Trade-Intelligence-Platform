"""
Buyer Discovery Engine
EPCH AI Trade Intelligence Platform
"""

import json
import os

from dotenv import load_dotenv
from google import genai

from config import MODEL_NAME
from prompts import BUYER_DISCOVERY_PROMPT

# --------------------------------------------------------
# Load Environment Variables
# --------------------------------------------------------

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file.")

# --------------------------------------------------------
# Gemini Client
# --------------------------------------------------------

client = genai.Client(api_key=GOOGLE_API_KEY)

# --------------------------------------------------------
# Buyer Discovery
# --------------------------------------------------------

def discover_buyers(country, category, keywords, buyers):
    """
    Discover international buyers using Gemini AI.
    Returns:
        list[dict] on success
        dict with "error" on failure
    """

    prompt = BUYER_DISCOVERY_PROMPT.format(
        country=country,
        category=category,
        keywords=keywords if keywords else "None",
        buyers=buyers
    )

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        text = response.text.strip()

        # Remove accidental Markdown code fences
        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        buyers_list = json.loads(text)

        # Basic validation
        if not isinstance(buyers_list, list):
            return {
                "error": "Gemini did not return a JSON array."
            }

        required_fields = {
            "company_name",
            "country",
            "website",
            "buyer_type",
            "products",
            "reason",
            "confidence"
        }

        for buyer in buyers_list:

            if not isinstance(buyer, dict):
                return {
                    "error": "Invalid buyer object returned."
                }

            missing = required_fields - set(buyer.keys())

            if missing:
                return {
                    "error": f"Missing fields: {', '.join(missing)}"
                }

        return buyers_list

    except json.JSONDecodeError:

        return {
            "error": "Gemini returned invalid JSON.",
            "raw_response": text
        }

    except Exception as e:

        return {
            "error": str(e)
        }