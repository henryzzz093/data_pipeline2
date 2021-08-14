FROM ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.1.2}
COPY setup.py setup.py
RUN pip install -e .