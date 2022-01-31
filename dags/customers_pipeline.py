# airflow DAG
import airflow
import datetime

from data_pipelines.actions.customers import (
    CustomersToPostgres,
    CustomersToMySQL,
)

from data_pipelines.airflow.operator import ActionOperator

dag = airflow.DAG(
    dag_id="customers_pipeline",
    start_date=datetime.datetime(2021, 1, 1),
    schedule_interval="@daily",
)


def get_sink(database):

    sink_kwargs = {
        "host": "host.docker.internal",
        "username": "henry",
        "password": "henry123",
        "database": "henry",
        "schema": "henry",
        "table": "customers",
    }

    if database == "postgres":
        action_class = CustomersToPostgres
        sink_kwargs["port"] = "5438"
    elif database == "mysql":
        action_class = CustomersToMySQL
        sink_kwargs["port"] = "3307"

    return sink_kwargs, action_class


with dag:
    source_kwargs = {"url": "http://fake_data_api:5000"}

    databases = ["mysql", "postgres"]

    for database in databases:

        sink_kwargs, action_class = get_sink(database=database)

        kwargs = {
            "task_id": f"customers_to_{database}",
            "source_kwargs": source_kwargs,
            "sink_kwargs": sink_kwargs,
        }

        run_pipeline = ActionOperator(
            action_class=action_class, dag=dag, **kwargs
        )
