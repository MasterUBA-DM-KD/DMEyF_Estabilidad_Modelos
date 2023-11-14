import logging

import duckdb
import pandas as pd

from src.constants import LAG_FILES, MONTHS_INFERENCE

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def extract(con: duckdb.DuckDBPyConnection, path_parquet: str, where_clause: str) -> None:
    con.sql(
        f"""
        CREATE OR REPLACE TABLE competencia_03 AS (
            SELECT
                *
            FROM read_parquet('{path_parquet}')
            WHERE foto_mes IN({where_clause})
        )
        """
    )


def transform(con: duckdb.DuckDBPyConnection, lags: bool = True, ternaria: bool = True) -> None:
    if lags:
        create_lags(con)
    if ternaria:
        create_clase_ternaria(con)


def load(con: duckdb.DuckDBPyConnection, path_final: str) -> None:
    logger.info("Export final dataset %s", path_final)
    con.sql(
        f"""
        COPY competencia_03
        TO '{path_final}' (FORMAT PARQUET);
        """
    )


def get_dataframe(con: duckdb.DuckDBPyConnection, where_clause: str) -> pd.DataFrame:
    df = con.sql(
        f"""
        SELECT
            *
        FROM competencia_03
        WHERE foto_mes IN({where_clause})
        """
    ).to_df()

    return df


def create_adversarial_data(con: duckdb.DuckDBPyConnection, where_clauses: dict) -> pd.DataFrame:
    df = con.sql(
        f"""
        SELECT
            *
        FROM competencia_03
        WHERE {where_clauses['adversarial']} 
        """
    ).to_df()

    return df


def create_clase_ternaria(con: duckdb.DuckDBPyConnection) -> None:
    for month in MONTHS_INFERENCE:
        logger.info("Creating ranks")
        con.sql(
            f"""
                CREATE OR REPLACE TABLE competencia_03_temp_clase AS (
                    SELECT
                        foto_mes,
                        numero_de_cliente
                    FROM competencia_03
                    WHERE foto_mes <= {month}
                );
                """
        )
        con.sql(
            """
                CREATE OR REPLACE TABLE competencia_03_temp_clase AS (
                    SELECT
                        *,
                        RANK() OVER (PARTITION BY numero_de_cliente ORDER BY foto_mes DESC) AS rank_foto_mes,
                    FROM competencia_03_temp_clase
                );
                """
        )

        con.sql(
            """
                CREATE OR REPLACE TABLE competencia_03_temp_clase AS (
                    SELECT
                        *,
                        rank_foto_mes*-1 + 1 AS rank_foto_mes_2
                    FROM competencia_03_temp_clase
                );
                """
        )
        logger.info("Creating ternaria")
        con.sql(
            f"""
            CREATE OR REPLACE TABLE competencia_03_temp_clase AS (
                SELECT
                    *,
                    CASE
                        WHEN rank_foto_mes_2 = 0 THEN 'BAJA+1'
                        WHEN rank_foto_mes_2 =-1 THEN 'BAJA+2'
                        ELSE 'CONTINUA'
                    END AS clase_ternaria_{month}
                FROM competencia_03_temp_clase
            );
            """
        )

        logger.info("Drop ranks")
        con.sql(
            """
            ALTER TABLE competencia_03_temp_clase DROP COLUMN rank_foto_mes;
            ALTER TABLE competencia_03_temp_clase DROP COLUMN rank_foto_mes_2;
            """
        )

        logger.info("Joining")
        con.sql(
            f"""
            CREATE OR REPLACE TABLE competencia_03 AS (
                SELECT
                    c.*,
                    t.clase_ternaria_{month}
                FROM competencia_03 AS c
                LEFT JOIN competencia_03_temp_clase AS t
                ON c.foto_mes = t.foto_mes AND c.numero_de_cliente = t.numero_de_cliente
            );
            """
        )


def create_lags(con: duckdb.DuckDBPyConnection) -> None:
    logger.info("Creating lags")
    for i in LAG_FILES:
        with open(i) as f:
            query = f.read()
        logger.info("Creating %s", i)
        con.sql(
            f"""
            CREATE OR REPLACE TABLE experimentos_colaborativos AS (
                {query}
            );
            """
        )
