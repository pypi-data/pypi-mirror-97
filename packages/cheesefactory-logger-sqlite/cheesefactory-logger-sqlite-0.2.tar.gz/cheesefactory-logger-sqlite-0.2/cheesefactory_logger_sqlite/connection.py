# connection.py

import logging
import re
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)


class CfLogSqliteConnection:
    """Manage a SQLite connection."""

    def __init__(self):
        """
        Attributes:
            self._connection: SQLite connection.
            self._cursor: SQLite cursor.
            self.database_path: Path to SQLite database file.
            self.result: SQL query results.
        """
        self._connection = None
        self._cursor = None
        self.database_path = './log.sqlite'
        self.result = None

    #
    # PROPERTIES
    #

    @property
    def status(self):
        """Retrieve connection status.

        status() for cheesefactory programs should return True/False along with any reasons.

        Returns:
            True, if live. False, if not live.
            Additional info, such as error codes. (not implemented)
        """
        try:
            self._cursor.execute('SELECT sqlite_version();')
            result = self._cursor.fetchall()
            version = result[0][0]

            if re.search(r'^[0-9]+\.[0-9]+\.[0-9]+$', version):
                return True, None
        except AttributeError:
            return False, 'No connection detected.'
        except sqlite3.ProgrammingError:
            return False, 'No connection detected.'
        else:
            return False, 'No connection detected.'

    #
    # PROTECTED METHODS
    #

    def _connect(self, database_path: str = None, create: bool = True):
        """Make a SQLite connection to a database file.

        If the database file exists, use it. If not, create it. If the file exists, but the table fields do not match,
        create a new file.

        Args:
            database_path: Directory and filename of database.
            create: Create the database file if it does not exist?
        """
        if database_path is not None:
            self.database_path = database_path

        if Path(self.database_path).exists():  # A database file exists. Connect to it.
            logger.debug(f'Connecting to existing database: {self.database_path}')
            self._connection = sqlite3.connect(self.database_path)
            self._cursor = self._connection.cursor()

        else:  # Create a new database file. Make table and test.

            if create is True:
                logger.debug(f'Connecting to new database: {self.database_path}')
                self._connection = sqlite3.connect(self.database_path)
                self._cursor = self._connection.cursor()
            else:  # Database file does not exist and not allowed to create a new one. create = False
                raise FileNotFoundError(f'SQLite database does not exist: {self.database_path}')

    #
    # PUBLIC METHODS
    #

    def close(self):
        """Close the SQLite connection, if it is open."""
        if self.status[0] is True:
            self._connection.close()

    def execute(self, sql: str = None):
        self._cursor.execute(sql)
        self._connection.commit()
        self.result = self._cursor.fetchall()
