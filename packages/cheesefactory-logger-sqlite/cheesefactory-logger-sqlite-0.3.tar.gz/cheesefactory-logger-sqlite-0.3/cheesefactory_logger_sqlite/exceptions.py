# exceptions.py

class Error(Exception):
    """Base class."""
    pass


class MissingTableError(Error):

    def __init__(self, table: str, database: str):
        """Exception raised when source and destination files do not match.

        Args:
            table: Missing table.
            database: Database of interest.
        """
        self.table = table
        self.database = database

    def __str__(self):
        return f'Table ({self.table}) missing in database ({self.database})'



