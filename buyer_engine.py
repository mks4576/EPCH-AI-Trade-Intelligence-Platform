"""
Buyer Discovery Engine
EPCH AI Trade Intelligence Platform
Version 2.0
"""

import json
import os

from dotenv import load_dotenv
from google import genai

from config import AI_MODEL
from prompts import BUYER_DISCOVERY_PROMPT

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found in .env file."
    )

# --------------------------------------------------
# Gemini Client
# --------------------------------------------------

client = genai.Client(api_key=GOOGLE_API_KEY)

# --------------------------------------------------
# Buyer Discovery
# --------------------------------------------------

def discover_buyers(country, category, keywords, buyers):
    """
    Discover international buyers using Google Gemini.

    Returns:
        list[dict] on success
        dict on error
    """

    prompt = BUYER_DISCOVERY_PROMPT.format(
        country=country,
        category=category,
        keywords=keywords if keywords else "None",
        buyers=buyers
    )

    try:

        response = client.models.generate_content(
            model=AI_MODEL,
            contents=prompt
        )

        text = response.text.strip()

        # Remove Markdown code fences if present
        if text.startswith("```"):

            text = (
                text.replace("```json", "")
                    .replace("```", "")
                    .strip()
            )

        buyers_list = json.loads(text)

        if not isinstance(buyers_list, list):

            return {
                "error": "Gemini did not return a JSON array."
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