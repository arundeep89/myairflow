from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime


with DAG(
    dag_id="my_dag",
    start_date = datetime(2025, 2, 1),
    schedule_interval="@once",
    catchup=False
) as dag:
    
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="my_postgres",
        sql="sql/create.sql"
    )

    load_table = SQLExecuteQueryOperator(
        task_id="load_table",
        conn_id="my_postgres",
        sql="sql/load.sql"
    )

    create_table