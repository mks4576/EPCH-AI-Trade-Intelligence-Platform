"""
Utility Functions
EPCH AI Trade Intelligence Platform
"""

import io
import pandas as pd


# --------------------------------------------------------
# Dashboard Metrics
# --------------------------------------------------------

def average_confidence(buyers):
    """
    Calculate average confidence score.
    """

    if not buyers:
        return 0

    scores = []

    for buyer in buyers:

        confidence = buyer.get("confidence", 0)

        if isinstance(confidence, (int, float)):
            scores.append(confidence)

    if not scores:
        return 0

    return round(sum(scores) / len(scores), 1)


# --------------------------------------------------------
# Search Buyers
# --------------------------------------------------------

def search_buyers(buyers, keyword):
    """
    Search buyers by company, country,
    buyer type or products.
    """

    if not keyword:
        return buyers

    keyword = keyword.lower()

    filtered = []

    for buyer in buyers:

        text = " ".join([
            buyer.get("company_name", ""),
            buyer.get("country", ""),
            buyer.get("buyer_type", ""),
            buyer.get("products", "")
        ]).lower()

        if keyword in text:
            filtered.append(buyer)

    return filtered


# --------------------------------------------------------
# DataFrame
# --------------------------------------------------------

def buyers_dataframe(buyers):

    return pd.DataFrame(buyers)


# --------------------------------------------------------
# CSV Export
# --------------------------------------------------------

def dataframe_to_csv(df):

    return df.to_csv(index=False).encode("utf-8")


# --------------------------------------------------------
# Excel Export
# --------------------------------------------------------

def dataframe_to_excel(df):

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Buyers"
        )

    return output.getvalue()
# --------------------------------------------------------
# JSON Response to DataFrame
# --------------------------------------------------------

import json


def json_to_dataframe(response_text):
    """
    Converts Gemini JSON response into a Pandas DataFrame.
    """

    try:

        # Remove markdown code fences if Gemini returns them
        cleaned = (
            response_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        buyers = json.loads(cleaned)

        if isinstance(buyers, dict):
            buyers = [buyers]

        return pd.DataFrame(buyers)

    except Exception as e:
        raise Exception(f"Unable to parse Gemini JSON:\n{e}")