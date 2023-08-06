#  Copyright (c) 2020. Sinri Edogawa
from typing import Iterable

import pymysql
from pymysql.cursors import SSCursor, SSDictCursor

from nehushtan.mysql import constant
from nehushtan.mysql.MySQLCondition import MySQLCondition
from nehushtan.mysql.MySQLQueryResult import MySQLQueryResult
from nehushtan.mysql.MySQLTableExistence import MySQLTableExistence


class MySQLTableSelection:
    # _model: MySQLTableExistence
    # _select_fields: list
    # _conditions: list
    # _group_by_fields: list
    # _sort_expression: str
    # _limit: int
    # _offset: int
    # _use_indices: list
    # _force_indices: list
    # _ignore_indices: list
    # _for_update: bool

    def __init__(self, model: MySQLTableExistence):
        self._model = model
        self._select_fields = []
        self._conditions = []
        self._group_by_fields = []
        self._sort_expression = ''
        self._limit = 0
        self._offset = 0
        self._use_indices = []
        self._force_indices = []
        self._ignore_indices = []
        self._for_update = False

    def get_limit(self) -> int:
        return self._limit

    def set_limit(self, limit: int):
        self._limit = limit
        return self

    def get_offset(self) -> int:
        return self._offset

    def set_offset(self, offset: int):
        self._offset = offset
        return self

    def get_sort_expression(self):
        return self._sort_expression

    def set_sort_expression(self, sort_expression: str):
        self._sort_expression = sort_expression
        return self

    def add_select_field(self, field_expression: str, alias: str = ''):
        s = field_expression
        if len(alias) > 0:
            s += f' as {alias}'
        self._select_fields.append(s)
        return self

    def add_select_field_name_list(self, field_name_array: Iterable[str]):
        """

        :param field_name_array: ["F1","F2", ...] or ("F1","F2", ...)
        :return:
        """
        for item in field_name_array:
            self._select_fields.append(item)
        return self

    def add_condition(self, condition: MySQLCondition):
        self._conditions.append(condition)
        return self

    def add_conditions(self, conditions: Iterable[MySQLCondition]):
        """

        :param conditions: array of MySQLCondition
        :return:
        """
        for condition in conditions:
            if isinstance(condition, MySQLCondition):
                self._conditions.append(condition)
            # else just ignore
        return self

    def add_simple_conditions(self, equal_dict: dict):
        """

        :param equal_dict: {FIELD:VALUE,FIELD:VALUE_ARRAY}
        :return:
        """
        for k, v in equal_dict.items():
            if isinstance(v, (tuple, list)):
                self.add_condition(MySQLCondition.make_in_array(k, v))
            else:
                self.add_condition(MySQLCondition.make_equal(k, v))
        return self

    def set_group_by_fields(self, group_by_fields: list):
        self._group_by_fields = group_by_fields
        return self

    def use_index(self, index: str):
        self._use_indices.append(index)
        return self

    def force_index(self, index: str):
        self._force_indices.append(index)
        return self

    def ignore_index(self, index: str):
        self._ignore_indices.append(index)
        return self

    def set_for_update(self, value: bool):
        self._for_update = value

    def generate_sql(self):
        table = self._model.get_table_expression()

        fields = "*"
        if len(self._select_fields) > 0:
            fields = ",".join(self._select_fields)

        condition_sql = MySQLCondition.build_sql_component(self._conditions)

        indices = ''
        if len(self._use_indices) > 0:
            indices += " USE INDEX (" + ",".join(self._use_indices) + ") "
        if len(self._force_indices) > 0:
            indices += " FORCE INDEX (" + ",".join(self._force_indices) + ") "
        if len(self._ignore_indices) > 0:
            indices += " IGNORE INDEX (" + ",".join(self._force_indices) + ") "

        sql = f"SELECT {fields} FROM {table} {indices} WHERE {condition_sql} "

        if len(self._group_by_fields) > 0:
            sql += "GROUP BY " + ",".join(self._group_by_fields) + " "

        if self._sort_expression.strip() != '':
            sql += "ORDER BY " + self._sort_expression + " "

        if self._limit > 0:
            sql += f"LIMIT {self._limit} "
            if self._offset > 0:
                sql += f"OFFSET {self._offset} "

        if self._for_update:
            sql += " FOR UPDATE "

        return sql

    def query_for_result_matrix(self, row_type: type):
        result = MySQLQueryResult()
        try:
            sql = self.generate_sql()
            result.set_sql(sql)
            if row_type is dict:
                matrix = self._model.get_mysql_kit().raw_query_for_all_dict_rows(sql)
            else:
                matrix = self._model.get_mysql_kit().raw_query_for_all_tuple_rows(sql)
            result.set_status(constant.MYSQL_QUERY_STATUS_QUERIED)
            result.append_result_rows(matrix)
        except pymysql.MySQLError as e:
            result.set_status(constant.MYSQL_QUERY_STATUS_ERROR)
            result.set_error(f"MySQL Error {e.__class__} [{e.args[0]}] {e.args[1]}")
        except Exception as pe:
            result.set_status(constant.MYSQL_QUERY_STATUS_ERROR)
            result.set_error(f"Python Error {pe.__class__}: {pe}")
        finally:
            return result

    def query_for_result_as_tuple_of_dict(self):
        return self.query_for_result_matrix(dict)

    def query_for_result_as_tuple_of_tuple(self):
        return self.query_for_result_matrix(tuple)

    def query_for_result_stream(self, row_type: type):
        result = MySQLQueryResult()
        try:
            sql = self.generate_sql()
            result.set_sql(sql)
            if row_type is dict:
                cursor = self._model.get_mysql_kit().get_raw_connection().cursor(SSDictCursor)
            else:
                cursor = self._model.get_mysql_kit().get_raw_connection().cursor(SSCursor)
            cursor.execute(sql)
            result.set_status(constant.MYSQL_QUERY_STATUS_STREAMING)
            result.set_stream(cursor)
            return result
        except pymysql.MySQLError as e:
            result.set_status(constant.MYSQL_QUERY_STATUS_ERROR)
            result.set_error(f"MySQL Error {e.__class__} [{e.args[0]}] {e.args[1]}")
        except Exception as pe:
            result.set_status(constant.MYSQL_QUERY_STATUS_ERROR)
            result.set_error(f"Python Error {pe.__class__}: {pe}")
        finally:
            return result

    def query_for_result_stream_as_dict(self):
        return self.query_for_result_stream(row_type=dict)

    def query_for_result_stream_as_tuple(self):
        return self.query_for_result_stream(row_type=tuple)
