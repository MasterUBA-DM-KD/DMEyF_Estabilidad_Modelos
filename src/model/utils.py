import lightgbm as lgb
import pandas as pd
import mlflow


def train_model(X_train: pd.DataFrame, y_train: pd.Series, params: dict, tags: dict, **kwargs) -> lgb.LGBMClassifier:
    mlflow.lightgbm.autolog()

    with mlflow.start_run():
        mlflow.set_tags(tags)
        model = lgb.LGBMClassifier(**params)
        model.fit(X_train, y_train, **kwargs)

    mlflow.end_run()

    return model
