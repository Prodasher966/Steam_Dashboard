import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.feature_engineering import explode_genres
from utils.metrics import generate_genre_summary

st.set_page_config(layout="wide")

# =========================
# Page Header
# =========================
st.title("Genre Intelligence")
st.caption(
    "Comparative analysis of supply, demand, and engagement efficiency across game genres."
)

# =========================
# Load Data
# =========================
df = load_data()

df = df.dropna(subset=["genres", "recommendations"])
df = df[df["recommendations"] > 0]

# =========================
# Feature Engineering
# =========================
df_genres = explode_genres(df)

# =========================
# Genre Metrics
# =========================
genre_stats = (
    df_genres.groupby("genres")
    .agg(
        game_count=("appid", "count"),
        total_recommendations=("recommendations", "sum"),
        avg_recommendations=("recommendations", "mean"),
    )
    .reset_index()
)

# =========================
# ROW 1 — Metric Toggle
# =========================
st.subheader("Genre Performance Overview")

metric = st.radio(
    "Select metric",
    ["game_count", "total_recommendations", "avg_recommendations"],
    horizontal=True,
)

metric_labels = {
    "game_count": "Number of Games",
    "total_recommendations": "Total Recommendations",
    "avg_recommendations": "Avg Recommendations per Game",
}

fig_bar = px.bar(
    genre_stats.sort_values(metric),
    x=metric,
    y="genres",
    orientation="h",
    labels={metric: metric_labels[metric], "genres": "Genre"},
)

st.plotly_chart(fig_bar, use_container_width=True)

# =========================
# ROW 2 — Supply vs Demand
# =========================
st.subheader("Supply vs Demand Imbalance")

fig_scatter = px.scatter(
    genre_stats,
    x="game_count",
    y="avg_recommendations",
    size="total_recommendations",
    color="genres",
    labels={
        "game_count": "Number of Games",
        "avg_recommendations": "Avg Recommendations",
    },
)

st.plotly_chart(fig_scatter, use_container_width=True)

# =========================
# ROW 3 — Genre Trends Over Time
# =========================
st.subheader("Genre Engagement Trends")

top_genres = (
    genre_stats.sort_values("total_recommendations", ascending=False)
    .head(6)["genres"]
)

genre_yearly = (
    df_genres[df_genres["genres"].isin(top_genres)]
    .groupby(["release_year", "genres"])["recommendations"]
    .sum()
    .reset_index()
)

fig_trend = px.area(
    genre_yearly,
    x="release_year",
    y="recommendations",
    color="genres",
    labels={
        "release_year": "Release Year",
        "recommendations": "Total Recommendations",
    },
)

st.plotly_chart(fig_trend, use_container_width=True)

# =========================
# ROW 4 — Auto Summary
# =========================
st.subheader("Key Takeaways")

summary = generate_genre_summary(genre_stats)
st.info(summary)
