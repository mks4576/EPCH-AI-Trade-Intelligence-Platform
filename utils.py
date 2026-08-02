"""
Utility Functions
EPCH AI Trade Intelligence Platform
Version 2.0
"""

import io
import pandas as pd

# ==========================================================
# Dashboard Metrics
# ==========================================================

def average_confidence(df: pd.DataFrame) -> float:
    """
    Calculate average confidence score.
    """

    if df.empty:
        return 0.0

    return round(df["confidence"].mean(), 1)


def average_potential(df: pd.DataFrame) -> float:
    """
    Calculate average buyer potential.
    """

    if df.empty:
        return 0.0

    return round(df["buyer_potential"].mean(), 1)


def average_market_fit(df: pd.DataFrame) -> float:
    """
    Calculate average market fit.
    """

    if df.empty:
        return 0.0

    return round(df["market_fit"].mean(), 1)


# ==========================================================
# Search & Filter
# ==========================================================

def search_buyers(df: pd.DataFrame, keyword: str) -> pd.DataFrame:
    """
    Search buyers across multiple columns.
    """

    if df.empty or not keyword:
        return df

    keyword = keyword.lower()

    mask = (
        df["company_name"].astype(str).str.lower().str.contains(keyword)
        | df["country"].astype(str).str.lower().str.contains(keyword)
        | df["buyer_type"].astype(str).str.lower().str.contains(keyword)
        | df["products"].astype(str).str.lower().str.contains(keyword)
    )

    return df[mask]


def filter_country(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """
    Filter by country.
    """

    if df.empty or country == "All":
        return df

    return df[df["country"] == country]


def filter_buyer_type(df: pd.DataFrame, buyer_type: str) -> pd.DataFrame:
    """
    Filter by buyer type.
    """

    if df.empty or buyer_type == "All":
        return df

    return df[df["buyer_type"] == buyer_type]


# ==========================================================
# Sorting
# ==========================================================

def sort_by_confidence(df: pd.DataFrame) -> pd.DataFrame:
    """
    Highest confidence first.
    """

    if df.empty:
        return df

    return df.sort_values(
        by="confidence",
        ascending=False,
        ignore_index=True,
    )


def sort_by_market_fit(df: pd.DataFrame) -> pd.DataFrame:
    """
    Highest market fit first.
    """

    if df.empty:
        return df

    return df.sort_values(
        by="market_fit",
        ascending=False,
        ignore_index=True,
    )


def sort_by_potential(df: pd.DataFrame) -> pd.DataFrame:
    """
    Highest buyer potential first.
    """

    if df.empty:
        return df

    return df.sort_values(
        by="buyer_potential",
        ascending=False,
        ignore_index=True,
    )


# ==========================================================
# Export Functions
# ==========================================================

def dataframe_to_csv(df: pd.DataFrame) -> bytes:
    """
    Convert DataFrame to CSV.
    """

    return df.to_csv(index=False).encode("utf-8")


def dataframe_to_excel(df: pd.DataFrame) -> bytes:
    """
    Convert DataFrame to Excel.
    """

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl",
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Buyers",
            index=False,
        )

    return output.getvalue()


# ==========================================================
# Data Formatting
# ==========================================================

def prepare_dataframe(buyers: list) -> pd.DataFrame:
    """
    Convert buyer list to DataFrame and
    add Serial Number column.
    """

    df = pd.DataFrame(buyers)

    if df.empty:
        return df

    df.insert(
        0,
        "S.No.",
        range(1, len(df) + 1),
    )

    return df


# ==========================================================
# Risk Summary
# ==========================================================

def risk_summary(df: pd.DataFrame) -> dict:
    """
    Count buyers by risk level.
    """

    if df.empty:
        return {}

    return (
        df["risk_level"]
        .value_counts()
        .to_dict()
    )


# ==========================================================
# Business Size Summary
# ==========================================================

def business_size_summary(df: pd.DataFrame) -> dict:
    """
    Count buyers by business size.
    """

    if df.empty:
        return {}

    return (
        df["business_size"]
        .value_counts()
        .to_dict()
    )