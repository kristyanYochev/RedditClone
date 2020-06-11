from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from reddit.models.post import Post
from sqlite3 import IntegrityError

class Posts(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "id",
            type=int,
            required=True,
        )
        self.parser.add_argument(
            "title",
            type=str,
            required=True,
            help="Title is required"
        )
        self.parser.add_argument(
            "content",
            type=str,
            required=True,
            help="Content is required"
        )
        self.parser.add_argument(
            "subredditName",
            type=str,
            required=True,
        )

    @jwt_required
    def get(self):
        authorId = get_jwt_identity()

        posts = Post.getFromUser(authorId)

        jsonify = list()

        for i in range(len(posts)):
            jsonify.append(Post.toJSON(posts[i].title, posts[i].content, posts[i].score, posts[i].subredditName))
            
        return jsonify

    def post(self):
        request = self.parser.parse_args()
        authorId = get_jwt_identity()

        try:
            Post.add(request.get("title"), 
                    request.get("content"), 
                    authorId, 
                    request.get("subredditName"))
            
            return {}, 200
        
        except IntegrityError:
            return {
                "message": {
                    "error": "Cannot add to non-existent subreddit!"
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
            Post(request.get("id")).edit(request.get("title"),
                    request.get("content"))

            return {}, 200

        except Exception as e:
            return {
                "message": {
                    "error": f"Internal Server Error: {e}"
                }
            }, 500

    def delete(self):
        id = self.parser.parse_args().get("id")
        
        Post(id).delete()

        return {}, 200





    