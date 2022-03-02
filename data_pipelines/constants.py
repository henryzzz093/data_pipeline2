from enum import Enum


class ConnectionIDs(Enum):
    AWS_DEFAULT = "aws_default"
    GOOGLE_DRIVE = "gdrive_default"
    MYSQL_DOCKER = "mysql_docker"
    MYSQL_LOCAL = "mysql_local"
    POSTGRES_DOCKER = "postgres_docker"
    POSTGRES_LOCAL = "postgres_local"
    POSTGRES_REMOTE = "postgres_remote"
