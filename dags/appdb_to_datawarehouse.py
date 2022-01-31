import datetime

import os

import airflow

from data_pipelines.actions.aws import AppDataBaseToS3, S3ToDatawarehouse

from data_pipelines.airflow.operator import ActionOperator

table_list = ["customers", "transactions", "transaction_details"]


dag = airflow.DAG(
    dag_id="pipeline.appdb_to_datawarehouse",
    start_date=datetime.datetime(2022, 1, 10),
    schedule_interval="@daily",
)

with dag:
    for table in table_list:
        extract_source_kwargs = {
            "url": "http://host.docker.internal:5000",
            "params": {"date": "{{ ds }}", "table_name": table},
        }

        extract_sink_kwargs = {
            "aws_access_key_id": os.getenv("AWS_ACCESS_KEY"),
            "aws_secret_key_id": os.getenv("AWS_SECRET_KEY"),
            "s3_key": f"{{{{ ds }}}}/{table}/data.json",
            "s3_bucket": "data-pipeline-datalake-henry",
        }

        extract_kwargs = {
            "task_id": "extract_{}".format(table),
            "source_kwargs": extract_source_kwargs,
            "sink_kwargs": extract_sink_kwargs,
        }

        extract = ActionOperator(
            action_class=AppDataBaseToS3, dag=dag, **extract_kwargs
        )

        hosts = [
            "host.docker.internal",
            "henry.co6ljk0rbymi.us-west-2.rds.amazonaws.com",
        ]

        load_tasks = []

        names = ["local", "remote"]

        for host, name in zip(hosts, names):

            if name == "local":
                port = "5438"
            else:
                port = "5432"

            load_source_kwargs = {
                "aws_access_key_id": os.getenv("AWS_ACCESS_KEY"),
                "aws_secret_key_id": os.getenv("AWS_SECRET_KEY"),
                "s3_key": f"{{{{ ds }}}}/{table}/data.json",
                "s3_bucket": "data-pipeline-datalake-henry",
            }

            load_sink_kwargs = {
                "host": host,
                "port": port,
                "username": "henry",
                "password": "henry123",
                "database": "henry",
                "table": table,
                "schema": "henry",
            }

            load_kwargs = {
                "task_id": "load_{}_{}".format(table, name),
                "source_kwargs": load_source_kwargs,
                "sink_kwargs": load_sink_kwargs,
            }

            load = ActionOperator(
                action_class=S3ToDatawarehouse, dag=dag, **load_kwargs
            )
            load_tasks.append(load)

        extract >> load_tasks
