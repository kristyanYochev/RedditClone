from reddit.extensions import db
from typing import Optional


class Post:
    def __init__(self, pid: Optional[int] = None):
        self.id = pid

    @staticmethod
    def add(title: str,
            content: str,
            score: int,
            authorId: int,
            subredditName: str):
        with db as cursor:
            cursor.execute(
                """
                INSERT INTO Posts (
                    Title,
                    Content,
                    Score,
                    AuthorId,
                    SubredditName
                ) VALUES (?, ?, ?, ?, ?);
                """,
                (
                    title,
                    content,
                    score,
                    authorId,
                    subredditName
                )
            )

    def delete(self):
        with db as cursor:
            cursor.execute(
                "DELETE FROM Posts WHERE Id = ?;", (self.id)
            )

    def edit(self, title: str, content: str):
        with db as cursor:
            cursor.execute(
                "UPDATE Posts SET Title = ?, Content = ?;",
                (
                    title,
                    content
                )
            )

    def getBySubreddit(self, subredditName: str):
        with db as cursor:
            cursor.execute(
                '''
                SELECT p.Title, p.Score, u.UserName FROM Posts AS p
                JOIN Users AS u ON p.AuthorId = u.Id
                WHERE p.SubredditName = ?
                ORDER BY p.Score DESC
                ''', (subredditName,)
            )
            rows = cursor.fetchall()
            return list(map(lambda row: {
                'title': row[0], 'score': row[1], 'author': row[2]
            }, rows))

    def updateScore(self, amount: int):
        with db as cursor:
            cursor.execute(
                "UPDATE Posts SET Score = Score + ? WHERE Id = ?;",
                (amount, self.id)
            )
