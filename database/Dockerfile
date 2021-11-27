FROM python:3.9

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/database/"

COPY database/requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3"]
CMD [ "database/db_setup.py" ]