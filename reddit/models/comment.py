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
                INSERT INTO Comments (Content, PostId, AuthorId, ParentCommentId)
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
                '''
                UPDATE Comments SET Content = ?
                WHERE Id = ?;
                ''', (content, self.id,)
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
                SELECT c.Id, c.AuthorId, c.Content, u.UserName FROM Comments AS c
                JOIN Users AS u ON c.AuthorId = u.Id
                WHERE c.PostId = ? AND c.ParentCommentId IS NULL;
                ''' ,(postId,)
            )
            rows = cursor.fetchall()
            return list(map(lambda row: {
                'id': row[0],
                'authorid': row[1],
                'content': row[2],
                'author': row[3]
            },rows))