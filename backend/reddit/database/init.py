from reddit.extensions import db


def create_tables():
    with db as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Users (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                UserName VARCHAR(256) NOT NULL UNIQUE,
                Password VARCHAR(256) NOT NULL
            );
            """, []
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Subreddits (
                Name VARCHAR(128) PRIMARY KEY
            );
            """, []
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS UserSubredditSubscriptions (
                SubredditName VARCHAR(128),
                UserId INTEGER,
                PRIMARY KEY (UserId, SubredditName),
                FOREIGN KEY (SubredditName) REFERENCES Subreddits(Name)
                    ON DELETE CASCADE,
                FOREIGN KEY (UserId) REFERENCES Users(Id) ON DELETE CASCADE
            );
            """, []
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Posts (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Title VARCHAR(128) NOT NULL,
                Content TEXT NOT NULL,
                Score INTEGER DEFAULT 0,
                UploadTime DATETIME CURRENT_TIMESTAMP,
                AuthorId INTEGER,
                SubredditName INTEGER,
                FOREIGN KEY (AuthorId) REFERENCES Users(Id) ON DELETE CASCADE,
                FOREIGN KEY (SubredditName) REFERENCES Subreddits(Name)
                    ON DELETE CASCADE
            );
            """, []
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Comments (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Content TEXT,
                PostId INTEGER NOT NULL,
                AuthorId INTEGER NOT NULL,
                ParentCommentId INTEGER,
                FOREIGN KEY (PostId) REFERENCES Posts(Id) ON DELETE CASCADE,
                FOREIGN KEY (AuthorId) REFERENCES Users(Id) ON DELETE CASCADE,
                FOREIGN KEY (ParentCommentId) REFERENCES Comments(Id)
                    ON DELETE CASCADE
            );
            """, []
        )
