import streamlit as st
from utils.data_loader import load_data
from utils.feature_engineering import add_primary_genre

if "df" not in st.session_state:
    df = load_data()
    df = add_primary_genre(df)
    st.session_state["df"] = df

# =========================
# Global Page Config
# =========================
st.set_page_config(
    page_title="Steam Market Intelligence Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# Sidebar Branding
# =========================
st.sidebar.title("Steam Intelligence")
st.sidebar.caption("Portfolio Analytics Dashboard")

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
**Project Scope**
- Steam games (2021–2025)
- ~65K records
- Market & engagement analysis

**Focus Areas**
- Market trends
- Genre intelligence
- Pricing & monetization
- Publisher & developer analysis
- Dataset credibility
"""
)

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit • Plotly • Pandas")

# =========================
# Main Landing Page
# =========================
st.title("Steam Market Intelligence Dashboard")
st.subheader("A data-driven analysis of Steam’s game ecosystem (2021–2025)")

st.markdown(
    """
This dashboard presents an **analytical overview of the Steam marketplace**, focusing on  
game supply, player engagement, monetization strategies, and market structure.

Rather than showcasing raw charts, the project emphasizes:
- **Insight-driven analysis**
- **Metric transparency**
- **Data credibility**
- **Interpretability over visual noise**
"""
)

# =========================
# What This Dashboard Covers
# =========================
st.markdown("### What You’ll Find Inside")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
**📊 Executive Overview**
- High-level KPIs
- Market scale and engagement snapshot

**🎯 Genre Intelligence**
- Supply vs demand by genre
- Engagement efficiency analysis

**💰 Pricing & Monetization**
- Price tier performance
- Free vs paid dynamics
"""
    )

with col2:
    st.markdown(
        """
**🏢 Developer & Publisher Intelligence**
- Market concentration
- Entity efficiency signals

**📈 Market Trends**
- Growth vs saturation
- Engagement evolution over time

**🧪 Dataset Health**
- Missing values
- Temporal coverage
- Credibility scoring
"""
    )

# =========================
# How to Use
# =========================
st.markdown("---")
st.markdown(
    """
### How to Navigate

Use the **sidebar** to explore individual analysis pages.  
Each page includes:
- Focused visualizations
- Interpretable metrics
- An **auto-generated insight summary** at the bottom

This ensures that every chart answers a clear business question.
"""
)

# =========================
# Footer
# =========================
st.markdown("---")
st.caption(
    "This dashboard is a personal portfolio project designed to demonstrate analytical thinking, "
    "data modeling discipline, and insight communication."
)
