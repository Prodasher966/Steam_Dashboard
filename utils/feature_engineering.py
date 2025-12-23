import pandas as pd
import numpy as np

# -------------------------
# Genre Processing
# -------------------------
def explode_genres(df):
    df = df.copy()
    df["genres"] = df["genres"].str.split(",")
    df = df.explode("genres")
    df["genres"] = df["genres"].str.strip()
    return df


# -------------------------
# Pricing Buckets
# -------------------------
def add_price_buckets(df):
    df = df.copy()

    def bucket(price):
        if price == 0:
            return "Free"
        elif price <= 500:
            return "Low (₹1–₹500)"
        elif price <= 1000:
            return "Mid (₹501–₹1000)"
        else:
            return "High (₹1000+)"

    df["price_bucket"] = df["price"].apply(bucket)
    df["pricing_type"] = np.where(df["price"] == 0, "Free", "Paid")

    return df


# -------------------------
# Yearly Aggregates
# -------------------------
def yearly_metrics(df):
    return (
        df.groupby("release_year")
        .agg(
            game_count=("appid", "count"),
            total_recommendations=("recommendations", "sum"),
            avg_recommendations=("recommendations", "mean"),
            median_recommendations=("recommendations", "median"),
        )
        .reset_index()
        .sort_values("release_year")
    )


# -------------------------
# Publisher / Developer Aggregates
# -------------------------
def entity_metrics(df, column):
    return (
        df.groupby(column)
        .agg(
            game_count=("appid", "count"),
            total_recommendations=("recommendations", "sum"),
            avg_recommendations=("recommendations", "mean"),
            median_recommendations=("recommendations", "median"),
        )
        .reset_index()
    )

def missing_value_summary(df):
    return (
        df.isna()
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
        .rename(columns={"index": "column", 0: "missing_pct"})
    )
    
def yearly_coverage(df):
    return (
        df.groupby("release_year")["appid"]
        .count()
        .reset_index(name="records")
        .sort_values("release_year")
    )
    
def add_primary_genre(df):
    df = df.copy()

    df["primary_genre"] = (
        df["genres"]
        .fillna("Unknown")
        .str.split(",")
        .str[0]
        .str.strip()
    )

    return df
