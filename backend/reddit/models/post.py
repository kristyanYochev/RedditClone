from reddit.extensions import db
from typing import Optional


class Post:
    def __init__(self, pid: Optional[int] = None):
        self.id = pid

    @staticmethod
    def add(title: str,
            content: str,
            authorId: int,
            subredditName: str):
        with db as cursor:
            cursor.execute(
                """
                INSERT INTO Posts (
                    Title,
                    Content,
                    AuthorId,
                    SubredditName
                ) VALUES (?, ?, ?, ?);
                """,
                (
                    title,
                    content,
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
                "UPDATE Posts SET Title = ?, Content = ? WHERE Id = ?;",
                (
                    title,
                    content,
                    self.id
                )
            )

    @staticmethod
    def getFromUser(id: int):
        with db as cursor:
            cursor.execute(
                '''
                SELECT p.Title, p.Content, p.Score, p.SubredditName FROM Posts AS p
                JOIN UserSubredditSubscriptions AS uss ON p.AuthorId = uss.Id
                WHERE p.AuthorId = ?
                ORDER BY p.Score DESC
                ''', (id,)
            )
            rows = cursor.fetchall()
            return list(map(lambda row: {
                'title': row[0], 'content': row[1], 'score': row[2], 'subredditName': row[3]
            }, rows))

    def updateScore(self, amount: int):
        with db as cursor:
            cursor.execute(
                "UPDATE Posts SET Score = Score + ? WHERE Id = ?;",
                (amount, self.id)
            )

    @staticmethod
    def toJSON(title: str, content: str, score: int, subredditName: str):
        return {
            "title": title,
            "content": content,
            "score": score,
            "subredditName": subredditName
        }
