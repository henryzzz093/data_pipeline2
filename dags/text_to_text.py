import datetime

import os

import airflow

from data_pipelines.actions.core import TextToText

from data_pipelines.airflow.operator import ActionOperator

data_dir = os.path.dirname(os.path.abspath(__file__)).replace(
    "dags", "data_pipelines/data"
)

dag = airflow.DAG(
    dag_id="pipeline.text_to_text",
    start_date=datetime.datetime(2021, 10, 1),
    schedule_interval="@once",
)

with dag:
    source_kwargs = {
        "filepath": data_dir + "/input/raw_data.txt",
        "file_permission": "r",
    }

    sink_kwargs = {
        "filepath": data_dir + "/output/output_data.txt",
        "file_permission": "w",
    }

    kwargs = {
        "task_id": "run-pipeline",
        "source_kwargs": source_kwargs,
        "sink_kwargs": sink_kwargs,
    }

    run_pipeline = ActionOperator(action_class=TextToText, dag=dag, **kwargs)

    run_pipeline
