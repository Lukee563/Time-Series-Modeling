#  Causal Effects in High-Frequency Virtual Markets
## Estimating the Causal Effect of Hypixel Skyblock's 15% Price Increase on Booster Cookie Prices

A production-ready econometric pipeline designed to ingest, align, and analyze high-frequency time-series data from the Hypixel Skyblock market. This project utilizes a Difference-in-Differences (DiD) framework to quantify the causal impact of the April 15, 2026, premium currency restructuring on the real value of Booster Cookies relative to a composite macroeconomic control index.

## Project Context
The Hypixel Skyblock economy is a highly volatile, player-driven marketplace. Isolating the true macroeconomic pass-through of a developer policy shock is difficult due to high-frequency speculative noise and localized asset bubbles. This quantitative engine solves these issues to provide clean causal estimates:
* **Composite Control Engineering:** Dynamically aggregates 12 individual Perfect Gemstone markets to construct a stable, economy-wide commodity index, successfully satisfying the Parallel Trends assumption.
* **High-Frequency Noise Filtering:** Implements a chronological 3-day binning architecture to smooth out daily micro-variance and eliminate short-term liquidity shocks, reducing localized asset skew.
* **Robust Causal Identification:** Deploys an OLS Fixed Effects panel model utilizing Newey-West HAC (Heteroskedasticity and Autocorrelation Consistent) standard errors (with a mathematically optimized 4-period lag) to rigorously estimate relative purchasing power transfers.

## Repository Structure
    Virtual-Economies-DiD/
    ├── analysis/
    │   └── modeling.ipynb       # Jupyter notebook for DiD event study, parallel trends verification, and regression outputs
    ├── data/
    │   ├── raw/                 # Unprocessed API responses for the Booster Cookie and 12 Perfect Gemstone variants
    │   └── cleaned/             # 3-day binned, long-format panel data ready for econometric modeling
    ├── scripts/
    │   ├── data_construction.py # Data ingestion, structural alignment, and panel assembly
    │   ├── market_api.py        # Logic for parallel ingestion of Coflnet historical market endpoints
    └── .gitignore               # Standard Python VSCode GitIgnore

## Technical Approach
The pipeline follows a strict econometric order of operations to maintain statistical integrity:

1. **Parallel API Ingestion:** Automates the retrieval of historical pricing vectors for both the treatment asset (Booster Cookies) and the counterfactual assets (Mining Commodities).
2. **Temporal Alignment & Binning:** Raw timestamps are parsed, sorted, and downsampled into 3-day rolling averages to compress residual variance and normalize the error distribution (resolving Jarque-Bera non-normality).
3. **Panel Assembly:** The binned time-series are structurally stacked into a long-format panel, injecting deterministic policy indicators (`Treatment`, `Post`, and `DiD_Interaction`).
4. **Estimation:** The final model isolates the specific real-value acceleration of the premium currency, yielding an R-squared of 0.974 within the localized event window.

## Getting Started
To integrate the construction pipeline into your own analysis and replicate the panel structure:

    import sys
    import os
    sys.path.append(os.path.abspath('..'))

    from scripts.market_api import data_pull
    from scripts.data_construction import assemble_panel

    # 1. Pull the latest historical market data
    data_pull('https://sky.coflnet.com/api/bazaar/BOOSTER_COOKIE/history', 'data/raw/booster_cookie_historical.csv')

    # 2. Construct the binned, model-ready panel
    # (Automatically handles composite indexing if multiple counterfactuals are present in data/raw/)
    panel_df = assemble_panel(bin_frequency='3D')
