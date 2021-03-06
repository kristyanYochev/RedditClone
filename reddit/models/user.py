from reddit.extensions import db
from typing import Optional
from passlib.hash import sha256_crypt as sha256


class UserNotFoundError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class User:
    def __init__(self, uid: Optional[int] = None):
        self.id = uid

    @staticmethod
    def register(username: str, password: str):
        with db as cursor:
            cursor.execute(
                "INSERT INTO Users (UserName, Password) VALUES (?, ?);",
                (
                    username,
                    sha256.encrypt(password)
                )
            )

    @staticmethod
    def verify(username: str, password: str) -> int:
        with db as cursor:
            cursor.execute(
                "SELECT Id, Password FROM Users WHERE Username = ?",
                (username, )
            )

            row = cursor.fetchone()

            if row is None:
                raise UserNotFoundError()

            uid = row[0]
            password_hash = row[1]

            if not sha256.verify(password, password_hash):
                raise InvalidPasswordError()

            return uid

    def subscribeToSubreddit(self, sub: str):
        with db as cursor:
            cursor.execute(
                """
                INSERT INTO UserSubredditSubscriptions (UserId, SubredditName)
                VALUES (?, ?)
                """,
                (self.id, sub)
            )

    def getSubscribedSubreddits(self):
        with db as cursor:
            cursor.execute(
                """
                SELECT SubredditName FROM UserSubredditSubscriptions
                    WHERE UserId = ?
                """,
                (self.id,)
            )

            rows = cursor.fetchall()

            return list(map(lambda row: row[0], rows))
