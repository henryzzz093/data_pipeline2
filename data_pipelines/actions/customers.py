from data_pipelines.actions.core import SourceToSink
from data_pipelines.connections.core import PostgresConn, MySQLConn, HTTPConn


class CustomersToMySQL(SourceToSink):
    source_class = HTTPConn
    sink_class = MySQLConn


class CustomersToPostgres(SourceToSink):
    source_class = HTTPConn
    sink_class = PostgresConn
