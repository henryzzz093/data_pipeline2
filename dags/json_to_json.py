import datetime

import os

import airflow

from data_pipelines.actions.core import JsonToJson

from data_pipelines.airflow.operator import ActionOperator

data_dir = os.path.dirname(os.path.abspath(__file__)).replace('dags', 'data_pipelines/data')

dag = airflow.DAG(
    dag_id = 'pipeline.json_to_json',
    start_date = datetime.datetime(2021, 10, 1),
    schedule_interval='@once'
)

with dag:
    source_kwargs = {
        'filepath': data_dir + '/input/raw_data.json',
        'file_permission': 'r',
    }

    sink_kwargs = {
        'filepath': data_dir + '/output/output_data2.json',
        'file_permission': 'w',
    }

    kwargs = {
        'task_id': 'run-pipeline',
        'source_kwargs': source_kwargs,
        'sink_kwargs': sink_kwargs
    }

    run_pipeline = ActionOperator(
        action_class = JsonToJson, dag = dag, **kwargs
    )

    run_pipeline