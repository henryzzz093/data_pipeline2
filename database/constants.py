from enum import Enum


class ConnectionKwargs(Enum):
    APP_DB_LOCAL = {
        "host": "host.docker.internal",
        "port": "3307",
        "username": "henry",
        "password": "henry123",
        "database": "henry",
        "schema": "henry",
        "db_type": "mysql",
    }
    DATAWH_LOCAL = {
        "host": "host.docker.internal",
        "port": "5438",
        "username": "henry",
        "password": "henry123",
        "database": "henry",
        "schema": "henry",
        "db_type": "postgres",
    }
    DATAWH_AWS = {
        "host": "henry.co6ljk0rbymi.us-west-2.rds.amazonaws.com",
        "port": "5432",
        "username": "henry",
        "password": "henry123",
        "database": "henry",
        "schema": "henry",
        "db_type": "postgres",
    }
