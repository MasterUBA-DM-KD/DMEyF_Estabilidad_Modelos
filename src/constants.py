RUN_ETL = False
RANDOM_STATE = 42
PATH_DATABASE = "database/database.db"
PATH_CRUDO = "~/buckets/b1/datasets/raw/competencia_03_crudo.parquet"
PATH_FINAL = "~/buckets/b1/exp_colab/datasets/processed/competencia_03.parquet"
PATH_MAX_GAN = "~/buckets/b1/exp_colab/datasets/processed/ganancia_maxima.parquet"

MONTHS_BASELINE = [
    202007,
    202008,
    202009,
    202010,
    202011,
    202012,
    202101,
    202102,
    202103,
]

MONTHS_INFERENCE = [
    202104,
    202105,
    202106,
    202107,
    202108,
    202109
]

LAG_FILES = [
    "sql/lags_1.sql",
    "sql/lags_3.sql",
    "sql/lags_6.sql",
]

PARAMS = {
    'objective': 'binary',
    'metric': 'auc',
    'is_unbalance': True,
    'bagging_freq': 5,
    'boosting': 'dart',
    'num_boost_round': 300,
    "verbosity": -1,
    "n_jobs": -1,
    "seed": RANDOM_STATE,
}

ADV_MODEL_PARAMS = {
    'random_state': RANDOM_STATE,
    'n_jobs': -1
}

EVALUATOR_CONFIG = {
    "log_model_explainability": False,
    "metric_prefix": "evaluation_"
}


MLFLOW_TRACKING_URI = "sqlite:///buckets/b1/exp_colab/database/mlruns.db"
MLFLOW_ARTIFACT_ROOT = "gs://mlflow-artifacts-uribe/mlruns_exp_colab"

