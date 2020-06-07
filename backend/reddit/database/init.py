from reddit.extensions import db


def create_tables():
    with db as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Users (
                Id VARCHAR(36) PRIMARY KEY,
                UserName VARCHAR(256),
                Password VARCHAR(256)
            );
            """, []
        )
