import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """
    Loads the Steam games dataset.
    Acts as a single source of truth for all pages.
    """
    df = pd.read_csv("data/steam_games.csv")

    # Standardize column names (safety)
    df.columns = df.columns.str.lower()

    return df
