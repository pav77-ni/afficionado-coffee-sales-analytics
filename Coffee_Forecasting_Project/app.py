import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path 

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Afficionado Coffee Roasters",
    page_icon="☕",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("☕ Afficionado Coffee Roasters")
st.subheader("Sales & Demand Analytics Dashboard")


st.markdown("""
### 📌 Project Overview

This dashboard analyzes transaction data from Afficionado Coffee Roasters
to identify sales patterns, store performance, product performance and
hourly demand peaks.

The analysis supports data-driven decisions related to inventory planning,
staff scheduling and demand management.
""")
# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

#df = pd.read_csv("data/Coffee_Feature_Engineered.csv")
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "data" / "Coffee_Feature_Engineered.csv")

# Convert time
df["transaction_time"] = pd.to_datetime(
    df["transaction_time"]
)
df["hour"] = df["transaction_time"].dt.hour

df["Revenue"] = df["transaction_qty"] * df["unit_price"]
# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

# Store filter
stores = ["All Stores"] + sorted(
    df["store_location"].unique().tolist()
)

selected_store = st.sidebar.selectbox(
    "Select Store",
    stores
)

# Category filter
categories = ["All Categories"] + sorted(
    df["product_category"].unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Select Product Category",
    categories
)

# Metric selector
metric = st.sidebar.radio(
    "Select Metric",
    ["Revenue", "Quantity"]
)

# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

filtered_df = df.copy()

if selected_store != "All Stores":
    filtered_df = filtered_df[
        filtered_df["store_location"] == selected_store
    ]

if selected_category != "All Categories":
    filtered_df = filtered_df[
        filtered_df["product_category"] == selected_category
    ]

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_revenue = filtered_df["Revenue"].sum()

total_transactions = filtered_df["transaction_id"].nunique()

total_quantity = filtered_df["transaction_qty"].sum()

average_transaction = (
    total_revenue / total_transactions
    if total_transactions > 0
    else 0
)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"${total_revenue:,.2f}"
)

col2.metric(
    "Transactions",
    f"{total_transactions:,}"
)

col3.metric(
    "Quantity Sold",
    f"{total_quantity:,}"
)

col4.metric(
    "Avg Transaction Value",
    f"${average_transaction:,.2f}"
)

st.divider()

# --------------------------------------------------
# HOURLY DEMAND
# --------------------------------------------------

st.header("⏰ Hourly Demand Analysis")

if metric == "Revenue":

    hourly_data = (
        filtered_df
        .groupby("Hour")["Revenue"]
        .sum()
        .reset_index()
    )

    y_column = "Revenue"

else:

    hourly_data = (
        filtered_df
        .groupby("Hour")["transaction_qty"]
        .sum()
        .reset_index()
    )

    y_column = "transaction_qty"


fig_hour = px.line(
    hourly_data,
    x="Hour",
    y=y_column,
    markers=True,
    title=f"{metric} by Hour"
)

fig_hour.update_layout(
    xaxis_title="Hour of Day",
    yaxis_title=metric
)

st.plotly_chart(
    fig_hour,
    use_container_width=True
)

# --------------------------------------------------
# STORE PERFORMANCE
# --------------------------------------------------

st.header("🏪 Store Performance")

store_data = (
    filtered_df
    .groupby("store_location")
    .agg(
        Revenue=("Revenue", "sum"),
        Quantity=("transaction_qty", "sum"),
        Transactions=("transaction_id", "nunique")
    )
    .reset_index()
)

fig_store = px.bar(
    store_data,
    x="store_location",
    y="Revenue",
    title="Revenue by Store",
    text_auto=".2s"
)

st.plotly_chart(
    fig_store,
    use_container_width=True
)

# --------------------------------------------------
# CATEGORY PERFORMANCE
# --------------------------------------------------

st.header("☕ Product Category Performance")

category_data = (
    filtered_df
    .groupby("product_category")["Revenue"]
    .sum()
    .reset_index()
    .sort_values(
        "Revenue",
        ascending=False
    )
)

fig_category = px.bar(
    category_data,
    x="product_category",
    y="Revenue",
    title="Revenue by Product Category",
    text_auto=".2s"
)

st.plotly_chart(
    fig_category,
    use_container_width=True
)

# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------

st.header("🏆 Top 10 Products")

top_products = (
    filtered_df
    .groupby("product_type")["Revenue"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x="Revenue",
    y="product_type",
    orientation="h",
    title="Top 10 Products by Revenue",
    text_auto=".2s"
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)

# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------

st.header("📋 Transaction Data")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True
)

#total_revenue = df["Revenue"].sum()
#total_transactions = df["transaction_id"].nunique()
#total_quantity = df["transaction_qty"].sum()
#avg_transaction = total_revenue / total_transactions


# ==========================================================
# FILTERS
# ==========================================================

st.sidebar.header("🔎 Dashboard Filters")

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("🔎 Dashboard Filters")

store_filter = st.sidebar.multiselect(
    "🏪 Select Store",
    options=sorted(df["store_location"].unique()),
    default=sorted(df["store_location"].unique())
)

category_filter = st.sidebar.multiselect(
    "☕ Select Product Category",
    options=sorted(df["product_category"].unique()),
    default=sorted(df["product_category"].unique())
)

hour_filter = st.sidebar.slider(
    "🕐 Select Hour Range",
    min_value=int(df["hour"].min()),
    max_value=int(df["hour"].max()),
    value=(
        int(df["hour"].min()),
        int(df["hour"].max())
    )
)

filtered_df = df[
    (df["store_location"].isin(store_filter)) &
    (df["product_category"].isin(category_filter)) &
    (df["hour"].between(hour_filter[0], hour_filter[1]))
]
metric_choice = st.sidebar.radio(
    "📊 Select Metric",
    ["Revenue", "Quantity"]
)
# ==========================================================
# SELECTED METRIC ANALYSIS
# ==========================================================

st.header("📊 Selected Metric by Store")

if metric_choice == "Revenue":

    metric_data = (
        filtered_df
        .groupby("store_location")["Revenue"]
        .sum()
        .reset_index()
    )

    y_column = "Revenue"
    y_title = "Total Revenue"

else:

    metric_data = (
        filtered_df
        .groupby("store_location")["transaction_qty"]
        .sum()
        .reset_index()
    )

    y_column = "transaction_qty"
    y_title = "Total Quantity Sold"


fig_metric = px.bar(
    metric_data,
    x="store_location",
    y=y_column,
    title=f"{metric_choice} by Store",
    labels={
        "store_location": "Store Location",
        y_column: y_title
    },
    text_auto=".2s"
)

st.plotly_chart(fig_metric, width="stretch")
# ==========================================================
# DYNAMIC KPI CALCULATIONS
# ==========================================================

total_revenue = filtered_df["Revenue"].sum()

total_transactions = filtered_df["transaction_id"].nunique()

total_quantity = filtered_df["transaction_qty"].sum()

if total_transactions > 0:
    avg_transaction = total_revenue / total_transactions
else:
    avg_transaction = 0

best_store = (
    filtered_df.groupby("store_location")["Revenue"]
    .sum()
    .idxmax()
    if not filtered_df.empty
    else "N/A"
)

peak_hour = (
    filtered_df.groupby("hour")["Revenue"]
    .sum()
    .idxmax()
    if not filtered_df.empty
    else "N/A"
)
best_store = (
    df.groupby("store_location")["Revenue"]
    .sum()
    .idxmax()
)

peak_hour = (
    df.groupby("hour")["Revenue"]
    .sum()
    .idxmax()
)

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
col2.metric("🧾 Transactions", f"{total_transactions:,}")
col3.metric("☕ Quantity Sold", f"{total_quantity:,}")
col4.metric("📊 Avg Transaction", f"${avg_transaction:.2f}")
col5.metric("🏆 Best Store", best_store)
col6.metric("⏰ Peak Hour", f"{peak_hour}:00")

# ==========================================================
# REVENUE BY STORE
# ==========================================================

st.header("🏪 Revenue by Store")

store_revenue = (
    filtered_df
    .groupby("store_location")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

fig_store = px.bar(
    store_revenue,
    x="store_location",
    y="Revenue",
    title="Revenue by Store",
    labels={
        "store_location": "Store Location",
        "Revenue": "Total Revenue"
    },
    text_auto=".2s"
)

st.plotly_chart(fig_store, width="stretch")
# ==========================================================
# REVENUE BY PRODUCT CATEGORY
# ==========================================================

st.header("☕ Revenue by Product Category")

category_revenue = (
    filtered_df
    .groupby("product_category")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

fig_category = px.bar(
    category_revenue,
    x="product_category",
    y="Revenue",
    title="Revenue by Product Category",
    labels={
        "product_category": "Product Category",
        "Revenue": "Total Revenue"
    },
    text_auto=".2s"
)

st.plotly_chart(fig_category, width="stretch", key="store_chart")

# ==========================================================
# TOP 10 PRODUCTS
# ==========================================================

st.header("🏆 Top 10 Products by Revenue")

product_revenue = (
    filtered_df
    .groupby("product_detail")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
    .head(10)
)

fig_products = px.bar(
    product_revenue.sort_values("Revenue"),
    x="Revenue",
    y="product_detail",
    orientation="h",
    title="Top 10 Products by Revenue",
    labels={
        "product_detail": "Product",
        "Revenue": "Total Revenue"
    },
    text_auto=".2s"
)

st.plotly_chart(fig_products, width="stretch", key="store_chart")

# ==========================================================
# HOURLY REVENUE
# ==========================================================

st.header("🕐 Revenue by Hour")

hourly_revenue = (
    filtered_df
    .groupby("hour")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("hour")
)

fig_hour = px.line(
    hourly_revenue,
    x="hour",
    y="Revenue",
    markers=True,
    title="Hourly Revenue",
    labels={
        "hour": "Hour of Day",
        "Revenue": "Total Revenue"
    }
)

st.plotly_chart(fig_hour, width="stretch", key="store_chart")

# ==========================================================
# HOURLY DEMAND
# ==========================================================

st.header("📈 Hourly Demand")

hourly_demand = (
    filtered_df
    .groupby("hour")["transaction_qty"]
    .sum()
    .reset_index()
    .sort_values("hour")
)

fig_demand = px.bar(
    hourly_demand,
    x="hour",
    y="transaction_qty",
    title="Transaction Quantity by Hour",
    labels={
        "hour": "Hour of Day",
        "transaction_qty": "Total Quantity Sold"
    },
    text_auto=True
)

st.plotly_chart(fig_demand, width="stretch", key="store_chart")
# ==========================================================
# DOWNLOAD FILTERED DATA
# ==========================================================

st.header("⬇️ Download Data")

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv_data,
    file_name="afficionado_filtered_data.csv",
    mime="text/csv"
)
st.info(
    "ℹ️ Forecasting Note: The supplied dataset contains transaction year "
    "and time but does not include the transaction date. Therefore, "
    "calendar-based daily forecasting and weekly lag features cannot "
    "be reliably generated without additional date information."
)
