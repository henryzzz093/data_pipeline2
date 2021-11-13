FROM python:3.9
WORKDIR /scripts
COPY database/mysql/requirement.txt .
RUN pip install -r requirement.txt

