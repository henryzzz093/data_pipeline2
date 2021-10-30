FROM python:3.9

COPY database/mysql database/mysql

RUN pip install -r "database/mysql/requirement.txt"

CMD ["python3", "database/mysql/create_table.py"]
