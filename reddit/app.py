from flask import Flask, request, render_template, redirect, session

from reddit.models.user import User, UserNotFoundError, InvalidPasswordError
from sqlite3 import IntegrityError


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    return app


app = create_app()


@app.route("/")
def index():
    return """
        <h1>Hello World</h1>
        <a href='/login'>Login</a>
        <a href='/register'>Register</a>"""


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=None)
    else:
        username: str = request.form["username"]
        password: str = request.form["password"]

        try:
            uid = User.verify(username, password)

            session["userId"] = uid
            session["loggedIn"] = True

            return redirect("/")
        except UserNotFoundError:
            return render_template("login.html", error="User not found!")
        except InvalidPasswordError:
            return render_template("login.html", error="Invalid password!")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", error=None)
    else:
        username: str = request.form["username"]
        password: str = request.form["password"]
        repeat_password: str = request.form["repeat_password"]

        if password != repeat_password:
            return render_template(
                "register.html",
                error="Passwords do not match!"
            )

        try:
            User.register(username, password)

            return redirect("/login")
        except IntegrityError:
            return render_template("register.html", error="Username taken!")
