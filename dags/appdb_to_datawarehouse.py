import datetime

import airflow

from data_pipelines.actions.aws import AppDataBaseToS3, S3ToDatawarehouse

from data_pipelines.airflow.operator import ActionOperator

from data_pipelines.constants import ConnectionIDs

table_list = ["customers", "transactions", "transaction_details"]


dag = airflow.DAG(
    dag_id="pipeline.appdb_to_datawarehouse",
    start_date=datetime.datetime(2022, 3, 1),
    end_date=datetime.datetime(2022, 3, 5),
    schedule_interval="@daily",
)

with dag:
    for table in table_list:
        extract_source_kwargs = {
            "url": "http://host.docker.internal:5000",
            "params": {"date": "{{ ds }}", "table_name": table},
        }

        extract_sink_kwargs = {
            "connection_id": ConnectionIDs.AWS_DEFAULT.value,
            "s3_key": f"{{{{ ds }}}}/{table}/data.json",  # the path within S3
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

        # abstract layer to securely handle the credentials
        connection_ids = [
            ConnectionIDs.POSTGRES_DOCKER.value,  # local postgresDB
            ConnectionIDs.POSTGRES_REMOTE.value,  # AWS RDS
        ]

        load_tasks = []

        names = ["local", "remote"]

        for connection_id, name in zip(connection_ids, names):

            load_source_kwargs = {
                "connection_id": ConnectionIDs.AWS_DEFAULT.value,
                "s3_key": f"{{{{ ds }}}}/{table}/data.json",
                "s3_bucket": "data-pipeline-datalake-henry",
            }

            load_sink_kwargs = {
                "connection_id": connection_id,
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

        # the reason why we put them into a list is because be executed at the same time # noqa:E501
        extract >> load_tasks
