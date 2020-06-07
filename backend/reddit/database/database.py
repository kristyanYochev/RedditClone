import sqlite3
from types import TracebackType
from typing import Optional, Type


class Database:
    def __init__(self, db_file_path: str):
        self.database = sqlite3.connect(db_file_path)

    def __enter__(self) -> sqlite3.Cursor:
        cursor = self.database.cursor()
        return cursor

    def __exit__(self,
                 exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        if exc_type is None:
            self.database.commit()
        else:
            self.database.rollback()
