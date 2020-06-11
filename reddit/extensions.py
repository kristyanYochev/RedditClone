from flask_restful import Api
from flask_jwt_extended import JWTManager
from reddit.database.database import Database

api = Api()
jwt = JWTManager()
db = Database("database.db")
