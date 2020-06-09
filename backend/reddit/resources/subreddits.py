from flask_restful import Resource, request, reqparse
from reddit.models.subreddit import Subreddit
from sqlite3 import IntegrityError


class Subreddits(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "name",
            type=str,
            required=True,
            help="Name is required!"
        )

    def get(self):
        args: dict = request.args

        search_term = args.get("q")

        subreddits = Subreddit.search(search_term)

        return list(map(Subreddit.toJSON, subreddits))

    def post(self):
        name = self.parser.parse_args().get("name")

        try:
            Subreddit(name).addToDb()
        except IntegrityError:
            return {
                "message": {
                    "error": "Subreddit already exists"
                }
            }, 400

        return {}, 200
