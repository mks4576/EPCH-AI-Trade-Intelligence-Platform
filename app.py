"""
EPCH AI Trade Intelligence Platform
Version 2.0
"""

import pandas as pd
import streamlit as st

from buyer_engine import discover_buyers
from utils import dataframe_to_csv, dataframe_to_excel

from config import (
    COUNTRIES,
    PRODUCT_CATEGORIES,
    BUYER_TYPES,
    BUYER_COUNTS,
    EXPORT_FORMATS,
    APP_VERSION,
    AI_MODEL,
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="EPCH AI Trade Intelligence Platform",
    page_icon="🌍",
    layout="wide",
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("🌍 EPCH AI")

    st.markdown("---")

    st.subheader("Project Information")

    st.write(f"**Version:** {APP_VERSION}")
    st.write(f"**Model:** {AI_MODEL}")
    st.write("**Framework:** Streamlit")

    st.markdown("---")

    st.subheader("Current Features")

    st.success("Buyer Discovery")
    st.success("Google Gemini")
    st.success("CSV Export")
    st.success("Excel Export")

    st.markdown("---")

    st.info(
        "AI-powered Trade Intelligence Platform\n\n"
        "Built using Python + Streamlit + Google Gemini."
    )

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🌍 EPCH AI Trade Intelligence Platform")

st.caption(
    "AI-powered Buyer Discovery & Trade Intelligence"
)

st.markdown("---")

# --------------------------------------------------
# Search Form
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    country = st.selectbox(
        "🌎 Export Destination",
        COUNTRIES
    )

    category = st.selectbox(
        "📦 Product Category",
        PRODUCT_CATEGORIES
    )

    keywords = st.text_input(
        "🔍 Keywords",
        placeholder="Example: Sustainable, Handmade, Luxury"
    )

with col2:

    buyer_type = st.selectbox(
        "🏢 Buyer Type",
        BUYER_TYPES
    )

    buyers = st.selectbox(
        "👥 Number of Buyers",
        BUYER_COUNTS
    )

    export_format = st.selectbox(
        "📥 Export Format",
        EXPORT_FORMATS
    )

st.markdown("")

search = st.button(
    "🚀 Discover Buyers",
    use_container_width=True
)

# --------------------------------------------------
# Search
# --------------------------------------------------

if search:

    with st.spinner("Searching international buyers..."):

        result = discover_buyers(
            country=country,
            category=category,
            keywords=f"{buyer_type}, {keywords}",
            buyers=buyers
        )

    # -------------------------------
    # Error Handling
    # -------------------------------

    if isinstance(result, dict) and "error" in result:

        st.error(result["error"])

        if "raw_response" in result:

            st.text_area(
                "Gemini Response",
                result["raw_response"],
                height=400
            )

    else:

        df = pd.DataFrame(result)

        st.success(f"{len(df)} buyers found.")

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = dataframe_to_csv(df)
        excel = dataframe_to_excel(df)

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                "📄 Download CSV",
                csv,
                file_name="buyers.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col2:

            st.download_button(
                "📊 Download Excel",
                excel,
                file_name="buyers.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Developed by Manish Kumar | Version 2.0"
)