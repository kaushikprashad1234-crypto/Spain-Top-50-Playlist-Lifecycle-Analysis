# app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Afficionado Coffee Roasters Dashboard",
    page_icon="☕",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>
.main {
    background-color: #f5f5f5;
}

h1, h2, h3 {
    color: #2c3e50;
}

.stMetric {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 0px 5px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("☕ Afficionado Coffee Roasters")
st.subheader(
    "Product Optimization & Revenue Contribution Dashboard"
)

st.markdown("---")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("E:\\power bi\\Transactions\\raw\\Afficionado Coffee Roasters.xlsx - Transactions.csv")

    # Revenue Calculation
    df["revenue"] = (
        df["transaction_qty"] * df["unit_price"]
    )

    return df

df = load_data()

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("📌 Dashboard Filters")

# Store Filter
selected_store = st.sidebar.multiselect(
    "Select Store Location",
    options=df["store_location"].unique(),
    default=df["store_location"].unique()
)

# Product Category Filter
selected_category = st.sidebar.multiselect(
    "Select Product Category",
    options=df["product_category"].unique(),
    default=df["product_category"].unique()
)

# Product Type Filter
selected_type = st.sidebar.multiselect(
    "Select Product Type",
    options=df["product_type"].unique(),
    default=df["product_type"].unique()
)

# Top N Slider
top_n = st.sidebar.slider(
    "Select Top Products",
    min_value=5,
    max_value=20,
    value=10
)

# ---------------------------------------------------
# FILTER DATAFRAME
# ---------------------------------------------------

filtered_df = df[
    (df["store_location"].isin(selected_store)) &
    (df["product_category"].isin(selected_category)) &
    (df["product_type"].isin(selected_type))
]

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------

total_revenue = filtered_df["revenue"].sum()

total_orders = (
    filtered_df["transaction_id"].nunique()
)

total_units = (
    filtered_df["transaction_qty"].sum()
)

avg_order_value = (
    total_revenue / total_orders
    if total_orders > 0 else 0
)

top_product = (
    filtered_df.groupby("product_detail")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "💰 Total Revenue",
    f"${total_revenue:,.2f}"
)

col2.metric(
    "🧾 Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "📦 Units Sold",
    f"{total_units:,}"
)

col4.metric(
    "🛒 Avg Order Value",
    f"${avg_order_value:,.2f}"
)

col5.metric(
    "🏆 Top Product",
    top_product
)

st.markdown("---")

# ---------------------------------------------------
# REVENUE BY CATEGORY
# ---------------------------------------------------

st.subheader("📊 Revenue Distribution by Category")

category_revenue = (
    filtered_df.groupby("product_category")["revenue"]
    .sum()
    .reset_index()
)

fig_category = px.pie(
    category_revenue,
    names="product_category",
    values="revenue",
    hole=0.45,
    title="Revenue Share by Category"
)

st.plotly_chart(
    fig_category,
    use_container_width=True
)

# ---------------------------------------------------
# TOP REVENUE PRODUCTS
# ---------------------------------------------------

st.subheader("🏆 Top Revenue Products")

top_products = (
    filtered_df.groupby("product_detail")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
    .reset_index()
)

fig_top_products = px.bar(
    top_products,
    x="product_detail",
    y="revenue",
    text_auto=True,
    title="Top Revenue Generating Products"
)

st.plotly_chart(
    fig_top_products,
    use_container_width=True
)

# ---------------------------------------------------
# PRODUCT POPULARITY ANALYSIS
# ---------------------------------------------------

st.subheader("🔥 Product Popularity Analysis")

popular_products = (
    filtered_df.groupby("product_detail")
    ["transaction_qty"]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
    .reset_index()
)

fig_popular = px.bar(
    popular_products,
    x="product_detail",
    y="transaction_qty",
    text_auto=True,
    title="Top Selling Products"
)

st.plotly_chart(
    fig_popular,
    use_container_width=True
)

# ---------------------------------------------------
# POPULARITY VS REVENUE
# ---------------------------------------------------

st.subheader("📌 Popularity vs Revenue Analysis")

scatter_df = (
    filtered_df.groupby("product_detail")
    .agg({
        "transaction_qty": "sum",
        "revenue": "sum"
    })
    .reset_index()
)

fig_scatter = px.scatter(
    scatter_df,
    x="transaction_qty",
    y="revenue",
    size="revenue",
    hover_name="product_detail",
    title="Popularity vs Revenue"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# ---------------------------------------------------
# PARETO ANALYSIS
# ---------------------------------------------------

st.subheader("📈 Pareto Revenue Analysis")

pareto_df = (
    filtered_df.groupby("product_detail")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

pareto_df["cumulative_revenue"] = (
    pareto_df["revenue"].cumsum()
)

pareto_df["cumulative_pct"] = (
    pareto_df["cumulative_revenue"]
    / pareto_df["revenue"].sum()
) * 100

fig_pareto = go.Figure()

# Revenue Bars
fig_pareto.add_trace(
    go.Bar(
        x=pareto_df["product_detail"],
        y=pareto_df["revenue"],
        name="Revenue"
    )
)

# Cumulative Line
fig_pareto.add_trace(
    go.Scatter(
        x=pareto_df["product_detail"],
        y=pareto_df["cumulative_pct"],
        mode="lines+markers",
        name="Cumulative %",
        yaxis="y2"
    )
)

fig_pareto.update_layout(
    title="Pareto Analysis",
    yaxis=dict(title="Revenue"),
    yaxis2=dict(
        title="Cumulative %",
        overlaying="y",
        side="right"
    ),
    xaxis=dict(title="Products")
)

st.plotly_chart(
    fig_pareto,
    use_container_width=True
)

# ---------------------------------------------------
# STORE PERFORMANCE
# ---------------------------------------------------

st.subheader("🏪 Store-Level Revenue")

store_revenue = (
    filtered_df.groupby("store_location")["revenue"]
    .sum()
    .reset_index()
)

fig_store = px.bar(
    store_revenue,
    x="store_location",
    y="revenue",
    text_auto=True,
    title="Revenue by Store"
)

st.plotly_chart(
    fig_store,
    use_container_width=True
)

# ---------------------------------------------------
# PRODUCT PERFORMANCE TABLE
# ---------------------------------------------------

st.subheader("📋 Product Performance Table")

product_table = (
    filtered_df.groupby([
        "product_category",
        "product_type",
        "product_detail"
    ])
    .agg({
        "transaction_qty": "sum",
        "revenue": "sum",
        "unit_price": "mean"
    })
    .reset_index()
)

product_table.columns = [
    "Category",
    "Product Type",
    "Product",
    "Units Sold",
    "Revenue",
    "Average Price"
]

st.dataframe(
    product_table,
    use_container_width=True
)

# ---------------------------------------------------
# DOWNLOAD REPORT
# ---------------------------------------------------

st.subheader("⬇️ Download Product Performance Report")

csv = (
    product_table.to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="product_performance_report.csv",
    mime="text/csv"
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.markdown(
    """
    ### 📌 Dashboard Summary

    This dashboard provides:
    - Product revenue analytics
    - Product popularity insights
    - Pareto revenue concentration analysis
    - Store-level performance monitoring
    - KPI-based operational intelligence

    Developed for Afficionado Coffee Roasters.
    """
<<<<<<< HEAD
)
=======
)
>>>>>>> 19460643192bad5f3c0b282c9d60cc4807fb6025
