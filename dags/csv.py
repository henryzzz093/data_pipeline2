# airflow DAG
import datetime

import airflow

from data_pipelines.actions.core import CSVToCSV, CSVToText
from data_pipelines.airflow.operator import ActionOperator

dag = airflow.DAG(
    dag_id="csv-to-text",
    start_date=datetime.datetime(2021, 6, 30),
    end_date=datetime.datetime(2021, 7, 30),
    schedule_interval="@daily",
)

# dag2 = airflow.DAG(
#     dag_id = 'csv-to-text',
#     start_date=datetime.datetime(2021, 6, 30),
#     end_date=datetime.datetime(2021, 7, 30),
#     schedule_interval="@daily",
# )

kwargs = {
    "task_id": "execute_pipeline",
    "source_kwargs": {"date": "{{ ds}}"},
    "sink_kwargs": {"is_source": False},
}

with dag:
    task1 = ActionOperator(action_class=CSVToText, dag=dag, **kwargs)
    # task2 = ActionOperator(action_class=CSVToText, dag=dag2, **kwargs)
    task1
    # task2
