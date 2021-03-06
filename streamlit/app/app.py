import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
from utils import get_image

st.set_page_config(layout="wide")


psql_col, mysql_col = st.columns(2)
mysql_logo = get_image("./images/MySQL-Logo.png")
psql_logo = get_image("./images/PostgresLogo.png")


def get_data(sql, conn_type):

    if conn_type == "psql":
        conn_str = "postgresql://henry:henry@host.docker.internal:5438/henry"
    elif conn_type == "mysql":
        conn_str = "mysql+mysqlconnector://henry:henry@host.docker.internal:3307/henry"  # noqa: E501
    engine = create_engine(conn_str, echo=True)
    df = pd.read_sql(sql, engine)
    return df


def get_table_status(conn_type):
    try:
        sql = "SELECT * FROM stocks"
        get_data(sql, conn_type)
        return "✅"
    except Exception as e:
        st.write(e)
        return "❌"


def get_row_counts(conn_type):
    sql = "SELECT count(*) as row_count FROM stocks"
    df = get_data(sql, conn_type)
    return df.row_count.values[0]


def get_sample_data(conn_type):
    sql = "SELECT * FROM stocks limit 10"
    df = get_data(sql, conn_type)
    if len(df) > 0:
        return df
    else:
        return pd.DataFrame()


def get_table(db):
    result = pd.DataFrame()
    st.markdown("***")
    status = get_table_status(db)
    row_count = get_row_counts(db)
    st.subheader("Table Status: {}".format(status))
    st.subheader("Row Counts: {}".format(row_count))
    st.subheader("Sample Data")
    df = get_sample_data(db)
    if len(df) > 0:
        result = st.table(df.sample(10).round())
    return result


with psql_col:
    db = "psql"
    st.header(db.upper())
    st.image(psql_logo)
    get_table(db)

with mysql_col:
    db = "mysql"
    st.header(db.upper())
    st.image(mysql_logo)
    get_table(db)
