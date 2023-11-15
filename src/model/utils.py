import os

import lightgbm as lgb
import pandas as pd
import mlflow

from src.constants import MLFLOW_ARTIFACT_ROOT, MLFLOW_TRACKING_URI, EVALUATOR_CONFIG

os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_TRACKING_URI
os.environ["MLFLOW_ARTIFACT_ROOT"] = MLFLOW_ARTIFACT_ROOT


def train_model(X_train: pd.DataFrame, y_train: pd.Series, X_test:pd.DataFrame, y_test: pd.Series, params: dict, tags: dict, **kwargs) -> lgb.LGBMClassifier:
    mlflow.lightgbm.autolog()

    with mlflow.start_run():
        mlflow.set_tags(tags)
        model = lgb.LGBMClassifier(**params)
        model.fit(X_train, y_train, **kwargs)

        eval_data = X_test.copy()
        eval_data["target"] = y_test.copy()

        model_info = mlflow.lightgbm.log_model(model, "model", input_example=X_train.loc[[0]])

        mlflow.evaluate(
            model_info.model_uri,
            model_type="classifier",
            data=eval_data,
            targets="target",
            evaluators="default",
            evaluator_config=EVALUATOR_CONFIG,
        )

    mlflow.end_run()

    return model
