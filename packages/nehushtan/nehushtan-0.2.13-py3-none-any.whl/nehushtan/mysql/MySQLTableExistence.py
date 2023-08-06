#  Copyright (c) 2020. Sinri Edogawa

from abc import abstractmethod, ABC

from nehushtan.mysql.MySQLKit import MySQLKit


class MySQLTableExistence(ABC):

    def __init__(self):
        # Must initialize `_mysql_kit` in overriding method here
        self._mysql_kit = None
        pass

    @abstractmethod
    def get_mysql_kit(self) -> MySQLKit:
        pass
        # if self._mysql_kit is None:
        #     raise Exception("MySQLKit is not available for querying...")
        # return self._mysql_kit

    @abstractmethod
    def mapping_table_name(self) -> str:
        pass

    @abstractmethod
    def mapping_schema_name(self) -> str:
        pass

    def get_table_expression(self) -> str:
        e = ''
        if self.mapping_schema_name() != '':
            e += f'`{self.mapping_schema_name()}`.'
        e += f'`{self.mapping_table_name()}`'
        return e
