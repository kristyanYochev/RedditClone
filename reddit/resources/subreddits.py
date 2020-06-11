from flask_restful import Resource, request, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from reddit.models.subreddit import Subreddit
from reddit.models.user import User
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

    @jwt_required
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

    def delete(self):
        name = self.parser.parse_args().get("name")

        Subreddit(name).delete()

        return {}, 200


class SubredditSubscribe(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "name",
            type=str,
            required=True,
            help="Name is required!"
        )

    @jwt_required
    def post(self, sub_name: str):
        user_id = get_jwt_identity()

        try:
            User(user_id).subscribeToSubreddit(sub_name)
        except IntegrityError:
            return {
                "message": {
                    "error": "Subreddit doesn't exist"
                }
            }, 400

        return {}, 200
