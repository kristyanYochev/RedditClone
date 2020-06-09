from reddit.extensions import db
from typing import List


class Subreddit:
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def search(query: str) -> List['Subreddit']:
        with db as cursor:
            cursor.execute(
                "SELECT Name FROM Subreddits WHERE Name LIKE '%' || ? || '%'",
                (query,)
            )

            rows = cursor.fetchall()

            return list(map(lambda x: Subreddit(x[0]), rows))

    def addToDb(self):
        with db as cursor:
            cursor.execute(
                "INSERT INTO Subreddits (Name) VALUES (?)",
                (self.name,)
            )

    def delete(self):
        with db as cursor:
            cursor.execute(
                "DELETE FROM Subreddits WHERE Name = ?",
                (self.name,)
            )

    def toJSON(self):
        return {
            "name": self.name
        }
