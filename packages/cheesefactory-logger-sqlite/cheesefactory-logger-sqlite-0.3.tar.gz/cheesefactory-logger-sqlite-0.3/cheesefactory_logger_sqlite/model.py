# model.py

import logging
import sqlite3
from .connection import CfLogSqliteConnection
from .exceptions import MissingTableError

logger = logging.getLogger(__name__)


class CfLogSqliteModel(CfLogSqliteConnection):
    def __init__(self):
        super().__init__()
        self.table: str = 'log'
        self.field_list: dict = {}
        self.primary_key = 'id'

    #
    # PROTECTED METHODS
    #

    def _create_table(self):
        """Create a log table."""
        # Dynamically create SQL based on field dict.
        sql = f'CREATE TABLE {self.table} ('
        for field, field_type in self.field_list.items():
            sql += f' {field} {field_type},'
        sql = sql[:-1]  # Erase trailing comma
        sql += ');'

        logger.debug(f'Creating table ({self.table}): {sql}')
        try:
            self.execute(sql)
        except AttributeError as e:
            raise AttributeError(f'No SQLite connection exists. Connect before creating table. ({str(e)})')
        logger.debug(f'New table created: {self.table}')

    def _test_database(self):
        """Check database sanity."""
        # Does a field_list exist to compare things to?
        if self.field_list == {} or self.field_list is None:
            raise ValueError('Missing field_list.')

        # Does the log table exist in the database?
        self._cursor.execute(f"SELECT name FROM main.sqlite_master WHERE type = 'table' AND name = '{self.table}';")
        results = self._cursor.fetchall()

        if len(results) == 0:
            raise MissingTableError(table=self.table, database=self.database_path)

        # Build a list of fields present in the table
        self._cursor.execute(f"PRAGMA table_info({self.table});")
        results = self._cursor.fetchall()
        table_fields = []
        for result in results:
            table_fields.append(result[1])

        # Does the table contain all of the required fields?
        missing_fields = []
        for field in self.field_list.keys():
            if field not in table_fields:
                missing_fields.append(field)
        if len(missing_fields) > 0:
            raise sqlite3.Error(f'Table {self.table} is missing required fields: {", ".join(missing_fields)}')
        logger.debug(f'Table successfully tested: {self.table}')

    #
    # PUBLIC METHODS
    #

    # def read_records(self, days=1, where=None):
    #    """Produce all log entries X days back.
    #
    #    Args:
    #        days: How many days ago to start reading the logs from?
    #        where: SQL WHERE to filter data.
    #    """
    #    sql = f"SELECT * FROM log WHERE timestamp > datetime('now', '-{days} day', 'localtime')"
    #
    #    if where is not None:
    #        sql += ' AND {where}'
    #
    #    logger.debug(sql)
    #    self._cursor.execute(sql)
    #    results = self._cursor.fetchall()
    #    logger.debug(results)
    #    return results

    def exists(self, where=None):
        """Does the query return results?

        Args:
            where: SQL WHERE to filter data.
        """
        self.read_records(where=where)
        if len(self.result) == 0:
            return False
        else:
            return True

    def read_records(self, where=None):
        """Produce record entries.

        Args:
            where: SQL WHERE to filter data.
        """
        sql = f'SELECT * FROM {self.table}'

        if where is not None:
            sql += f' WHERE {where}'

        logger.debug(sql)
        self.execute(sql)

    def write_kwargs(self, pk=None, **kwargs) -> int:
        """Insert record into database from keyword arguments.

        Args:
            pk: Primary key. If present, performs an UPDATE on that record.
            kwargs: key-value pairs. The keys should match field names.
        Returns:
            If an INSERT was performed, returns the primary key of the affected record, else 0 is returned.
        """

        if len(kwargs) == 0:
            raise ValueError('Missing kwargs. Cannot write to database.')

        # Are all given fields present in self.field_list? If not, raise an error.
        field_map = ''  # Prep for possible UPDATE. So fields don't need to be traversed again.
        ordered_keys = ''
        ordered_values = ''
        invalid_keys = ''
        field_list = self.field_list.keys()

        for key, value in kwargs.items():
            if key not in field_list:
                invalid_keys += f'{key}, '
            if key == 'id':  # If primary key, skip
                continue
            elif isinstance(value, int):
                field_map += f'{key} = {str(value)}, '
                ordered_keys += f'{key}, '
                ordered_values += f'{str(value)}, '
            elif isinstance(value, str):
                field_map += f"{key} = '{value}', "
                ordered_keys += f'{key}, '
                ordered_values += f"'{str(value)}', "

        if invalid_keys != '':
            invalid_keys = invalid_keys[:-2]  # Clean up the trailing commas and whitespaces
            raise ValueError(f'Invalid key(s): {invalid_keys}. '
                             f'Acceptable values are {", ".join(field_list)}')

        # Determine if this is an INSERT or UPDATE
        if pk is None:  # New record. Do an INSERT.
            logger.debug(f'Inserting new record.')
            ordered_keys = ordered_keys[:-2]  # Clean up the trailing comma and whitespaces
            ordered_values = ordered_values[:-2]  # Clean up the trailing comma and whitespaces
            sql = f'INSERT INTO {self.table} ({ordered_keys}) VALUES ({ordered_values});'
            logger.debug(f'write(): {sql}')
            self.execute(sql)
            pk = self._cursor.lastrowid

        else:  # Existing record. Do an UPDATE.
            logger.debug(f'Updating record. pk={str(pk)}')
            field_map = field_map[:-2]  # Clean up the trailing comma and whitespaces
            # TODO: Auto-detect primary key?
            sql = f'UPDATE {self.table} SET {field_map} WHERE {self.primary_key} = {str(pk)};'
            logger.debug(f'write(): {sql}')
            self.execute(sql)

        return pk
