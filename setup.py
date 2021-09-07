from setuptools import find_packages, setup

setup(
    name="data_pipelines",
    version="1.0.0",
    packages=find_packages(),
    include_package_date=True,
    zip_safe=False,
    install_requires=[
        "apache-airflow",
        "boto3",
        "black",
        "flake8",
        "isort",
        "interrogate",
        "jinja2",
        "pre-commit",
        "psycopg2",
        "requests",
        "python-dotenv",
        "mysql-connector-python"
    ],
)
