from functools import wraps
from flask import Flask, request, render_template, redirect, session

from reddit.models.user import User, UserNotFoundError, InvalidPasswordError
from reddit.models.post import Post
from reddit.models.subreddit import Subreddit

from sqlite3 import IntegrityError


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    return app


app = create_app()

@app.route("/")
def index():
    return render_template("index.html")


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

@app.route("/logout", methods=["GET"])
def logout():
    if request.method == "GET":
        session.pop("userId", None)
        session.pop("loggedIn", None)
        return redirect("/")


@app.route("/posts", methods=["GET", "POST"])
def posts():
    uid = session["userId"]

    if request.method == "GET":
        return render_template("post.html", error=None)
    else:
        title: str = request.form["title"]
        content: str = request.form["content"]
        subredditName: str = request.form["subredditName"]

        try:
            Post.add(title, content, uid, subredditName)
            return redirect("/")

        except IntegrityError:
            return render_template("post.html", error="Cannot add to non-existent subreddit!")

@app.route("/myPosts", methods=["GET"])
def myPosts():
    uid = session["userId"]

    if request.method == "GET":
        return render_template("my-posts.html", posts=Post.getFromUser(uid))          

@app.route("/posts/<int:id>", methods=["GET", "PUT", "DELETE"])
def post(postId: int):
    if request.method == "GET":
        return render_template("detailed.html", post=Post.fetch(postId))

    elif request.method == "PUT":
        title: str = request.form["title"]
        content: str = request.form["content"]

        Post(postId).edit(title, content)

        return redirect("/posts/{postId}")

    else:
        Post(postId).delete()

        return redirect('/posts')



@app.route("/r")
def subreddits():
    search_term = request.args.get("q")
    subs = Subreddit.search(search_term, session["userId"])

    return render_template("subreddits.html", subs=subs)


@app.route("/subscribe/<subName>")
def subscribe(subName: str):
    try:
        User(session["userId"]).subscribeToSubreddit(subName)
        return redirect("/")
    except IntegrityError:
        return """
            <h1>Cannot subscribe to subreddit
            you are already subscribed to!</h1><a href="/">BACK TO HOME</a>
            """
