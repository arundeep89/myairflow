# Define the default arguments for the DAG
from airflow.decorators import dag
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 16),
    'retries': 1
}
# Create the DAG with the specified schedule interval
@dag(
    dag_id="my_dbt_dag",
    start_date = datetime(2025, 2, 1),
    schedule_interval="@once",
    catchup=False
)
def my_dag():
    project_dir='/opt/airflow/dbt_example'
    profile_dir='/opt/airflow/dbt_example/profiles'
    # Define dbt tasks using BashOperator
    task1 = BashOperator(
        task_id='dbt_task1',
        bash_command=f'dbt run --project-dir {project_dir} --profiles-dir {profile_dir}'
    )
    task2 = BashOperator(
        task_id='dbt_task2',
        bash_command=f'dbt test --project-dir {project_dir} --profiles-dir {profile_dir}'
    )
    # Set task dependencies
    task1 >> task2

my_dag()