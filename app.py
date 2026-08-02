"""
EPCH AI Trade Intelligence Platform
Version 2.0
Executive AI Dashboard
"""

import pandas as pd
import streamlit as st

from buyer_engine import discover_buyers

from utils import (
    average_confidence,
    average_market_fit,
    average_potential,
    dataframe_to_csv,
    dataframe_to_excel,
)

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
    st.write(f"**AI Model:** {AI_MODEL}")

    st.markdown("---")

    st.success("✅ Buyer Discovery")
    st.success("✅ AI Buyer Intelligence")
    st.success("✅ CSV Export")
    st.success("✅ Excel Export")

    st.markdown("---")

    st.info(
        """
Enterprise AI Platform

Designed for Export Promotion Councils,
Exporters and International Trade Teams.
"""
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
# Search Panel
# --------------------------------------------------

left, right = st.columns(2)

with left:

    country = st.selectbox(
        "🌎 Export Destination",
        COUNTRIES,
    )

    category = st.selectbox(
        "📦 Product Category",
        PRODUCT_CATEGORIES,
    )

    keywords = st.text_input(
        "🔍 Keywords",
        placeholder="Luxury, Sustainable, Handmade...",
    )

with right:

    buyer_type = st.selectbox(
        "🏢 Buyer Type",
        BUYER_TYPES,
    )

    buyers = st.selectbox(
        "👥 Number of Buyers",
        BUYER_COUNTS,
    )

    export_format = st.selectbox(
        "📥 Export Format",
        EXPORT_FORMATS,
    )

st.markdown("")

search = st.button(
    "🚀 Discover Buyers",
    width="stretch",
)

# --------------------------------------------------
# Buyer Discovery
# --------------------------------------------------

if search:

    with st.spinner("🔍 AI is discovering international buyers..."):

        result = discover_buyers(
            country=country,
            category=category,
            keywords=f"{buyer_type}, {keywords}",
            buyers=buyers,
        )

    if isinstance(result, dict):

        st.error(result.get("error", "Unknown error"))

        if "raw_response" in result:

            st.text_area(
                "Gemini Raw Response",
                result["raw_response"],
                height=300,
            )

    else:

        from utils import prepare_dataframe

        df = prepare_dataframe(result)

        st.success(f"✅ {len(df)} Buyers Found")

        # --------------------------------------------------
        # Executive Dashboard
        # --------------------------------------------------

        st.subheader("📊 Executive Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Buyers",
            len(df),
        )

        col2.metric(
            "Avg Confidence",
            f"{average_confidence(df)}%",
        )

        col3.metric(
            "Buyer Potential",
            f"{average_potential(df)}/5",
        )

        col4.metric(
            "Market Fit",
            f"{average_market_fit(df)}/5",
        )

        st.markdown("---")

        # --------------------------------------------------
        # Buyer Intelligence
        # --------------------------------------------------

        st.subheader("🏢 Buyer Intelligence")

        for buyer in result:

            with st.expander(
                f"🏢 {buyer['company_name']} ({buyer['country']})"
            ):

                left_col, right_col = st.columns(2)

                with left_col:

                    st.write(f"**🌐 Website:** {buyer['website']}")
                    st.write(f"**🏢 Buyer Type:** {buyer['buyer_type']}")
                    st.write(f"**📦 Products:** {buyer['products']}")
                    st.write(f"**📈 Confidence:** {buyer['confidence']}%")
                    st.write(
                        f"**⭐ Buyer Potential:** {'⭐' * buyer['buyer_potential']}"
                    )
                    st.write(
                        f"**🎯 Market Fit:** {'⭐' * buyer['market_fit']}"
                    )

                with right_col:

                    st.write(f"**🏭 Business Size:** {buyer['business_size']}")
                    st.write(f"**⚠️ Risk Level:** {buyer['risk_level']}")
                    st.write(
                        f"**👤 Suggested Contact:** {buyer['suggested_contact']}"
                    )

                    st.write("**📬 Recommended Approach**")

                    st.info(
                        buyer["recommended_approach"]
                    )

                st.markdown("### 🤖 AI Summary")

                st.success(
                    buyer["ai_summary"]
                )

                st.markdown("### 💡 Why this Buyer?")

                st.write(
                    buyer["reason"]
                )

        st.markdown("---")

        # --------------------------------------------------
        # Buyer Data
        # --------------------------------------------------

        st.subheader("📄 Buyer Data")

        # Hide the default DataFrame index because we have our own S.No. column
        st.dataframe(
            df,
            hide_index=True,
            width="stretch",
        )

        csv = dataframe_to_csv(df)
        excel = dataframe_to_excel(df)

        download1, download2 = st.columns(2)

        with download1:
            st.download_button(
                label="📄 Download CSV",
                data=csv,
                file_name="buyers.csv",
                mime="text/csv",
                width="stretch",
            )

        with download2:
            st.download_button(
                label="📊 Download Excel",
                data=excel,
                file_name="buyers.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width="stretch",
            )

        # --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Developed by MKS | EPCH AI Trade Intelligence Platform | Version 2.0"
)