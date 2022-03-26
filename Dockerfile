FROM ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.2.0-python3.7}

USER airflow

ENV PYTHONPATH "${PYTHONPATH}:/data_pipelines/"   

# change the owner of the folder airflow to the user airflow, also copy poetry.lock, pyproj.. to airflow directory
COPY --chown=airflow:airflow poetry.lock pyproject.toml ./ 

# use poetry as the package dependency manager
RUN pip install poetry

# do not create a virtual env, beacause we are running it inside a containers...
RUN poetry config virtualenvs.create false --local

# --no-dev flag, only install the tool.poetry.dependencies...not the dev part
RUN poetry install --no-dev
