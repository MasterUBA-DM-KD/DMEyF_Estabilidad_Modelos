# Standard Library Imports
import os

# Third Party Imports
import lightgbm as lgb
import mlflow
import pandas as pd

# docformatter Package Imports
from src.constants import MLFLOW_ARTIFACT_ROOT, MLFLOW_TRACKING_URI

os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_TRACKING_URI
os.environ["MLFLOW_ARTIFACT_ROOT"] = MLFLOW_ARTIFACT_ROOT


def train_model(
    X_train: pd.DataFrame,
    y_train_binaria: pd.Series,
    X_test: pd.DataFrame,
    y_real_ternaria: pd.Series,
    y_real_binaria: pd.Series,
    experiment_name: str,
    params: dict,
    tags: dict,
    **kwargs,
) -> lgb.LGBMClassifier:
    mlflow.lightgbm.autolog()
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run():
        mlflow.set_tags(tags)
        model = lgb.LGBMClassifier(**params)
        model.fit(X_train, y_train_binaria, **kwargs)

        model_info = mlflow.lightgbm.log_model(model, "model", input_example=X_train.loc[[0]])

        if X_test is not None:
            eval_data = X_test.copy()
            eval_data["target"] = y_real_ternaria.copy()

            mlflow.evaluate(
                model_info.model_uri,
                model_type="classifier",
                data=eval_data,
                targets="target",
                evaluators="default",
                evaluator_config={"log_model_explainability": False, "metric_prefix": "real_ternaria_"},
            )

            eval_data = X_test.copy()
            eval_data["target"] = y_real_binaria.copy()

            mlflow.evaluate(
                model_info.model_uri,
                model_type="classifier",
                data=eval_data,
                targets="target",
                evaluators="default",
                evaluator_config={"log_model_explainability": False, "metric_prefix": "real_binaria_"},
            )

    mlflow.end_run()

    return model
