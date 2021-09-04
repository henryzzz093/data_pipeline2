import datetime
import os

import airflow

from data_pipelines.actions.core import (
    CSVToCSV,
    CSVToJsonl,
    CSVToPostgres,
    TextToText,
)
from data_pipelines.airflow.operator import ActionOperator

dag = airflow.DAG(
    dag_id="pipelines",
    start_date=datetime.datetime(2021, 6, 30),
    end_date=datetime.datetime(2021, 7, 30),
    schedule_interval="@daily",
)

pipelines = ["csv-to-csv", "text-to-text", "csv-to-jsonl", "csv-to-postgres"]

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
                "port": "5432",
                "username": os.getenv("PG_USERNAME"),
                "password": os.getenv("PG_PASSWORD"),
                "database": "test",
                "schema": "test",
                "table": "csv",
            }
            action_class = CSVToPostgres

        run_pipeline = ActionOperator(
            action_class=action_class, dag=dag, **kwargs
        )

    run_pipeline
