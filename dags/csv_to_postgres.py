import datetime

import os

import airflow

from data_pipelines.actions.core import CSVToPostgres

from data_pipelines.airflow.operator import ActionOperator

data_dir = os.path.dirname(os.path.abspath(__file__)).replace(
    "dags", "data_pipelines/data"
)

dag = airflow.DAG(
    dag_id="pipeline.csv_to_postgres",
    start_date=datetime.datetime(2021, 10, 1),
    schedule_interval="@once",
)

with dag:
    source_kwargs = {
        "filepath": data_dir + "/input/raw_data.csv",
        "file_permission": "r",
    }

    sink_kwargs = {
        "host": "host.docker.internal",
        "port": "5438",
        "username": os.getenv("PG_USERNAME"),
        "password": os.getenv("PG_PASSWORD"),
        "database": os.getenv("PG_DATABASE"),
        "schema": "henry",
        "table": "stocks",
    }

    kwargs = {
        "task_id": "run-pipeline",
        "source_kwargs": source_kwargs,
        "sink_kwargs": sink_kwargs,
    }

    run_pipeline = ActionOperator(
        action_class=CSVToPostgres, dag=dag, **kwargs
    )

    run_pipeline
