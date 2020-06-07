from flask_restful import Resource, reqparse
from reddit.models.user import User
from sqlite3 import IntegrityError


class Users(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "username",
            type=str,
            required=True,
            help="Username is required"
        )

        self.parser.add_argument(
            "password",
            type=str,
            required=True,
            help="Password is required"
        )

    def post(self):
        request = self.parser.parse_args()

        try:
            User.register(request.get("username"), request.get("password"))

            return {}, 200
        except IntegrityError:
            return {
                "message": {
                    "error": "Username taken!"
                }
            }, 400
        except Exception as e:
            return {
                "message": {
                    "error": f"Internal Server Error: {e}"
                }
            }, 500
