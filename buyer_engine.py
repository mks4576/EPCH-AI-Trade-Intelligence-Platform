"""
Buyer Discovery Engine
EPCH AI Trade Intelligence Platform
Version 2.0
"""

import json
import os
import time

from dotenv import load_dotenv
from google import genai

from config import (
    AI_MODEL,
    MAX_RETRIES,
    RETRY_DELAY,
    MAX_CONFIDENCE,
    MAX_RATING,
)
from prompts import BUYER_DISCOVERY_PROMPT

# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file.")

# ---------------------------------------------------------
# Gemini Client
# ---------------------------------------------------------

client = genai.Client(api_key=GOOGLE_API_KEY)

# ---------------------------------------------------------
# Required JSON Fields
# ---------------------------------------------------------

REQUIRED_FIELDS = {
    "company_name",
    "country",
    "website",
    "buyer_type",
    "products",
    "reason",
    "confidence",
    "buyer_potential",
    "market_fit",
    "business_size",
    "risk_level",
    "suggested_contact",
    "recommended_approach",
    "ai_summary",
}

# ---------------------------------------------------------
# Buyer Discovery
# ---------------------------------------------------------

def discover_buyers(
    country: str,
    category: str,
    keywords: str,
    buyers: int,
):
    """
    Discover international buyers using Gemini AI.

    Returns
    -------
    list[dict]
        Buyer records

    OR

    dict
        Error information
    """

    prompt = BUYER_DISCOVERY_PROMPT.format(
        country=country,
        category=category,
        keywords=keywords or "None",
        buyers=buyers,
    )

    last_error = None

    for attempt in range(MAX_RETRIES):

        try:

            response = client.models.generate_content(
                model=AI_MODEL,
                contents=prompt,
            )

            text = response.text.strip()

            # ------------------------------------------
            # Remove Markdown if Gemini adds it
            # ------------------------------------------

            if text.startswith("```"):

                text = (
                    text.replace("```json", "")
                        .replace("```", "")
                        .strip()
                )

            buyers_list = json.loads(text)

            if not isinstance(buyers_list, list):

                return {
                    "error": "Gemini returned an invalid response format."
                }

            # ------------------------------------------
            # Validate Buyer Objects
            # ------------------------------------------

            for buyer in buyers_list:

                if not isinstance(buyer, dict):

                    return {
                        "error": "Invalid buyer object returned."
                    }

                missing = REQUIRED_FIELDS - set(buyer.keys())

                if missing:

                    return {
                        "error": (
                            "Gemini response is missing fields: "
                            + ", ".join(sorted(missing))
                        )
                    }

                # -------------------------
                # Confidence
                # -------------------------

                buyer["confidence"] = max(
                    0,
                    min(
                        MAX_CONFIDENCE,
                        int(buyer.get("confidence", 80))
                    )
                )

                # -------------------------
                # Buyer Potential
                # -------------------------

                buyer["buyer_potential"] = max(
                    1,
                    min(
                        MAX_RATING,
                        int(buyer.get("buyer_potential", 3))
                    )
                )

                # -------------------------
                # Market Fit
                # -------------------------

                buyer["market_fit"] = max(
                    1,
                    min(
                        MAX_RATING,
                        int(buyer.get("market_fit", 3))
                    )
                )

            return buyers_list

        except json.JSONDecodeError:

            return {
                "error": (
                    "The AI returned invalid JSON.\n"
                    "Please try again."
                ),
                "raw_response": text,
            }

        except Exception as e:

            last_error = str(e)

            temporary_errors = [
                "503",
                "429",
                "UNAVAILABLE",
                "RESOURCE_EXHAUSTED",
            ]

            if (
                any(err in last_error for err in temporary_errors)
                and attempt < MAX_RETRIES - 1
            ):

                time.sleep(RETRY_DELAY)
                continue

            break

    # ---------------------------------------------------------
    # Friendly Error Messages
    # ---------------------------------------------------------

    if last_error:

        if "503" in last_error or "UNAVAILABLE" in last_error:

            return {
                "error": (
                    "🚦 Gemini AI is currently experiencing high demand.\n\n"
                    f"The application automatically retried {MAX_RETRIES} times,"
                    "but the service is still busy.\n\n"
                    "Please try again in a minute."
                )
            }

        if "429" in last_error:

            return {
                "error": (
                    "⏳ 🚦 Google Gemini API rate limit reached.\n\n"
                    "the application automatically retried the request,"
                    "but the free API quota has been temporarily exceeded.\n\n"
                    "This usually happens during rapid testing.\n\n"
                    "Please wait a few minutes and try again."
                )
            }

        return {
            "error": (
                "An unexpected error occurred.\n\n"
                f"{last_error}"
            )
        }

    return {
        "error": "Unknown error occurred."
    }