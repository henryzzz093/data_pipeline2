import sqlalchemy as db
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class stocks(Base):
    __tablename__ = "stocks"
    __table_args__ = {"schema": "henry"}

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DATE)
    open = db.Column(db.Numeric)
    high = db.Column(db.Numeric)
    low = db.Column(db.Numeric)
    close = db.Column(db.Numeric)
    adj_close = db.Column(db.Numeric)
    volume = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, server_default=func.now())


dbapi = "mysql+pymysql"
username = "henry"
password = "henry"
host = "host.docker.internal"
port = "3307"
database = "henry"

connection_string = f"{dbapi}://{username}:{password}@{host}:{port}/{database}"


if __name__ == "__main__":
    engine = db.create_engine(connection_string, echo=True)
    Base.metadata.create_all(engine)
