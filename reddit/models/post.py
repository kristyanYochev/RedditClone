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
                "DELETE FROM Posts WHERE Id = ?;", (self.id,)
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
                SELECT p.Id, p.Title, p.Content, p.Score, p.SubredditName FROM Posts AS p
                WHERE p.AuthorId = ?
                ORDER BY p.Score DESC
                ''', (id,)
            )

            rows = cursor.fetchall()

            return list(map(lambda row: {
                'id': row[0], 'title': row[1], 'content': row[2], 'score': row[3], 'subredditName': row[4]
            }, rows))

    @staticmethod
    def getFeed(id: int):
        with db as cursor:
            cursor.execute(
                '''
                SELECT p.Id, p.Title, p.Content, p.Score, p.SubredditName, u.UserName FROM UserSubredditSubscriptions uss
                JOIN Posts p ON p.SubredditName = uss.SubredditName
                JOIN Users u ON p.AuthorId = u.Id
                WHERE uss.UserId = ?
                ORDER BY p.Score, p.UploadTime DESC;    
                ''', (id,)
            )

            rows = cursor.fetchall()

            return list(map(lambda row: {
                'id': row[0], 
                'title': row[1], 
                'content': row[2], 
                'score': row[3], 
                'subredditName': row[4],
                'author': row[5]
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

    @staticmethod
    def fetch(id: int):
        with db as cursor:
            cursor.execute(
                '''
                SELECT * FROM Posts WHERE Id = ?
                ''', (id,)
            )
            result = cursor.fetchone()
            data = {
                "id": id,
                "title": result[1], 
                "content": result[2],
                "score": result[3],
                "subredditName": result[6]
            }

            return data