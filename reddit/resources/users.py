# def post(self):
#     request = self.parser.parse_args()

#     try:
#         User.register(request.get("username"), request.get("password"))

#         return {}, 200
#     except IntegrityError:
#         return {
#             "message": {
#                 "error": "Username taken!"
#             }
#         }, 400
#     except Exception as e:
#         return {
#             "message": {
#                 "error": f"Internal Server Error: {e}"
#             }
#         }, 500

# def put(self):
#     request = self.parser.parse_args()

#     try:
#         user_id = User.verify(
#             request.get("username"),
#             request.get("password")
#         )
#         return {
#             "access_token": create_access_token(identity=user_id),
#             "refresh_token": create_refresh_token(identity=user_id)
#         }, 200
#     except UserNotFoundError:
#         return {
#             "message": {
#                 "error": "User not found!"
#             }
#         }, 400
#     except InvalidPasswordError:
#         return {
#             "message": {
#                 "error": "Password invalid!"
#             }
#         }, 400
#     except Exception as e:
#         return {
#             "message": {
#                 "error": f"Internal Server Error: {e}"
#             }
#         }, 500
