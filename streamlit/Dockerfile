FROM python:latest

WORKDIR /app

COPY streamlit/requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]



