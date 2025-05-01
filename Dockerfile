FROM apache/airflow:2.10.5

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

USER root
RUN apt-get update
RUN apt-get install sudo

USER airflow
RUN airflow db init
RUN airflow db upgrade

RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-postgres && deactivate