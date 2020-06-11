from reddit.extensions import db
from typing import Optional


class Comment:
    def __init__(self, cid: Optional[int] = None):
        self.id = cid

    @staticmethod
    def add(content: str, postid: int, authorid: int, parentid: int):
        with db as cursor:
            cursor.execute(
                """
                INSERT INTO Posts (Content, PostId, AuthorId, ParentId)
                VALUES (?, ?, ?, ?);""",
                (
                    content,
                    postid,
                    authorid,
                    parentid
                )
            )

    def delete(self):
        with db as cursor:
            cursor.execute(
                "DELETE FROM Comments WHERE Id = ?;", (self.id)
            )

    def edit(self, content: str):
        with db as cursor:
            cursor.execute(
                "UPDATE Comments SET Content = ?;", (content)
            )
