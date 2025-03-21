from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from great_expectations_provider.operators.great_expectations import (
    GreatExpectationsOperator,
)
from datetime import datetime


with DAG(
    dag_id="my_dag",
    start_date = datetime(2025, 2, 1),
    schedule_interval="@once",
    catchup=False
) as dag:
    
    drop_table = SQLExecuteQueryOperator(
        task_id="drop_table",
        conn_id="my_postgres",
        sql="DROP TABLE IF EXISTS customer"
    )
    
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

    validate = GreatExpectationsOperator(
        task_id = "gx_validate",
        conn_id = 'my_postgres',
        data_context_root_dir="include/gx",
        data_asset_name="postgres.customer",
        expectation_suite_name="strawberry_suite",
        return_json_dict=True,
    )

    drop_table >> create_table >> load_table >> validate