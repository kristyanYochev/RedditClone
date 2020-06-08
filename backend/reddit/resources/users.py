from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from reddit.models.user import User, InvalidPasswordError, UserNotFoundError
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

    def put(self):
        request = self.parser.parse_args()

        try:
            user_id = User.veify(
                request.get("username"),
                request.get("password")
            )
            return {
                "access_token": create_access_token(identity=user_id),
                "refresh_token": create_refresh_token(identity=user_id)
            }, 200
        except UserNotFoundError:
            return {
                "message": {
                    "error": "User not found!"
                }
            }, 400
        except InvalidPasswordError:
            return {
                "message": {
                    "error": "Password invalid!"
                }
            }, 400
        except Exception as e:
            return {
                "message": {
                    "error": f"Internal Server Error: {e}"
                }
            }, 500
