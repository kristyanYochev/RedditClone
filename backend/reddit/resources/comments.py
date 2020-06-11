from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from reddit.models.comment import Comment
from sqlite3 import IntegrityError

class Comments(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "Id",
            type=int,
        )
        self.parser.add_argument(
            "content",
            type=str,
            required=True,
            help="Content is required"
        )
        self.parser.add_argument(
            "postId",
            type=int,
            required=True
        )
        self.parser.add_argument(
            "parentId",
            type=int,
            required=True
        )
    
    @jwt_required

    def post(self):
        request = self.parser.parse_args()
        authorId = get_jwt_identity()

        try:
            Comment.add(request.get("content"),
                        request.get("postId"),
                        authorId,
                        request.get("parentId"))
            
            return {}, 200

        except Exception as e:
            return {
                "message": {
                    "error": f"Internal Server Error: {e}"
                }
            }, 500

    @jwt_required

    def put(self):
        request = self.parser.parse_args()
        
        try:
            Comment(request.get("Id")).edit(
                request.get("content")
            )
            return{},200

        except Exception as e:
            return {
                "message": {
                    "error": f"Internal Server Error: {e}"
                }
            }, 500
            
    @jwt_required

    def delete(self):
        id = self.parser.parse_args().get("Id")

        Comment(id).delete()
        return{},200