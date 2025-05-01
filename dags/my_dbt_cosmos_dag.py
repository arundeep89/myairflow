"""
### Run a dbt Core project as a task group with Cosmos

Simple DAG showing how to run a dbt project as a task group, using
an Airflow connection and injecting a variable into the dbt project.
"""

from airflow.decorators import dag
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig

# adjust for other database types
from cosmos.profiles import PostgresUserPasswordProfileMapping
from pendulum import datetime

CONNECTION_ID = "my_postgres"
DB_NAME = "postgres"
SCHEMA_NAME = "public"
# The path to the dbt project
DBT_PROJECT_PATH = "/opt/airflow/dbt_example"
# The path where Cosmos will find the dbt executable
# in the virtual environment created in the Dockerfile
DBT_EXECUTABLE_PATH = "/dbt_venv/bin/dbt"

profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id=CONNECTION_ID,
        profile_args={"schema": SCHEMA_NAME, "database": DB_NAME},
    )
)

execution_config = ExecutionConfig(
    dbt_executable_path=DBT_EXECUTABLE_PATH,
)


@dag(
    start_date=datetime(2025, 4, 21),
    schedule=None,
    catchup=False
)
def my_dbt_cosmos_dag():
    transform_data = DbtTaskGroup(
        group_id="transform_data",
        project_config=ProjectConfig(DBT_PROJECT_PATH),
        profile_config=profile_config,
        execution_config=execution_config,
        default_args={"retries": 2},
    )

    transform_data


my_dbt_cosmos_dag()