SELECT
    *
    ,LEAD(clase_ternaria, 1) OVER (PARTITION BY numero_de_cliente ORDER BY foto_mes ASC) AS clase_ternaria_202108
    ,LEAD(clase_ternaria, 2) OVER (PARTITION BY numero_de_cliente ORDER BY foto_mes ASC) AS clase_ternaria_202107
    ,LEAD(clase_ternaria, 3) OVER (PARTITION BY numero_de_cliente ORDER BY foto_mes ASC) AS clase_ternaria_202106
    ,LEAD(clase_ternaria, 4) OVER (PARTITION BY numero_de_cliente ORDER BY foto_mes ASC) AS clase_ternaria_202105
    ,LEAD(clase_ternaria, 5) OVER (PARTITION BY numero_de_cliente ORDER BY foto_mes ASC) AS clase_ternaria_202104
    ,LEAD(clase_ternaria, 6) OVER (PARTITION BY numero_de_cliente ORDER BY foto_mes ASC) AS clase_ternaria_202103
FROM competencia_03