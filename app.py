"""
Export Promotion Council of India : AI Trade Intelligence Platform
Main Streamlit App
"""

import streamlit as st

from buyer_engine import discover_buyers
from config import (
    APP_NAME,
    APP_ICON,
    PAGE_LAYOUT,
    CATEGORIES,
    QUICK_COUNTRIES,
    FAIR_INFO,
    DEFAULT_BUYERS,
    MAX_BUYERS
)

from utils import (
    average_confidence,
    buyers_dataframe,
    dataframe_to_csv,
    dataframe_to_excel,
    search_buyers
)

# --------------------------------------------------------
# Page Configuration
# --------------------------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT
)

# --------------------------------------------------------
# Header
# --------------------------------------------------------

st.title("🌍 EPCH AI Trade Intelligence Platform")
st.caption("AI Powered International Buyer Discovery")

st.divider()

# --------------------------------------------------------
# Sidebar
# --------------------------------------------------------

st.sidebar.header("Buyer Search")

country = st.sidebar.selectbox(
    "Target Country",
    QUICK_COUNTRIES
)

category = st.sidebar.selectbox(
    "Product Category",
    CATEGORIES
)

keywords = st.sidebar.text_input(
    "Keywords",
    placeholder="eco-friendly handmade products"
)

buyers = st.sidebar.slider(
    "Number of Buyers",
    min_value=5,
    max_value=MAX_BUYERS,
    value=DEFAULT_BUYERS
)

search_button = st.sidebar.button(
    "🚀 Discover Buyers",
    use_container_width=True
)

# --------------------------------------------------------
# Fair Information
# --------------------------------------------------------

with st.expander("IHGF Fair Information"):

    st.write(f"**Fair:** {FAIR_INFO['name']}")
    st.write(f"**Organizer:** {FAIR_INFO['organizer']}")
    st.write(f"**Venue:** {FAIR_INFO['venue']}")
    st.write(f"**Website:** {FAIR_INFO['website']}")

# --------------------------------------------------------
# Run AI
# --------------------------------------------------------

if search_button:

    with st.spinner("Searching buyers using Gemini AI..."):

        result = discover_buyers(
            country,
            category,
            keywords,
            buyers
        )

    if isinstance(result, dict):

        st.error(result.get("error", "Unknown error"))

        if "raw_response" in result:

            with st.expander("Raw Response"):

                st.code(result["raw_response"])

    else:

        st.session_state["buyers"] = result

# --------------------------------------------------------
# Results
# --------------------------------------------------------

if "buyers" in st.session_state:

    buyers_list = st.session_state["buyers"]

    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Buyers Found",
        len(buyers_list)
    )

    col2.metric(
        "Average Confidence",
        f"{average_confidence(buyers_list)}%"
    )

    col3.metric(
        "Country",
        country
    )

    st.divider()

    search = st.text_input(
        "🔍 Search Buyers"
    )

    filtered = search_buyers(
        buyers_list,
        search
    )

    st.write(f"Showing **{len(filtered)}** buyers")

    st.divider()

    for buyer in filtered:

        with st.container(border=True):

            st.subheader(
                buyer["company_name"]
            )

            st.write(
                f"🌍 **Country:** {buyer['country']}"
            )

            st.write(
                f"🏢 **Buyer Type:** {buyer['buyer_type']}"
            )

            st.write(
                f"📦 **Products:** {buyer['products']}"
            )

            st.write(
                f"💡 {buyer['reason']}"
            )

            st.link_button(
                "🌐 Visit Website",
                buyer["website"]
            )

            st.progress(
                buyer["confidence"] / 100
            )

            st.caption(
                f"Confidence Score: {buyer['confidence']}%"
            )

    st.divider()

    df = buyers_dataframe(filtered)

    col_csv, col_excel = st.columns(2)

    with col_csv:

        st.download_button(
            "📥 Download CSV",
            dataframe_to_csv(df),
            file_name="buyers.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_excel:

        st.download_button(
            "📥 Download Excel",
            dataframe_to_excel(df),
            file_name="buyers.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )