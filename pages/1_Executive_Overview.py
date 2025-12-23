import streamlit as st
import plotly.express as px

from utils.metrics import (
    compute_overview_metrics,
    generate_overview_summary
)

from utils.feature_engineering import add_primary_genre


# ===============================
# Data
# ===============================
from utils.data_loader import load_data

df = load_data()
df = add_primary_genre(df)

st.title("Steam Market Intelligence — Executive Overview")
st.caption(
    "High-level view of market size, engagement patterns, and monetization trends on Steam (2021–2025)."
)

# ===============================
# KPI ROW
# ===============================
metrics = compute_overview_metrics(df)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Games", f"{metrics['total_games']:,}")
col2.metric("Total Recommendations", f"{metrics['total_recommendations']:,}")
col3.metric("Avg Game Price", f"₹{metrics['avg_price']}")
col4.metric("Free Games (%)", f"{metrics['free_pct']}%")
col5.metric("Top Genre", metrics["top_genre"])

st.markdown("---")

# ===============================
# ROW 2 — Market Scale & Attention
# ===============================
col1, col2 = st.columns(2)

with col1:
    releases = (
        df.groupby("release_year")
        .size()
        .reset_index(name="games_released")
    )

    fig = px.line(
        releases,
        x="release_year",
        y="games_released",
        markers=True,
        title="Steam Game Releases Over Time"
    )
    fig.update_layout(yaxis_title="Number of Games", xaxis_title="Release Year")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(
        df,
        x="recommendations",
        nbins=60,
        log_y=True,
        title="Distribution of Player Recommendations (Long-Tail Effect)"
    )
    fig.update_layout(
        xaxis_title="Number of Recommendations",
        yaxis_title="Number of Games"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ===============================
# ROW 3 — Monetization & Demand
# ===============================
col1, col2 = st.columns(2)

with col1:
    df["price_type"] = df["price"].apply(lambda x: "Free" if x == 0 else "Paid")

    fig = px.box(
        df,
        x="price_type",
        y="recommendations",
        log_y=True,
        title="Player Engagement: Free vs Paid Games"
    )
    fig.update_layout(
        xaxis_title="Game Type",
        yaxis_title="Recommendations (log scale)"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    genre_reco = (
        df.groupby("primary_genre")["recommendations"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        genre_reco,
        x="recommendations",
        y="primary_genre",
        orientation="h",
        title="Top Genres by Total Player Recommendations"
    )
    fig.update_layout(
        xaxis_title="Total Recommendations",
        yaxis_title="Genre"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ===============================
# AUTO-GENERATED SUMMARY
# ===============================
st.subheader("🧠 Auto-Generated Summary")

summary_points = generate_overview_summary(df, metrics)

with st.container():
    for point in summary_points:
        st.markdown(f"- {point}")
