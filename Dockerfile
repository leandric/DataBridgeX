FROM apache/airflow:3.0.2 AS base

COPY --chown=airflow:root ./dags /opt/airflow/dags
COPY --chown=airflow:root ./conf /opt/airflow/conf
COPY --chown=airflow:root ./data /opt/airflow/data
COPY --chown=airflow:root ./config /opt/airflow/config
COPY ./requirements.txt /

RUN pip install --no-cache-dir "apache-airflow==3.0.2" -r /requirements.txt