import duckdb
import pandas as pd

from src.constants import MONTHS_BASELINE, MONTHS_INFERENCE, PARAMS, PATH_CRUDO, PATH_DATABASE, RUN_ETL
from src.model.utils import train_model
from src.preprocess.etl import extract, get_dataframe, transform

if __name__ == "__main__":
    con = duckdb.connect(database=PATH_DATABASE, read_only=False)
    if RUN_ETL:
        all_months = MONTHS_BASELINE + MONTHS_INFERENCE
        all_months = [str(month) for month in all_months]
        where_clause = ", ".join(all_months)
        extract(con, PATH_CRUDO, where_clause)
        transform(con, False, True)

    # # Train baseline model
    # baseline = train_model(X_train, y_train, PARAMS)
    #
    # kwargs = {
    #     'init_model': baseline
    # }
    #
    #
    # tags = {
    #     'stage': 'adversarial',
    #     'last_month': f'{int(adversarial_data["foto_mes"].max())}'
    # }
    #
    #
    # tags_monthly = {
    #     'stage': 'monthly',
    #     'last_month': f'{int(X_train["foto_mes"].max())}'
    # }


