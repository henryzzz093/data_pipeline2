FROM ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.2.0-python3.7}

USER airflow

ENV PYTHONPATH "${PYTHONPATH}:/data_pipelines/"

COPY --chown=airflow:airflow poetry.lock pyproject.toml ./

RUN pip install poetry
RUN poetry config virtualenvs.create false --local
RUN poetry install --no-dev
