import streamlit as st
import pandas as pd
import plotly.express as px

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

st.markdown(
    "Interactive analysis of transaction volume, revenue, "
    "store performance and hourly demand."
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("data/Coffee_Feature_Engineered.csv")

# Convert time
df["transaction_time"] = pd.to_datetime(
    df["transaction_time"]
)

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