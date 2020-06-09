from flask_restful import Resource, request
from reddit.models.subreddit import Subreddit


class Subreddits(Resource):
    def get(self):
        args: dict = request.args

        search_term = args.get("q")

        subreddits = Subreddit.search(search_term)

        return list(map(Subreddit.toJSON, subreddits))
