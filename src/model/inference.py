# Third Party Imports
import lightgbm as lgb
import pandas as pd


def predict_month(model: lgb.LGBMClassifier, X_test: pd.DataFrame) -> pd.DataFrame:
    predictions = model.predict_proba(X_test)
    predictions = predictions[:, 1]
    return predictions
