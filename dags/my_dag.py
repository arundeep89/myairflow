from airflow.decorators import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime


@dag(
    dag_id="my_dag",
    start_date = datetime(2025, 2, 1),
    schedule_interval="@once",
    catchup=False
)
def my_dag():

    @task.virtualenv(
        task_id="virtualenv_python", requirements=["great_expectations"], system_site_packages=False
    )
    def callable_virtualenv():
        import great_expectations as gx
        import pandas as pd

        context=gx.get_context(mode="ephemeral")
        data_source_name="my_dataframe"
        data_source=context.data_sources.add_pandas(name = data_source_name)

        data_asset_name="my_data_asset"
        data_asset=data_source.add_dataframe_asset(name=data_asset_name)

        batch_definition_name="my_batch_definition"
        batch_definition=data_asset.add_batch_definition_whole_dataframe(batch_definition_name)

        data_list=[
            {'VendorID':1, 'Name':'Alex'},
            {'VendorID':2, 'Name':'Junga'}
        ]

        dataframe=pd.DataFrame(data_list)

        batch_parameters={"dataframe":dataframe}

        batch_definition=(
            context.data_sources.get(data_source_name)
            .get_asset(data_asset_name)
            .get_batch_definition(batch_definition_name)
        )

        expectation=gx.expectations.ExpectColumnValuesToNotBeNull(
            column="VendorID"
        )

        batch=batch_definition.get_batch(batch_parameters=batch_parameters)
        validation_results = batch.validate(expectation)
        print(validation_results)

    drop_table = SQLExecuteQueryOperator(
        task_id="drop_table",
        conn_id="my_postgres",
        sql="sql/drop.sql"
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


    drop_table >> create_table >> load_table >> callable_virtualenv()

my_dag()
