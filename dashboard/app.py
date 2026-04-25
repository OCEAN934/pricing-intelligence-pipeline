import streamlit as st
import requests
import pandas as pd
import time

# =========================================
# CONFIG
# =========================================

BASE_URL = "https://pricing-intelligence-pipeline.onrender.com"

st.set_page_config(
    page_title="Pricing Intelligence Dashboard",
    layout="wide",
)

# -----------------------------------------
# OPTIONAL LIGHT STYLING
# -----------------------------------------
st.markdown("""
<style>
div[data-testid="metric-container"]{
    border:1px solid #e6e6e6;
    padding:15px;
    border-radius:12px;
}
</style>
""", unsafe_allow_html=True)


# =========================================
# HEADER
# =========================================

st.title("📊 Pricing Intelligence Dashboard")
st.markdown(
"""
Interactive pricing analytics powered by a live **Data Engineering Pipeline + FastAPI + Streamlit**.
"""
)

st.markdown("---")


# =========================================
# SAFE REQUEST WITH RETRIES
# =========================================

def safe_request(url, retries=4, wait=8):
    for _ in range(retries):
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            return response.json()
        except Exception:
            time.sleep(wait)
    return None


# =========================================
# DATA FETCHERS
# =========================================

@st.cache_data(ttl=300)
def fetch_books():
    data = safe_request(f"{BASE_URL}/books")
    if data:
        return pd.DataFrame(data["data"])
    return pd.DataFrame()


@st.cache_data(ttl=300)
def fetch_avg_price():
    data = safe_request(f"{BASE_URL}/insights/avg-price")
    return data["average_price"] if data else 0


@st.cache_data(ttl=300)
def fetch_category_summary():
    data = safe_request(f"{BASE_URL}/insights/category-summary")
    return data if data else {}


# =========================================
# LOAD DATA
# =========================================

with st.spinner("🚀 Connecting to backend and loading pricing data..."):
    df = fetch_books()


# =========================================
# AUTO WAKE IF API SLEEPS
# =========================================

if df.empty:
    st.warning("Backend is waking up... retrying automatically")

    for _ in range(3):
        time.sleep(10)
        st.cache_data.clear()
        df = fetch_books()

        if not df.empty:
            break

    if df.empty:
        st.error(
            "Backend still sleeping (free-tier cold start). "
            "Refresh once in a few seconds."
        )
        st.stop()


# =========================================
# SIDEBAR CONTROLS
# =========================================

st.sidebar.header("🔍 Dashboard Controls")

min_price, max_price = st.sidebar.slider(
    "Price Range (£)",
    float(df.price.min()),
    float(df.price.max()),
    (
        float(df.price.min()),
        float(df.price.max())
    )
)

order = st.sidebar.selectbox(
    "Sort Order",
    ["asc", "desc"]
)

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()


# =========================================
# FILTER / SORT
# =========================================

filtered_df = df[
    (df["price"] >= min_price) &
    (df["price"] <= max_price)
].copy()

filtered_df = filtered_df.sort_values(
    "price",
    ascending=(order=="asc")
)


# =========================================
# KPI SECTION
# =========================================

st.subheader("📌 Key Metrics")

c1, c2, c3, c4 = st.columns(4)

avg_price = fetch_avg_price()
total_books = len(filtered_df)
highest = filtered_df["price"].max()
lowest = filtered_df["price"].min()

c1.metric("Average Price", f"£{avg_price:.2f}")
c2.metric("Books in Range", total_books)
c3.metric("Highest Price", f"£{highest:.2f}")
c4.metric("Lowest Price", f"£{lowest:.2f}")


# =========================================
# BOOK LISTING
# =========================================

st.markdown("---")
st.subheader("📚 Book Listings")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# =========================================
# INSIGHTS
# =========================================

st.markdown("---")
st.subheader("📈 Pricing Insights")

left, right = st.columns(2)

# Category segmentation (from API)
category_summary = fetch_category_summary()

category_df = pd.DataFrame(
    list(category_summary.items()),
    columns=["Category","Count"]
)

with left:
    st.markdown("### Price Segmentation")
    if not category_df.empty:
        st.bar_chart(
            category_df.set_index("Category")
        )

with right:
    st.markdown("### Price Distribution")
    st.line_chart(filtered_df["price"])


# =========================================
# SORTED API FEATURE
# =========================================

st.markdown("---")
st.subheader("⚡ Top 10 Cheapest / Premium Books")

sorted_data = safe_request(
    f"{BASE_URL}/books/sorted?order={order}"
)

if sorted_data:
    sorted_df = pd.DataFrame(
        sorted_data["data"]
    )

    st.dataframe(
        sorted_df.head(10),
        use_container_width=True,
        hide_index=True
    )


# =========================================
# EXTRA SUMMARY
# =========================================

st.markdown("---")

st.subheader("🧠 Dataset Summary")

st.write(
f"""
- Total records available: **{len(df)}**
- Current filtered records: **{len(filtered_df)}**
- Active sorting mode: **{order.upper()}**
- Data source: **Live FastAPI backend**
"""
)


# =========================================
# FOOTER
# =========================================

st.markdown("---")
st.caption(
"Built with Streamlit • Powered by FastAPI • End-to-End Pricing Intelligence Pipeline"
)