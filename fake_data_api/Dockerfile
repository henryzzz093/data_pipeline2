FROM python:latest

# set python check, appending directory to that path
ENV PYTHONPATH "${PYTHONPATH}:/database/"


# create a new folder and set the path to '/api'
WORKDIR /api
COPY fake_data_api/requirement.txt .
RUN pip install -r requirement.txt

ENTRYPOINT ["python3", "api.py"]