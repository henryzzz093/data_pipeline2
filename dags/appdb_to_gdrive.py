import airflow
import datetime

from data_pipelines.actions.gcp import AppDataBaseToGDrive
from data_pipelines.airflow.operator import ActionOperator


dag = airflow.DAG(
    dag_id="pipline.appdb_to_gdrive",
    start_date=datetime.datetime(2022, 1, 1),
    schedule_interval="@daily",
)

table_list = ["customers", "transactions", "transaction_details"]

with dag:
    for table in table_list:
        task_id = f"execute-pipeline-{table}"
        source_kwargs = {
            "url": "http://host.docker.internal:5000",
            "params": {"date": "{{ ds }}", "table_name": table},
        }

        sink_kwargs = {
            "connection_id": "gdrive_default",
            "file_ext": "csv",
            "folder_name": "Testing1",
        }

        kwargs = {"source_kwargs": source_kwargs, "sink_kwargs": sink_kwargs}

        execute = ActionOperator(
            action_class=AppDataBaseToGDrive,
            dag=dag,
            task_id=task_id,
            **kwargs,
        )
