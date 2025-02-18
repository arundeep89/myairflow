FROM apache/airflow:latest

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

USER root
RUN apt-get update
RUN apt-get install sudo

USER airflow
RUN airflow db init
RUN airflow db upgrade