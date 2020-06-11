import sqlite3
from types import TracebackType
from typing import Optional, Type


class Database:
    def __init__(self, db_file_path: str):
        self.db_file_path = db_file_path

    def __enter__(self) -> sqlite3.Cursor:
        self.database = sqlite3.connect(self.db_file_path)
        cursor = self.database.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        return cursor

    def __exit__(self,
                 exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        if exc_type is None:
            self.database.commit()
        else:
            self.database.rollback()
        self.database.close()
