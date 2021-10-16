FROM ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.1.2}
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml 
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install