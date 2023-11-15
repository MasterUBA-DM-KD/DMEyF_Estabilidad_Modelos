import duckdb

from src.constants import MONTHS_BASELINE, MONTHS_INFERENCE, PATH_CRUDO, PATH_DATABASE, PATH_FINAL, RUN_ETL
from src.preprocess.etl import extract, load, transform

if __name__ == "__main__":
    con = duckdb.connect(database=PATH_DATABASE, read_only=False)
    if RUN_ETL:
        extract(con, PATH_CRUDO, '1=1')
        transform(con, True, True)
        load(con, PATH_FINAL)
    else:
        all_months = MONTHS_BASELINE + MONTHS_INFERENCE
        all_months = [str(month) for month in all_months]
        where_clause = ", ".join(all_months)
        extract(con, PATH_FINAL, where_clause)