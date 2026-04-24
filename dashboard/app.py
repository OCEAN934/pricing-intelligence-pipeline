import streamlit as st
import requests
import pandas as pd
import time

# 🔗 API URL
BASE_URL = "https://pricing-intelligence-pipeline.onrender.com"

st.set_page_config(
    page_title="Pricing Intelligence Dashboard",
    layout="wide"
)

# ---------------------------
# HEADER
# ---------------------------
st.title("📊 Pricing Intelligence Dashboard")
st.markdown("Real-time insights powered by your data pipeline 🚀")

# ---------------------------
# SAFE API CALL WITH RETRY
# ---------------------------
def safe_request(url, retries=3):
    for i in range(retries):
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            return response.json()
        except Exception:
            time.sleep(5)
    return None

# ---------------------------
# FETCH DATA
# ---------------------------
@st.cache_data
def fetch_books():
    data = safe_request(f"{BASE_URL}/books")
    if data:
        return pd.DataFrame(data["data"])
    return pd.DataFrame()

@st.cache_data
def fetch_avg_price():
    data = safe_request(f"{BASE_URL}/insights/avg-price")
    return data["average_price"] if data else 0

@st.cache_data
def fetch_category_summary():
    data = safe_request(f"{BASE_URL}/insights/category-summary")
    return data if data else {}

# ---------------------------
# LOAD DATA WITH SPINNER
# ---------------------------
with st.spinner("🚀 Fetching data from API (may take 30–60 sec on first load)..."):
    df = fetch_books()

# ---------------------------
# HANDLE EMPTY DATA
# ---------------------------
if df.empty:
    st.warning("⚠️ API is waking up (Render free tier). Please wait and refresh.")
    st.stop()

# ---------------------------
# SIDEBAR CONTROLS
# ---------------------------
st.sidebar.header("🔍 Controls")

min_price, max_price = st.sidebar.slider(
    "Price Range",
    float(df["price"].min()),
    float(df["price"].max()),
    (float(df["price"].min()), float(df["price"].max()))
)

order = st.sidebar.selectbox("Sort Order", ["asc", "desc"])

# ---------------------------
# FILTER + SORT
# ---------------------------
filtered_df = df[
    (df["price"] >= min_price) &
    (df["price"] <= max_price)
]

filtered_df = filtered_df.sort_values(
    "price",
    ascending=(order == "asc")
)

# ---------------------------
# METRICS
# ---------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

avg_price = fetch_avg_price()
total_books = len(filtered_df)
max_price_val = filtered_df["price"].max()

col1.metric("Average Price (API)", f"£{avg_price:.2f}")
col2.metric("Books in Range", total_books)
col3.metric("Max Price", f"£{max_price_val:.2f}")

# ---------------------------
# DATA TABLE
# ---------------------------
st.subheader("📚 Book Listings")
st.dataframe(filtered_df, use_container_width=True)

# ---------------------------
# CHARTS
# ---------------------------
st.subheader("📊 Insights")

col1, col2 = st.columns(2)

# Category distribution
category_summary = fetch_category_summary()
category_df = pd.DataFrame(
    list(category_summary.items()),
    columns=["Category", "Count"]
)

col1.markdown("### Price Segmentation")
if not category_df.empty:
    col1.bar_chart(category_df.set_index("Category"))

# Price trend
col2.markdown("### Price Distribution")
col2.line_chart(filtered_df["price"])

# ---------------------------
# SORTED API DEMO
# ---------------------------
st.subheader("⚡ Top Results (Sorted via API)")

sorted_data = safe_request(f"{BASE_URL}/books/sorted?order={order}")

if sorted_data:
    sorted_df = pd.DataFrame(sorted_data["data"])
    st.dataframe(sorted_df.head(10), use_container_width=True)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown(
    "✅ Built with Streamlit | ⚡ Powered by FastAPI backend | 🌍 Live Data Pipeline"
)