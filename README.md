🎮 Steam Market Intelligence Dashboard (2021–2025)
--------------------------------------------------

A multi-page, insight-driven analytics dashboard built using **Streamlit** to analyze trends, engagement patterns, monetization strategies, and market structure of games published on **Steam** between 2021 and 2025.

This project focuses on **business-style analytics and decision-making insights**, rather than gamer-centric visuals, making it suitable for **portfolio and recruiter review**.

📊 Dashboard Overview
---------------------

The dashboard is structured into **six analytical sections**, each answering a specific market question:

### 1️⃣ Executive Overview

High-level snapshot of the Steam marketplace:

*   Total number of games released
    
*   Market growth across years
    
*   Engagement distribution
    
*   Dominant genres and pricing patterns
    

**Purpose:** Provide a quick, decision-maker–friendly understanding of market size and engagement.

### 2️⃣ Genre Intelligence

Deep dive into game genres:

*   Genre-wise game distribution
    
*   Engagement comparison across genres
    
*   Dominant and niche genres
    
*   Market concentration by genre
    

**Purpose:** Understand which genres drive volume and player engagement on Steam.

### 3️⃣ Pricing & Monetization

Analysis of pricing strategies:

*   Free-to-play vs paid games
    
*   Price bucket distribution
    
*   Engagement vs pricing
    
*   Monetization effectiveness
    

**Purpose:** Evaluate how pricing impacts player recommendations and market reach.

### 4️⃣ Developer & Publisher Intelligence

Market structure analysis:

*   Top developers and publishers by output
    
*   Engagement concentration
    
*   Long-tail vs major studios
    

**Purpose:** Assess whether the Steam market favors large publishers or smaller independent studios.

### 5️⃣ Market Trends

Temporal and structural analysis:

*   Game releases over time
    
*   Engagement growth vs market size
    
*   Median engagement trends
    
*   Genre contribution across years
    

**Purpose:**Identify long-term trends and structural shifts in the Steam marketplace.

### 6️⃣ Dataset Health & Credibility

Quality and reliability assessment of the dataset:

*   Missing values analysis
    
*   Distribution sanity checks
    
*   Outlier inspection
    
*   Coverage validation
    

**Purpose:** Ensure analytical conclusions are based on trustworthy data.

🗂️ Dataset Information
-----------------------

*   **Source:** Kaggle – Steam Games Dataset (2021–2025)
    
*   **Size:** ~65,000 game records
    
*   **Key Fields:**
    
    *   App ID
        
    *   Game name
        
    *   Release year & date
        
    *   Genres & categories
        
    *   Price
        
    *   Recommendations (engagement proxy)
        
    *   Developer & publisher
        

🛠️ Tech Stack
--------------

*   **Python**
    
*   **Streamlit** – interactive dashboard framework
    
*   **Pandas** – data manipulation & aggregation
    
*   **Plotly** – interactive visualizations
    
*   **Modular architecture** (pages, utilities, feature engineering)
    

📁 Project Structure
--------------------

```text
steam-dashboard/
│
├── app.py                      # Main entry point (Streamlit Landing Page)
│
├── data/
│   └── steam_games.csv         # Raw dataset containing Steam store information
│
├── pages/                      # Multi-page dashboard modules
│   ├── 1_Executive_Overview.py # High-level KPIs and market summary
│   ├── 2_Genre_Intelligence.py # Deep dive into genre performance and tags
│   ├── 3_Pricing_Monetization.py # Price distribution and revenue analysis
│   ├── 4_Developer_Publisher.py # Competitive landscape and studio metrics
│   ├── 5_Market_Trends.py      # Historical growth and release patterns
│   └── 6_Dataset_Health.py     # Data quality, missing values, and audit
│
├── utils/                      # Helper modules and logic
│   ├── data_loader.py          # Optimized CSV loading and caching
│   ├── feature_engineering.py  # Data transformation and cleaning logic
│   └── metrics.py              # Calculation engine for dashboard KPIs
│
└── README.md                   # Project documentation
```

🚀 How to Run
-------------
```bash
pip install -r requirements.txt
streamlit run app.py
```
🎯 Project Intent
-----------------

This project was built as a **portfolio-level analytics dashboard** to demonstrate:

*   Analytical thinking
    
*   Dashboard design
    
*   Data exploration at scale
    
*   Modular and maintainable code structure
    

It prioritizes **clarity, insight, and structure** over excessive automation or ML complexity.

📌 Disclaimer
-------------

This dashboard is intended for **educational and portfolio purposes**.
All insights are derived from publicly available data and do not represent official Steam analytics.
