from reddit.app import create_app
from reddit.database.init import create_tables

if __name__ == "__main__":
    app = create_app()
    create_tables()

    app.run(port=3000)
