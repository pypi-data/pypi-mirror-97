from contextlib import contextmanager

from dataclasses import dataclass

import dbt.exceptions
from dbt.adapters.base import Credentials
from dbt.contracts.connection import AdapterResponse
from dbt.contracts.connection import Connection
from dbt.adapters.sql import SQLConnectionManager
from dbt.logger import GLOBAL_LOGGER as logger

import ibm_db
import ibm_db_dbi

@dataclass
class IBMDB2Credentials(Credentials):
    host: str
    database: str
    schema: str
    username: str
    password: str
    port: int = 50000
    protocol: str = 'TCPIP'

    @property
    def type(self):
        return 'ibmdb2'

    def _connection_keys(self):
        return ('database', 'schema', 'host', 'port', 'protocol', 'username', 'password')


class IBMDB2ConnectionManager(SQLConnectionManager):
    TYPE = 'ibmdb2'

    @contextmanager
    def exception_handler(self, sql: str):
        try:
            yield
        except ibm_db_dbi.DatabaseError as exc:
            self.release()
            logger.debug('ibm_db_dbi error: {}'.format(str(exc)))
            logger.debug("Error running SQL: {}".format(sql))
            raise dbt.exceptions.DatabaseException(str(exc))
        except Exception as exc:
            self.release()
            logger.debug("Error running SQL: {}".format(sql))
            logger.debug("Rolling back transaction.")
            raise dbt.exceptions.RuntimeException(str(exc))

    @classmethod
    def open(cls, connection):
        if connection.state == 'open':
            logger.debug('Connection is already open, skipping open.')
            return connection

        credentials = connection.credentials

        try:
            con_str = f"DATABASE={credentials.database}"
            con_str += f";HOSTNAME={credentials.host}"
            con_str += f";PORT={credentials.port}"
            con_str += f";PROTOCOL={credentials.protocol}"
            con_str += f";UID={credentials.username}"
            con_str += f";PWD={credentials.password}"

            handle = ibm_db_dbi.connect(con_str, '', '')

            connection.state = 'open'
            connection.handle = handle

        except Exception as exc:
            connection.state = 'fail'
            connection.handle = None
            logger.debug("Error connecting to database: {}".format(str(exc)))
            raise dbt.exceptions.FailedToConnectException(str(exc))

        return connection

    @classmethod
    def cancel(self, connection):
        connection_name = connection.name

        logger.info("Cancelling query '{}' ".format(connection_name))

        try:
            connection.handle.close()
        except Exception as e:
            logger.error('Error closing connection for cancel request')
            raise Exception(str(e))

    @classmethod
    def get_credentials(cls, credentials):
        return credentials

    @classmethod
    def get_response(cls, cursor) -> AdapterResponse:

        message = 'OK'
        rows = cursor.rowcount

        return AdapterResponse(
            _message=message,
            rows_affected=rows
        )

    def add_begin_query(self):
        connection = self.get_thread_connection()
        cursor = connection.handle.cursor
        return connection, cursor
