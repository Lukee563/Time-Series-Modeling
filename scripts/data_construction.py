import pandas as pd
import numpy as np
from scripts.ts_imputer import imputer

def data_construction(path):
    """ 
    Constructs lagged variables, interpolates columns with low missing NA values, 
    calls the imputer function to estimate values for the boundary columns 
    such as minSell and minBuy. 
    """

    ## Pull static market data for the Hypixel - Booster Cookie Market
    cookie_data = pd.read_csv(path)

    ## ----------------------------------------------------------------------
    # An immediate problem presents itself in the form of missing values across
    # highly relevant columns [minBuy, minSell, etc,]. Rather than using univariate 
    # imputation methods (Mean, Mode, Median imputation) I'll be using model-based 
    # multivariate techniques depending on the distributional qualities of each unique column. 
    # The goal is to create a panel with the highest probability of accuracy for later 
    # buy-side quantitative modeling. 
    # (It's a video game, but who doesn't like market arbitrage against 12 year olds.) 
    ## ----------------------------------------------------------------------

    # Sort chronologically to prevent look-ahead bias
    cookie_data["timestamp"] = pd.to_datetime(cookie_data["timestamp"], format="ISO8601")
    cookie_data = cookie_data.sort_values("timestamp", ascending=True).reset_index(drop=True)

    ## Clear Most Recent (Incomplete) Day
    cookie_data = cookie_data[1:len(cookie_data)]

    # Interpolate the Highly Dense Columns with linear interpolation
    dense_cols = ["maxSell", "buy", "sell", "buyVolume", "sellVolume"]
    cookie_data[dense_cols] = cookie_data[dense_cols].interpolate(method="linear")

    # Engineer lags
    cookie_data['buyMovingWeek_lag_1'] = cookie_data['buyMovingWeek'].shift(1)
    cookie_data['sellMovingWeek_lag_1'] = cookie_data['sellMovingWeek'].shift(1)
    cookie_data["buy_lag_1"] = cookie_data["buy"].shift(1)
    cookie_data["sell_lag_1"] = cookie_data["sell"].shift(1)

    # Fix the Row 0 shift NaN
    lag_cols = ['buyMovingWeek_lag_1', 'sellMovingWeek_lag_1', 'buy_lag_1', 'sell_lag_1']
    cookie_data[lag_cols] = cookie_data[lag_cols].bfill()

    # Build the Repair Dictionary
    cols = cookie_data.columns
    broken_cols = {}

    for c in cols:
        na_values = cookie_data[c].isna().sum()
        na_percent = round((na_values / len(cookie_data)), 4)

        if na_values > 0:
            broken_cols[c] = float(na_percent)

    # Imputation Task
    cookie_data_clean = imputer(cookie_data, broken_cols)
    cookie_data_clean.to_csv("data/cleaned/cookie_market_cleaned.csv")
    return cookie_data_clean

