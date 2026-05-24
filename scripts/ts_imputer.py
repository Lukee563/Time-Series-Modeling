import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

## ----------------------------------------------------------------------
# Rather than assuming the distributional qualities of the market data,
# I will fit an XGBoost model to a training panel of unbroken records, 
# validate model performance through train-test validation, then impute 
# the missing values to reconstruct a high-quality time series panel.
## ----------------------------------------------------------------------

## Example input: data = all data, broken_cols = {'minBuy': 0.1002, 'minSell': 0.497}

def imputer(data, broken_cols_dict):
    # Clone the data 
    df_clean = data.copy()

    # Identify all completely clean columns to use as baseline features
    all_numeric = df_clean.select_dtypes(include=["number"]).columns
    initially_clean_cols = [c for c in all_numeric if c not in broken_cols_dict]

    # Sort broken columns by missingness percentage (lowest to highest)
    # This allows us to use repaired columns as features for subsequent iterations
    sorted_broken_cols = [
        k for k, v in sorted(broken_cols_dict.items(), key=lambda item: item[1])
    ]

    print(f"Starting sequential XGBoost Imputation Pipeline\n")

    # Keep a running list of features we are allowed to use to predict targets
    current_features = list(initially_clean_cols)

    for target in sorted_broken_cols:
        print(f"--- Imputing Target Column: {target} ---")

        # Separate the target column into broken (to impute) and unbroken (to train)
        is_na = df_clean[target].isna()

        # Unbroken records become our training panel
        train_panel = df_clean[~is_na]
        predict_panel = df_clean[is_na]

        X = train_panel[current_features]
        y = train_panel[target]

        # Train-Test Split on the unbroken records for quantitative validation
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Fit the non-parametric XGBoost Regressor
        model = XGBRegressor(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
        )
        model.fit(X_train, y_train)

        # Out-of-Sample Performance Evaluation
        preds = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)
        print(
            f"Validation Performance -> OOS RMSE: {round(rmse, 4)} | OOS R²: {round(r2 * 100, 2)}%"
        )

        # Impute the actual missing values in the main dataframe
        if len(predict_panel) > 0:
            X_missing = predict_panel[current_features]
            imputed_values = model.predict(X_missing)
            df_clean.loc[is_na, target] = imputed_values
            print(f"Successfully imputed {len(predict_panel)} missing values.")
        else:
            print("No missing values detected to impute.")

        # Append the newly repaired column to our feature pool
        # This ensures 'minSell' benefits from the information inside a clean 'buy'/'sell' column
        current_features.append(target)
        print(f"Feature pool expanded. Current feature count: {len(current_features)}\n")

    return df_clean