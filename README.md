# Time-Series-Modeling: Hypixel Skyblock Cocoa Market

A production-ready data engineering and modeling pipeline designed to ingest, sanitize, and reconstruct high-velocity time-series data from the Hypixel Skyblock Cocoa Bean market. This framework addresses critical data quality issues by employing multivariate, model-based imputation techniques that maintain strict temporal causality.

## Pipeline Architecture


## Project Context
The Hypixel Skyblock economy is a highly volatile, player-driven marketplace. Accurate price discovery is difficult due to sparse data and missing order-book entries. This project serves as a robust quantitative engine to:
* Prevent Look-Ahead Bias: Implements chronological data processing to ensure forecasting models are trained strictly on past observations.
* Recover Missing Market Intelligence: Uses a sequential XGBoost imputation pipeline to reconstruct fragmented minBuy and minSell price points, the very edge of the order book. 
* Bridge Market Data: Leverages autoregressive (AR) feature engineering and rolling window statistics to provide a continuous, model-ready panel for arbitrage analysis.

## Repository Structure
```
Time-Series-Modeling/
├── analysis/
│   └── modeling.ipynb       # Jupyter notebook for research, backtesting, and visualization
├── data/
│   ├── raw/                 # Unprocessed API response
│   └── cleaned/             # Imputed panel ready for modeling
├── scripts/
│   ├── data_construction.py # Data ingestion and feature engineering
│   ├── market_api.py        # Logic for interacting with Hypixel marketplace endpoints
│   └── ts_imputer.py        # Custom multivariate XGBoost imputation engine
└── .gitignore               # Standard Python VSCode GitIgnore
```

## Technical Approach
The pipeline follows a rigorous order of operations to maintain statistical integrity:

1. Temporal Alignment: Raw timestamps are parsed and sorted chronologically to eliminate data leakage.
2. Dense Interpolation: Highly continuous variables (e.g., buy, sell, volumes) are bridged using linear interpolation.
3. Temporal Feature Engineering: AR(1) spot lags and moving weekly window features are injected to capture momentum.
4. Sequential Imputation: XGBoost is deployed to surgically reconstruct the sparse boundary layers (minBuy/minSell) of the market, ensuring the imputed values are statistically consistent with observed global market trends.

## Getting Started
This repository is built for modularity. To integrate the construction pipeline into your own analysis, ensure the project root is in your sys.path:

import sys
sys.path.append('path/to/Time-Series-Modeling')

from scripts.data_construction import data_construction
# Returns a clean, model-ready panel
df = data_construction(path="data/raw/cocoa_beans_historical.csv")
