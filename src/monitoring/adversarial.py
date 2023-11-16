# Standard Library Imports
from typing import Union

# Third Party Imports
import mlflow
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

# docformatter Package Imports
from src.constants import ADV_MODEL_PARAMS


def train_adversarial(
    X_train: pd.DataFrame, X_test: pd.DataFrame, experiment_name: str, mlflow_tags: dict
) -> Union[RandomForestClassifier, LogisticRegression, DecisionTreeClassifier]:
    mlflow.sklearn.autolog(log_datasets=False)
    mlflow.set_experiment(experiment_name)

    X_train["label"] = 0
    X_test["label"] = 1

    X = pd.concat([X_train, X_test], axis=0)
    X.reset_index(drop=True, inplace=True)

    y = X["label"].copy()
    X = X.drop(["label"], axis=1)
    X = X.fillna(-9999)

    with mlflow.start_run():
        mlflow.set_tags(mlflow_tags)
        model = LogisticRegression(**ADV_MODEL_PARAMS)
        model.fit(X, y)

        coefficients = model.coef_[0]
        feature_importance = pd.DataFrame({"Feature": X.columns, "Importance": np.abs(coefficients)})
        feature_importance = feature_importance.sort_values(by=["Importance"], ascending=False, ignore_index=True)
        feature_importance = feature_importance.iloc[:10, :]
        feature_importance.to_csv("feature_importance.csv", index=False)
        mlflow.log_artifact("feature_importance.csv")

    mlflow.end_run()

    return model
