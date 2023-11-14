import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from src.constants import ADV_MODEL_PARAMS


def train_adversarial(adversarial_data: pd.DataFrame, mlflow_tags: dict) -> RandomForestClassifier:
    mlflow.sklearn.autolog()

    X = adversarial_data.drop(columns=['label'])
    y = adversarial_data['label']

    with mlflow.start_run():
        mlflow.set_experiment_tags(mlflow_tags)
        model = RandomForestClassifier(**ADV_MODEL_PARAMS)
        model.fit(X, y)

    mlflow.end_run()

    return model
