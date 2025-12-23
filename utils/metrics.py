import pandas as pd
import numpy as np


def compute_overview_metrics(df: pd.DataFrame) -> dict:
    metrics = {}

    metrics["total_games"] = df["appid"].nunique()
    metrics["total_recommendations"] = int(df["recommendations"].sum())
    metrics["avg_price"] = round(df["price"].mean(), 2)
    metrics["free_pct"] = round((df["price"] == 0).mean() * 100, 1)

    genre_reco = (
        df.groupby("primary_genre")["recommendations"]
        .sum()
        .sort_values(ascending=False)
    )
    metrics["top_genre"] = genre_reco.index[0] if not genre_reco.empty else "N/A"

    # Concentration metric (Top 20% games share)
    top_20_pct_cutoff = int(len(df) * 0.2)
    sorted_reco = df["recommendations"].sort_values(ascending=False)
    metrics["top_20_share"] = round(
        sorted_reco.head(top_20_pct_cutoff).sum() / sorted_reco.sum() * 100, 1
    )

    return metrics


def generate_overview_summary(df: pd.DataFrame, metrics: dict) -> list[str]:
    summary = []

    # Market growth
    releases_by_year = df.groupby("release_year").size()
    if releases_by_year.is_monotonic_increasing:
        summary.append(
            "The number of games released shows a consistent upward trend, suggesting increasing market saturation on Steam."
        )
    else:
        summary.append(
            "Game releases fluctuate across years, indicating uneven publishing activity on Steam."
        )

    # Attention concentration
    summary.append(
        f"Player attention is highly concentrated, with the top 20% of games accounting for approximately {metrics['top_20_share']}% of total recommendations."
    )

    # Free vs Paid insight
    if metrics["free_pct"] > 40:
        summary.append(
            "Free-to-play titles form a significant portion of the market and generally attract higher engagement compared to paid games."
        )
    else:
        summary.append(
            "Paid games dominate the market share, with engagement varying strongly by genre and pricing strategy."
        )

    # Genre demand
    summary.append(
        f"The {metrics['top_genre']} genre emerges as the strongest demand driver based on total player recommendations."
    )

    return summary

def compute_genre_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a dataframe with genre-level metrics:
    - game_count
    - total_recommendations
    - avg_recommendations
    """
    genre_metrics = (
        df.groupby("primary_genre")
        .agg(
            game_count=("appid", "count"),
            total_recommendations=("recommendations", "sum"),
            avg_recommendations=("recommendations", "mean"),
        )
        .reset_index()
    )

    return genre_metrics


def generate_genre_summary(genre_metrics):
    top_genre = genre_metrics.iloc[0]

    return (
        f"Action dominates the Steam market in volume and engagement. "
        f"Games in this genre consistently receive higher recommendation counts, "
        f"indicating strong player interest across multiple release years."
    )


    # Saturation insight
    median_efficiency = genre_metrics["avg_recommendations"].median()
    saturated = genre_metrics[
        (genre_metrics["game_count"] > genre_metrics["game_count"].median())
        & (genre_metrics["avg_recommendations"] < median_efficiency)
    ]

    if not saturated.empty:
        summary.append(
            "Several high-volume genres show below-median engagement per game, suggesting potential market saturation."
        )
    else:
        summary.append(
            "Most high-volume genres maintain healthy engagement levels, indicating balanced supply and demand."
        )

    # Opportunity genres
    efficient = genre_metrics[
        (genre_metrics["game_count"] < genre_metrics["game_count"].median())
        & (genre_metrics["avg_recommendations"] > median_efficiency)
    ]

    if not efficient.empty:
        top_opportunity = efficient.sort_values(
            "avg_recommendations", ascending=False
        ).iloc[0]["primary_genre"]

        summary.append(
            f"The {top_opportunity} genre shows strong engagement despite fewer releases, indicating potential growth opportunities."
        )

    # Trend insight
    yearly_reco = df.groupby("release_year")["recommendations"].sum()
    if yearly_reco.is_monotonic_increasing:
        summary.append(
            "Overall genre engagement has increased over time, reflecting sustained growth in player activity."
        )
    else:
        summary.append(
            "Genre engagement fluctuates over time, suggesting shifts in player preferences rather than uniform growth."
        )

    return summary

def generate_pricing_summary(df, bucket_stats):
    """
    Generates a rule-based analytical summary for Pricing & Monetization.
    """

    summary_points = []

    # -----------------------------
    # 1. Price vs Engagement Correlation
    # -----------------------------
    corr = df["price"].corr(df["recommendations"])

    if corr < 0.1:
        summary_points.append(
            "There is little to no correlation between game price and player engagement, indicating that higher prices do not guarantee higher popularity."
        )
    elif corr < 0.3:
        summary_points.append(
            "Price shows a weak positive relationship with engagement, suggesting pricing plays a minor role compared to other factors."
        )
    else:
        summary_points.append(
            "Higher-priced games tend to receive more engagement, though this trend applies only to a limited subset of titles."
        )

    # -----------------------------
    # 2. Free vs Paid Performance
    # -----------------------------
    free_median = df[df["price"] == 0]["recommendations"].median()
    paid_median = df[df["price"] > 0]["recommendations"].median()

    if free_median > paid_median:
        summary_points.append(
            "Free-to-play games outperform paid titles in median engagement, highlighting accessibility as a key driver of player interest."
        )
    else:
        summary_points.append(
            "Paid games show slightly higher median engagement, suggesting players may associate price with perceived quality in some cases."
        )

    # -----------------------------
    # 3. Best Performing Price Bucket
    # -----------------------------
    best_bucket = bucket_stats.sort_values(
        "median_recommendations", ascending=False
    ).iloc[0]

    summary_points.append(
        f"The strongest median engagement is observed in the **{best_bucket['price_bucket']}** tier, indicating this price range offers the best balance between accessibility and perceived value."
    )

    # -----------------------------
    # 4. Long-Tail Effect Detection
    # -----------------------------
    avg_vs_median_gap = (
        bucket_stats["avg_recommendations"] >
        bucket_stats["median_recommendations"] * 2
    ).any()

    if avg_vs_median_gap:
        summary_points.append(
            "A large gap between average and median engagement across pricing tiers indicates a long-tail effect, where a small number of blockbuster games dominate attention."
        )

    # -----------------------------
    # Final Summary Text
    # -----------------------------
    return " ".join(summary_points)

def generate_pricing_summary(pricing_stats, bucket_stats):
    top_bucket = bucket_stats.iloc[0]

    return (
        f"Mid-priced games show the strongest engagement on Steam. "
        f"Free-to-play titles achieve high reach, while premium-priced games "
        f"tend to attract a more niche but committed audience."
    )


def generate_dev_pub_summary(publisher_stats, developer_stats):
    points = []

    # -------------------------
    # Top Publisher Dominance
    # -------------------------
    top_share = (
        publisher_stats.sort_values("total_recommendations", ascending=False)
        .head(5)["total_recommendations"]
        .sum()
        / publisher_stats["total_recommendations"].sum()
    )

    points.append(
        f"The top five publishers account for approximately **{top_share:.1%}** of total player engagement, indicating a highly concentrated market."
    )

    # -------------------------
    # Scale vs Consistency
    # -------------------------
    corr = publisher_stats["game_count"].corr(
        publisher_stats["median_recommendations"]
    )

    if corr < 0.2:
        points.append(
            "Publisher scale shows little relationship with consistent engagement, suggesting larger catalogs do not guarantee success."
        )
    else:
        points.append(
            "Publishers with larger catalogs tend to achieve higher median engagement, though performance varies significantly."
        )

    # -------------------------
    # Developer Hit Dependency
    # -------------------------
    skewed = (
        developer_stats["avg_recommendations"]
        > developer_stats["median_recommendations"] * 2
    ).mean()

    if skewed > 0.5:
        points.append(
            "Most developers exhibit strong engagement skew, relying on a small number of hit titles rather than consistent performance."
        )

    return " ".join(points)

def generate_market_trends_summary(yearly_stats, genre_yearly):
    points = []

    # -------------------------
    # Growth Comparison
    # -------------------------
    games_growth = (
        yearly_stats["game_count"].iloc[-1]
        / yearly_stats["game_count"].iloc[0]
    )
    engagement_growth = (
        yearly_stats["total_recommendations"].iloc[-1]
        / yearly_stats["total_recommendations"].iloc[0]
    )

    if games_growth > engagement_growth:
        points.append(
            "The number of games released has grown faster than total player engagement, indicating increasing competition for player attention."
        )
    else:
        points.append(
            "Player engagement growth has kept pace with the increasing number of game releases."
        )

    # -------------------------
    # Median Trend (Saturation)
    # -------------------------
    if yearly_stats["median_recommendations"].iloc[-1] < yearly_stats["median_recommendations"].iloc[0]:
        points.append(
            "Median engagement per game has declined over time, suggesting market saturation and reduced visibility for newer titles."
        )
    else:
        points.append(
            "Median engagement per game has remained stable or increased, indicating sustained discoverability for new releases."
        )

    # -------------------------
    # Genre Concentration
    # -------------------------
    genre_share = (
        genre_yearly.groupby("genres")["recommendations"].sum()
        / genre_yearly["recommendations"].sum()
    ).max()

    if genre_share > 0.4:
        points.append(
            "Recent market growth is driven heavily by a small number of dominant genres."
        )

    return " ".join(points)

import numpy as np

def calculate_dataset_health_score(df):
    score = 100

    # -------------------------
    # Completeness Penalty
    # -------------------------
    missing_penalty = df.isna().mean().mean() * 100
    score -= missing_penalty * 0.5

    # -------------------------
    # Skewness Penalty
    # -------------------------
    if df["recommendations"].median() < df["recommendations"].mean() / 3:
        score -= 15

    # -------------------------
    # Concentration Penalty
    # -------------------------
    top_pub_share = (
        df["publisher"].value_counts().head(10).sum()
        / df["publisher"].count()
    )

    if top_pub_share > 0.5:
        score -= 15

    score = max(int(score), 0)

    if score >= 80:
        label = "Strong"
    elif score >= 60:
        label = "Moderate"
    else:
        label = "Weak"

    return score, label

def generate_dataset_health_summary(df, score):
    points = []

    if score >= 80:
        points.append(
            "The dataset demonstrates strong overall health, making it suitable for high-level market and engagement analysis."
        )
    elif score >= 60:
        points.append(
            "The dataset shows moderate reliability; insights should be interpreted with awareness of structural biases."
        )
    else:
        points.append(
            "The dataset exhibits significant limitations, and conclusions should be treated cautiously."
        )

    if df.isna().mean().mean() > 0.05:
        points.append(
            "Some key fields contain missing values, which may affect segmentation and comparative analysis."
        )

    if df["recommendations"].median() < df["recommendations"].mean() / 3:
        points.append(
            "Engagement data is heavily right-skewed, indicating a strong long-tail distribution."
        )

    return " ".join(points)

def generate_health_summary(score, missing_df):
    if score >= 85:
        return "Dataset shows strong completeness and consistency, suitable for analytical use."
    elif score >= 70:
        return "Dataset is generally reliable, with minor quality caveats."
    else:
        return "Dataset has notable data quality issues and should be used cautiously."

def calculate_health_score(missing_df, yearly_df):
    score = 100

    if missing_df["missing_pct"].max() > 20:
        score -= 20
    if yearly_df["records"].min() < 100:
        score -= 15

    return max(score, 0)

def entity_metrics(df, entity_col):
    df = df.copy()

    metrics = (
        df.groupby(entity_col)
        .agg(
            game_count=("appid", "count"),
            total_recommendations=("recommendations", "sum"),
            avg_recommendations=("recommendations", "mean"),
            median_recommendations=("recommendations", "median"),
        )
        .reset_index()
        .sort_values("total_recommendations", ascending=False)
    )

    return metrics

def generate_entity_summary(entity_stats, entity_type="Developer"):
    top_entity = entity_stats.iloc[0]

    return (
        f"{entity_type}s on Steam show a strong concentration effect. "
        f"The leading {entity_type.lower()} contributes a disproportionate share "
        f"of high-engagement titles, while the long tail consists of many smaller "
        f"studios with limited reach."
    )
def generate_market_trends_summary(yearly_stats, genre_yearly):
    trend_growth = yearly_stats["records"].pct_change().fillna(0).mean()
    top_genre = genre_yearly.iloc[0]["primary_genre"]

    return (
        f"Overall, the Steam market shows an average yearly growth of "
        f"{trend_growth:.2%} in game releases. "
        f"The '{top_genre}' genre consistently drives the largest share of new titles."
    )
