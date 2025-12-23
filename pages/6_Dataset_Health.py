import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.feature_engineering import missing_value_summary, yearly_coverage
from utils.metrics import calculate_health_score, generate_health_summary

st.set_page_config(layout="wide")

# =========================
# Page Header
# =========================
st.title("Dataset Health & Credibility")
st.caption(
    "Assessment of data completeness, temporal coverage, and overall analytical reliability."
)

# =========================
# Load Data
# =========================
df = load_data()

# =========================
# Feature Engineering
# =========================
missing_df = missing_value_summary(df)
yearly_df = yearly_coverage(df)

# =========================
# Health Score
# =========================
health_score = calculate_health_score(missing_df, yearly_df)

st.metric("Dataset Health Score", f"{health_score}/100")

# =========================
# ROW 1 — Missing Values
# =========================
st.subheader("Missing Value Distribution")

fig_missing = px.bar(
    missing_df.sort_values("missing_pct"),
    x="missing_pct",
    y="column",
    orientation="h",
    labels={
        "missing_pct": "Missing (%)",
        "column": "Column",
    },
)

st.plotly_chart(fig_missing, use_container_width=True)

# =========================
# ROW 2 — Temporal Coverage
# =========================
st.subheader("Records per Release Year")

fig_yearly = px.line(
    yearly_df,
    x="release_year",
    y="records",
    markers=True,
    labels={
        "release_year": "Release Year",
        "records": "Number of Records",
    },
)

st.plotly_chart(fig_yearly, use_container_width=True)

# =========================
# ROW 3 — Auto Summary
# =========================
st.subheader("Credibility Assessment")

summary = generate_health_summary(health_score, missing_df)
st.info(summary)
