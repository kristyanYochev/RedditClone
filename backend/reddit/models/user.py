from reddit.extensions import db
from typing import Optional
from passlib.hash import sha256_crypt as sha256


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
