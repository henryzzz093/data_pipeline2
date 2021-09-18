import datetime
import os

import airflow

from data_pipelines.actions.core import (
    CSVToCSV,
    CSVToJsonl,
    CSVToPostgres,
    TextToText,
    CSVTOMySQL,
)

from data_pipelines.actions.aws import CSVToS3

from data_pipelines.airflow.operator import ActionOperator

dag = airflow.DAG(
    dag_id="pipelines",
    start_date=datetime.datetime(2021, 6, 30),
    end_date=datetime.datetime(2021, 7, 30),
    schedule_interval="@daily",
)

pipelines = ["csv-to-csv", "text-to-text", "csv-to-jsonl", "csv-to-postgres", "csv-to-MySQL", "csv-to-s3"]

with dag:
    for pipeline in pipelines:
        kwargs = {
            "task_id": f"execute_{pipeline}",
            "sink_kwargs": {"is_source": False},
        }

        if pipeline == "csv-to-csv":
            kwargs["source_kwargs"] = {"date": "{{ ds }}"}
            action_class = CSVToCSV

        if pipeline == "text-to-text":
            action_class = TextToText

        if pipeline == "csv-to-jsonl":
            kwargs["source_kwargs"] = {"date": "{{ ds }}"}
            action_class = CSVToJsonl

        if pipeline == "csv-to-postgres":
            kwargs["source_kwargs"] = {"date": "{{ ds }}"}
            kwargs["sink_kwargs"] = {
                "host": "host.docker.internal",
                "port": "5438",
                "username": os.getenv("PG_USERNAME"),
                "password": os.getenv("PG_PASSWORD"),
                "database": os.getenv("PG_DATABASE"),
                "schema": os.getenv("PG_SCHEMA"),
                "table": "stocks",
            }
            action_class = CSVToPostgres

        if pipeline == "csv-to-MySQL":
            kwargs['source_kwargs'] = {"date": "{{ ds }}"}  # airflow macros, {{ ds }}: the execution date as YYYY-MM-DD
            kwargs['sink_kwargs'] = {
                "host": "host.docker.internal",
                "port": "3307",
                "username": os.getenv("MYSQL_USERNAME"),
                "password": os.getenv("MYSQL_PASSWORD"),
                "database": os.getenv("MYSQL_DATABASE"),
                "schema": os.getenv("MYSQL_SCHEMA"),
                "table": "stocks",
            }
            action_class = CSVTOMySQL

        if pipeline == 'csv-to-s3':
            kwargs['source_kwargs'] = {"date": "{{ ds }}"} 
            kwargs['sink_kwargs'] = {
                'AWS_ACCESS_KEY': os.getenv('AWS_ACCESS_KEY'),
                'AWS_SECRET_KEY': os.getenv('AWS_SECRET_KEY'),
                's3_bucket': 'test-bucket-henry-093',
                's3_key':'data-pipelines-2/{{ ds_nodash }}/data.json',
            }
            action_class = CSVToS3


        run_pipeline = ActionOperator(
            action_class=action_class, dag=dag, **kwargs
        )

    run_pipeline
