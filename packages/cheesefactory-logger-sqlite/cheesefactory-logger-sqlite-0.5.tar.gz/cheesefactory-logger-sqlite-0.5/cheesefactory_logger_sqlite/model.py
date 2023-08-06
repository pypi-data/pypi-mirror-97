# model.py

import logging
import sqlite3
from typing import List, Tuple
from .connection import CfLogSqliteConnection
from .exceptions import MissingTableError, TablePrimaryKeyError

logger = logging.getLogger(__name__)


class CfLogSqliteModel(CfLogSqliteConnection):
    def __init__(self):
        super().__init__()
        self.table: str = 'log'
        self.field_list: dict = {}

    #
    # PROPERTIES
    #

    @property
    def pk_field(self) -> str:
        """Find and return a table's primary key field. Because of how the table is automatically created, there can
        be only one pk.

        Return:
            A table's primary key field.
        """
        primary_keys = []
        results = self.execute(f"PRAGMA table_info('{self.table}')")
        for result in results:
            if result[5] == 1:  # This is the pk field
                primary_keys.append(result[1])  # This is the field name field
        if len(primary_keys) > 1:
            raise TablePrimaryKeyError(database=self.database_path, table=self.table,
                                       message='Table has more than 1 primary key.')
        if len(primary_keys) == 0:
            logger.debug('No primary key found.')
            return ''
        else:
            return primary_keys[0]

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

        if self.pk_field == '':
            logger.warning(f'Table ({self.table}) has no primary key. UPDATEs are not possible.')

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

    def dump_table(self, where: str = None, target_table: str = None, exclude_pk: bool = False) -> str:
        """Dumps the table into SQL INSERT statements.

        The dump will contain the columns and order provided by self.field_list. This is standard SQL that should
        work for PostgreSQL, MSSQL, and Oracle.

        Args:
            where: SQL WHERE to filter data.
            target_table: Replace the table name in the INSERT statements with this string.
            exclude_pk: Exclue the primary key in the SQL INSERTs
        Returns:
            The table rows as a SQL statement
        """
        pk_field = ''

        if len(self.field_list) == 0:
            raise ValueError('field_list cannot be empty!')

        if target_table is None:
            table = self.table
        else:
            table = target_table

        dump_prefix = f'INSERT INTO {table} ('

        # Add fields
        if exclude_pk is True:
            # No need to go through the cost of running this property multiple times in the following loop.
            pk_field = self.pk_field
        for field in self.field_list.keys():
            if exclude_pk is True and field == pk_field:
                continue
            else:
                dump_prefix = dump_prefix + f'{field}, '
        dump_prefix = dump_prefix[:-2] + ') VALUES '  # Cut off the trailing command and space from the field list

        # Add values to the statement, quoting as necessary
        # read_records() returns columns and order as defined by self.field_list
        results = self.read_records(where=where, exclude_pk=exclude_pk)
        dump = ''
        for result in results:
            dump = dump + dump_prefix + str(result) + ';\n'

        return dump

    def exists(self, where=None):
        """Does the query return results?

        Args:
            where: SQL WHERE to filter data.
        """
        result = self.read_records(where=where)
        if len(result) == 0:
            return False
        else:
            return True

    def read_records(self, where: str = None, exclude_pk: bool = False) -> List[Tuple]:
        """Produce record entries.

        Args:
            where: SQL WHERE to filter data.
            exclude_pk: Exclue the primary key in the results
        Notes:
            The SQL SELECT needs to be explicit with column names. We are going to enforce the names and
            order given in self.field_list.
        """
        field_list = ''
        pk_field = ''

        if exclude_pk is True:
            # No need to go through the cost of running this property multiple times in the following loop.
            pk_field = self.pk_field
        for field in self.field_list.keys():
            if exclude_pk is True and field == pk_field:
                continue
            field_list = field_list + f'{field}, '
        field_list = field_list[:-2]  # Remove trailing comma and space.
        sql = f'SELECT {field_list} FROM {self.table}'

        if where is not None:
            sql += f' WHERE {where}'

        logger.debug(sql)
        result = self.execute(sql)
        if result is None:
            return []
        else:
            return result

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
        field_map = field_map[:-2]  # Clean up the trailing comma and whitespaces

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
            pk_field = self.pk_field
            if pk_field == '':
                raise TablePrimaryKeyError(database=self.database_path, table=self.table,
                                           message='The table has no primary key. SQL UPDATE cannot happen.')
            logger.debug(f'Updating record. {pk_field}={str(pk)}')
            sql = f'UPDATE {self.table} SET {field_map} WHERE {pk_field} = {str(pk)};'
            logger.debug(f'write(): {sql}')
            self.execute(sql)

        return pk
