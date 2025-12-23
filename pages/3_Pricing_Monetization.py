import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.feature_engineering import add_price_buckets
from utils.metrics import generate_pricing_summary

st.set_page_config(layout="wide")

# =========================
# Page Header
# =========================
st.title("Pricing & Monetization")
st.caption(
    "Analysis of pricing strategies, monetization tiers, and their impact on player engagement."
)

# =========================
# Load Data
# =========================
df = load_data()

df = df.dropna(subset=["price", "recommendations"])

# =========================
# Feature Engineering
# =========================
df = add_price_buckets(df)

# =========================
# Pricing Metrics
# =========================
pricing_stats = (
    df.groupby("price_bucket")
    .agg(
        game_count=("appid", "count"),
        total_recommendations=("recommendations", "sum"),
        avg_recommendations=("recommendations", "mean"),
        median_recommendations=("recommendations", "median"),
    )
    .reset_index()
)

# =========================
# ROW 1 — Price Distribution
# =========================
st.subheader("Game Distribution by Price Tier")

fig_dist = px.bar(
    pricing_stats,
    x="price_bucket",
    y="game_count",
    labels={
        "price_bucket": "Price Tier",
        "game_count": "Number of Games",
    },
)

st.plotly_chart(fig_dist, use_container_width=True)

# =========================
# ROW 2 — Engagement by Price
# =========================
st.subheader("Engagement by Price Tier")

fig_engage = px.bar(
    pricing_stats,
    x="price_bucket",
    y="avg_recommendations",
    labels={
        "price_bucket": "Price Tier",
        "avg_recommendations": "Avg Recommendations",
    },
)

st.plotly_chart(fig_engage, use_container_width=True)

# =========================
# ROW 3 — Median Signal
# =========================
st.subheader("Median Engagement (Outlier-Controlled)")

fig_median = px.line(
    pricing_stats,
    x="price_bucket",
    y="median_recommendations",
    markers=True,
    labels={
        "price_bucket": "Price Tier",
        "median_recommendations": "Median Recommendations",
    },
)

st.plotly_chart(fig_median, use_container_width=True)

