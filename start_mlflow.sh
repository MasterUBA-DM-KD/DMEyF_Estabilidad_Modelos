export MLFLOW_TRACKING_URI=sqlite:///buckets/b1/exp_colab/database/mlruns.db &&
export MLFLOW_ARTIFACT_ROOT=gs://mlflow-artifacts-uribe/mlruns_exp_colab &&
mlflow ui --backend-store-uri $MLFLOW_TRACKING_URI --default-artifact-root $MLFLOW_ARTIFACT_ROOT --host 0.0.0.0 --port 5000
mlflow server --backend-store-uri $MLFLOW_TRACKING_URI --default-artifact-root $MLFLOW_ARTIFACT_ROOT --host 0.0.0.0 --port 6000 &
