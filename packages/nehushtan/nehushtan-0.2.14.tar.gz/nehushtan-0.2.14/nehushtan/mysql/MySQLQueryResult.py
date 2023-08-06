#  Copyright (c) 2020. Sinri Edogawa
import warnings
from typing import Iterable

from pymysql.cursors import Cursor

from nehushtan.mysql import constant


class MySQLQueryResult:
    # _sql: str
    # _status: str
    # _error: str

    # The beneath properties would be initialized for each instance when needed
    # _last_inserted_id: int
    # _affected_rows: int
    # _result_rows: list
    # _result_stream: Cursor  # do not know how to implement it in python now

    def __init__(self):
        self._sql = ''
        self._status = constant.MYSQL_QUERY_STATUS_INIT
        self._error = 'Not executed yet!'

        self._last_inserted_id = -1
        self._affected_rows = -1
        self._result_rows = []
        self._result_stream = None

    def is_queried(self):
        return self._status == constant.MYSQL_QUERY_STATUS_QUERIED

    def is_executed(self):
        return self._status == constant.MYSQL_QUERY_STATUS_EXECUTED

    def is_streamed(self):
        return self._status == constant.MYSQL_QUERY_STATUS_STREAMED

    def get_last_inserted_id(self):
        return self._last_inserted_id

    def set_last_inserted_id(self, last_inserted_id: int):
        self._last_inserted_id = last_inserted_id
        return self

    def get_affected_rows(self):
        return self._affected_rows

    def set_affected_rows(self, affected_rows: int):
        self._affected_rows = affected_rows
        return self

    def get_sql(self):
        return self._sql

    def set_sql(self, sql: str):
        self._sql = sql
        return self

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status
        if (
                constant.MYSQL_QUERY_STATUS_QUERIED,
                constant.MYSQL_QUERY_STATUS_STREAMING,
                constant.MYSQL_QUERY_STATUS_STREAMED,
                constant.MYSQL_QUERY_STATUS_EXECUTED,
        ).__contains__(self._status):
            self._error = 'NO ERROR'
        return self

    def get_error(self):
        return self._error

    def set_error(self, error: str):
        self._error = error
        return self

    def append_result_rows(self, rows: Iterable):
        """

        :param rows: Array (list ot tuple) of result rows, each row would be a dict or tuple
        :return:
        """
        if type(rows) is tuple:
            rows = list(rows)
        self._result_rows += rows
        return self

    def set_stream(self, cursor: Cursor):
        self._result_stream = cursor
        return self

    def get_stream(self) -> Cursor:
        if self._result_stream is None:
            raise Exception("No available stream!")
        return self._result_stream

    def read_next_row(self):
        if self._status != constant.MYSQL_QUERY_STATUS_STREAMING:
            raise Exception("Now no stream to read!")
        row = self.get_stream().fetchone()
        if row is None:
            self._status = constant.MYSQL_QUERY_STATUS_STREAMED
            self._result_stream.close()
            del self._result_stream
            return None
        return row

    def get_result(self):
        warnings.warn('Deprecated since 0.1.12. Use `get_fetched_rows_as_tuple` instead.', DeprecationWarning)
        if self._status != constant.MYSQL_QUERY_STATUS_QUERIED:
            raise Exception('Cannot fetch query result as status is not QUERIED.')
        return self._result_rows

    def get_fetched_rows_as_tuple(self):
        if self._status != constant.MYSQL_QUERY_STATUS_QUERIED:
            raise Exception('Cannot fetch query result as status is not QUERIED.')
        return tuple(self._result_rows)

    @staticmethod
    def create_error_result(error_message: str):
        return MySQLQueryResult().set_status(constant.MYSQL_QUERY_STATUS_ERROR).set_error(error_message)
