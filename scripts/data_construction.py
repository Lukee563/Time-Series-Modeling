import pandas as pd
import numpy as np
import seaborn as sns
from scripts.ts_imputer import imputer

def data_construction(path):
    """ 
    Constructs lagged variables, interpolates columns with low missing NA values, 
    calls the imputer function to estimate values for the boundary columns 
    such as minSell and minBuy. 
    """

    ## Pull static market data for the Hypixel - Minecraft Cocoa Bean Market
    cocoa_data = pd.read_csv(path)

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
    cocoa_data["timestamp"] = pd.to_datetime(cocoa_data["timestamp"], format="ISO8601")
    cocoa_data = cocoa_data.sort_values("timestamp", ascending=True).reset_index(drop=True)

    ## Clear Most Recent (Incomplete) Day
    cocoa_data = cocoa_data[1:len(cocoa_data)]

    # Interpolate the Highly Dense Columns with linear interpolation
    dense_cols = ["maxSell", "buy", "sell", "buyVolume", "sellVolume"]
    cocoa_data[dense_cols] = cocoa_data[dense_cols].interpolate(method="linear")

    # Engineer lags
    cocoa_data['buyMovingWeek_lag_1'] = cocoa_data['buyMovingWeek'].shift(1)
    cocoa_data['sellMovingWeek_lag_1'] = cocoa_data['sellMovingWeek'].shift(1)
    cocoa_data["buy_lag_1"] = cocoa_data["buy"].shift(1)
    cocoa_data["sell_lag_1"] = cocoa_data["sell"].shift(1)

    # Fix the Row 0 shift NaN
    lag_cols = ['buyMovingWeek_lag_1', 'sellMovingWeek_lag_1', 'buy_lag_1', 'sell_lag_1']
    cocoa_data[lag_cols] = cocoa_data[lag_cols].bfill()

    # Build the Repair Dictionary
    cols = cocoa_data.columns
    broken_cols = {}

    for c in cols:
        na_values = cocoa_data[c].isna().sum()
        na_percent = round((na_values / len(cocoa_data)), 4)

        if na_values > 0:
            broken_cols[c] = float(na_percent)

    # Imputation Task
    cocoa_data_clean = imputer(cocoa_data, broken_cols)
    cocoa_data_clean.to_csv("data/cleaned/cocoa_beans_historical_cleaned.csv")
    return cocoa_data_clean

