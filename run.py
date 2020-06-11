from reddit.app import app
from reddit.database.init import create_tables

if __name__ == "__main__":
    create_tables()
    app.run(port=3000)
