import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.feature_engineering import yearly_metrics, explode_genres
from utils.metrics import generate_market_trends_summary

st.set_page_config(layout="wide")

# =========================
# Page Header
# =========================
st.title("Market Trends")
st.caption(
    "Temporal analysis of game releases, player engagement, and structural shifts in the Steam market."
)

# =========================
# Load Data
# =========================
df = load_data()
df = df.dropna(subset=["release_year", "recommendations"])

# =========================
# Feature Engineering
# =========================
yearly_stats = yearly_metrics(df)

# =========================
# ROW 1 — Market Growth
# =========================
st.subheader("Game Releases Over Time")

fig_games = px.line(
    yearly_stats,
    x="release_year",
    y="game_count",
    markers=True,
    labels={
        "release_year": "Release Year",
        "game_count": "Number of Games",
    },
)

st.plotly_chart(fig_games, use_container_width=True)

# =========================
# ROW 2 — Engagement Growth
# =========================
st.subheader("Engagement Growth vs Market Size")

fig_engagement = px.line(
    yearly_stats,
    x="release_year",
    y=["total_recommendations", "avg_recommendations"],
    labels={
        "value": "Recommendations",
        "release_year": "Release Year",
        "variable": "Metric",
    },
)

st.plotly_chart(fig_engagement, use_container_width=True)

# =========================
# ROW 3 — Saturation Signal
# =========================
st.subheader("Median Engagement Trend")

fig_median = px.line(
    yearly_stats,
    x="release_year",
    y="median_recommendations",
    markers=True,
    labels={
        "release_year": "Release Year",
        "median_recommendations": "Median Recommendations",
    },
)

st.plotly_chart(fig_median, use_container_width=True)

# =========================
# ROW 4 — Genre Contribution Over Time
# =========================
st.subheader("Genre Contribution to Engagement")

df_genres = explode_genres(df)

top_genres = (
    df_genres.groupby("genres")["recommendations"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
)

genre_yearly = (
    df_genres[df_genres["genres"].isin(top_genres)]
    .groupby(["release_year", "genres"])["recommendations"]
    .sum()
    .reset_index()
)

fig_genre = px.area(
    genre_yearly,
    x="release_year",
    y="recommendations",
    color="genres",
    labels={
        "release_year": "Release Year",
        "recommendations": "Total Recommendations",
    },
)

st.plotly_chart(fig_genre, use_container_width=True)
