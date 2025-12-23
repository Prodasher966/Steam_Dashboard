import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.feature_engineering import entity_metrics
from utils.metrics import generate_entity_summary

st.set_page_config(layout="wide")

# =========================
# Page Header
# =========================
st.title("Developer & Publisher Intelligence")
st.caption(
    "Comparative analysis of developer and publisher performance, concentration, and engagement efficiency."
)

# =========================
# Load Data
# =========================
df = load_data()
df = df.dropna(subset=["developer", "publisher", "recommendations"])

# =========================
# Entity Selection
# =========================
entity_type = st.radio(
    "Analyze by",
    ["Publisher", "Developer"],
    horizontal=True,
)

entity_col = "publisher" if entity_type == "Publisher" else "developer"

# =========================
# Feature Engineering
# =========================
entity_stats = entity_metrics(df, entity_col)

top_entities = entity_stats.head(15)

# =========================
# ROW 1 — Dominance
# =========================
st.subheader(f"Top {entity_type}s by Total Engagement")

fig_total = px.bar(
    top_entities,
    x="total_recommendations",
    y=entity_col,
    orientation="h",
    labels={
        entity_col: entity_type,
        "total_recommendations": "Total Recommendations",
    },
)

st.plotly_chart(fig_total, use_container_width=True)

# =========================
# ROW 2 — Efficiency
# =========================
st.subheader(f"{entity_type} Efficiency (Avg Engagement per Game)")

fig_avg = px.scatter(
    top_entities,
    x="game_count",
    y="avg_recommendations",
    size="total_recommendations",
    hover_name=entity_col,
    labels={
        "game_count": "Number of Games",
        "avg_recommendations": "Avg Recommendations",
    },
)

st.plotly_chart(fig_avg, use_container_width=True)

# =========================
# ROW 3 — Median Signal
# =========================
st.subheader("Median Engagement Signal")

fig_median = px.bar(
    top_entities.sort_values("median_recommendations"),
    x="median_recommendations",
    y=entity_col,
    orientation="h",
    labels={
        "median_recommendations": "Median Recommendations",
        entity_col: entity_type,
    },
)

st.plotly_chart(fig_median, use_container_width=True)

# =========================
# ROW 4 — Auto Summary
# =========================
st.subheader("Key Takeaways")

summary = generate_entity_summary(entity_stats, entity_type)
st.info(summary)
