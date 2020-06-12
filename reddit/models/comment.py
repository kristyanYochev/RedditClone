from reddit.extensions import db
from typing import Optional

class PermissionError(Exception):
    pass

class Comment:
    def __init__(self, cid: Optional[int] = None):
        self.id = cid
        self.content = None

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

    def delete(self, userId: int):
        with db as cursor:
            cursor.execute(
                "DELETE FROM Comments WHERE Id = ? AND AuthorId = ?;", (self.id, userId)
            )
            if cursor.rowcount == 0:
                raise PermissionError()

    def edit(self, content: str):
        with db as cursor:
            cursor.execute(
                "UPDATE Comments SET Content = ?;", (content,)
            )

    def fetch(self):
        with db as cursor:
            cursor.execute(
              "SELECT Content FROM Comments WHERE id = ?;",(self.id,)  
            )

            row = cursor.fetchone()
            self.content = row[0]

    @staticmethod
    def getByPost(postId: int):
        with db as cursor:
            cursor.execute(
                '''
                SELECT c.Content, u.UserName FROM Comments AS c
                JOIN Users AS u ON c.AuthorId = u.Id
                WHERE c.PostId = ? AND c.ParentId IS NULL;
                ''' ,(postId,)
            )
            rows = cursor.fetchall()
            return list(map(lambda row: {
                'content': row[0],
                'author': row[1]
            },rows))