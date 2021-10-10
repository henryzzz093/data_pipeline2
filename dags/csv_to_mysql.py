import datetime

import os

import airflow

from data_pipelines.actions.core import CSVTOMySQL

from data_pipelines.airflow.operator import ActionOperator

data_dir = os.path.dirname(os.path.abspath(__file__)).replace(
    "dags", "data_pipelines/data"
)

dag = airflow.DAG(
    dag_id="pipeline.csv_to_mysql",
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
        "port": "3307",
        "username": os.getenv("MYSQL_USERNAME"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DATABASE"),
        "schema": "henry",
        "table": "stocks",
    }

    kwargs = {
        "task_id": "run-pipeline",
        "source_kwargs": source_kwargs,
        "sink_kwargs": sink_kwargs,
    }

    run_pipeline = ActionOperator(action_class=CSVTOMySQL, dag=dag, **kwargs)

    run_pipeline
