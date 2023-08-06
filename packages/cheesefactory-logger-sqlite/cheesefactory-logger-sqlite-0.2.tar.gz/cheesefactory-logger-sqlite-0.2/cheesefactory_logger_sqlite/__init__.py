# __init__.py

import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from .exceptions import MissingTableError
from .model import CfLogSqliteModel

logger = logging.getLogger(__name__)


class CfLogSqlite(CfLogSqliteModel):
    """Send logs to and read logs from a SQLite database."""
    def __init__(self):
        super().__init__()
        # Default log table design.
        self.field_list = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'message': 'TEXT',
            'timestamp': 'TEXT DEFAULT CURRENT_TIMESTAMP',
        }

    #
    # CLASS METHODS
    #

    @classmethod
    def connect(cls, database_path: str, create: bool = False, field_list: dict = None):
        """Make a SQLite connection to a database file.

        If the database file exists, use it. If not, create it. If the file exists, but the table fields do not match,
        create a new file.

        Args:
            database_path: Directory and filename of database.
            create: Create the database file if it does not exist?
            field_list:
        """
        log = cls()
        log.database_path = database_path
        log.field_list = field_list

        logger.debug(f'Connecting to log: {log.database_path}')
        log._connect(database_path=log.database_path, create=create)

        try:
            logger.debug(f'Testing log: {log.database_path}')
            log._test_database()

        except MissingTableError as e:
            logger.debug(f'Missing table: {str(e)}')
            log._create_table()

        except sqlite3.Error as e:
            logger.debug(f'Problems found. Archiving and recreating log: {log.database_path}\n{str(e)}')
            log.archive()
            log._connect()
            log._create_table()

        log._test_database()
        logger.debug(f'Connected to log database: {log.database_path}')

        return log

    #
    # PUBLIC METHODS
    #

    def archive(self) -> str:
        """Close any existing connection and move the database.

        Archived database files are appended with the date of rotation.

        Returns:
            New file name.
        """
        append_date = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')
        new_path = f'{self.database_path}.{append_date}'
        self.move_log(new_path)
        return new_path

    def move_log(self, new_path: str = None):
        """Close any existing connection and move the database.

        Args:
            new_path: New filename for database.
        """
        if new_path is None:
            raise ValueError('No new_path defined. Nothing to move to!')
        if self.database_path is None:
            raise ValueError('No database_path defined.')

        self.close()  # Kill connection, if it exists.
        Path(self.database_path).rename(new_path)

        if not Path(new_path).exists():
            raise FileNotFoundError(f'Could not create new file when renaming: {self.database_path} -> {new_path}')
        if Path(self.database_path).exists():
            raise FileExistsError(f'New file created, but old file still exists: '
                                  f'{self.database_path} -> {new_path}')

        logger.debug(f'Database file name changed: {self.database_path} -> {new_path}')
