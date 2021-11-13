FROM python:latest

WORKDIR /api
COPY fake_data_api/requirement.txt .
RUN pip install -r requirement.txt

ENTRYPOINT ["python3"]
CMD ["api.py"]