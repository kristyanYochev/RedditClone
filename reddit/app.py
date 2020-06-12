from functools import wraps
from flask import Flask, request, render_template, redirect, session

from reddit.models.comment import Comment
from reddit.models.user import User, UserNotFoundError, InvalidPasswordError
from reddit.models.post import Post
from reddit.models.subreddit import Subreddit

from sqlite3 import IntegrityError
from typing import Callable


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    return app


def login_required(f: Callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("loggedIn"):
            return f(*args, **kwargs)
        else:
            return redirect("/login")

    return wrapper


app = create_app()


@app.route("/")
def index():
    if session.get("loggedIn"):
        return render_template("index.html", posts=Post.getFeed(session.get("userId")))
    else:
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
        session.clear()
        return redirect("/")


@app.route("/posts", methods=["GET", "POST"])
@login_required
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
            return render_template(
                "post.html",
                error="Cannot add to non-existent subreddit!"
            )


@app.route("/myPosts", methods=["GET"])
def myPosts():
    uid = session["userId"]

    if request.method == "GET":
        return render_template("my-posts.html", posts=Post.getFromUser(uid))          


@app.route("/posts/<int:postId>", methods=["GET"])
@login_required
def post(postId: int):
    if request.method == "GET":
        return render_template("detailed.html", post=Post.fetch(postId))

@app.route("/posts/<int:postId>/edit", methods=["GET", "POST"])
@login_required
def edit(postId: int):
    if request.method == "GET":
        return render_template("edit-post.html", post=Post.fetch(postId))

    else:
        title: str = request.form["title"]
        content: str = request.form["content"]

        Post(postId).edit(title, content)

        return redirect("/myPosts")


@app.route("/posts/<int:postId>/delete", methods=["GET"])
@login_required
def delete(postId: int):
    if request.method == "GET":
        Post(postId).delete()

        return redirect('/myPosts')

@app.route("/posts/<int:postId>/upvote", methods=["GET"])
@login_required
def upvote(postId: int):
    if request.method == "GET":
        Post(postId).updateScore(1)

        return redirect('/')

@app.route("/posts/<int:postId>/downvote", methods=["GET"])
@login_required
def downvote(postId: int):
    if request.method == "GET":
        Post(postId).updateScore(-1)

        return redirect('/')

@app.route("/comments", methods=["POST"])
def add_comment():
    content: str = request.form["content"]
    postid: int = request.form["postId"]
    parentid: int = request.form.get("parentId")

    uid = session["userId"]

    Comment.add(content,postid,uid,parentid)

    return redirect(f"/posts/{postid}")

@app.route("/comments/<int:commentid>", methods=["GET", "PUT", "DELETE"])
def delete_comments(commentid: int):
    uid = session["userId"]

    if request.method == "GET":
        comment = Comment(commentid)
        comment.fetch()
        return render_template("edit_comment.html", comment=comment)
    elif request.method == "DELETE":
        try:
            Comment(commentid).delete(uid)
            return redirect("/")

        except PermissionError:
            return "<h1>No Permissions<h1><a href='/'>I AM BACK!</a>"
    else:
        try:
            values = (
                request.form['content']
            )
            Comment(commentid).edit(values)
            return redirect("/")

        except PermissionError:
            return "<h1>No Permissions<h1><a href='/'>I AM BACK!</a>"

@app.route("/r")
@login_required
def subreddits():
    search_term = request.args.get("q")
    subs = Subreddit.search(search_term, session["userId"])

    return render_template("subreddits.html", subs=subs)

@app.route("/r/<subredditName>", methods=["GET"])
@login_required
def subredditPosts(subredditName: str):
    if request.method == "GET":
        return render_template("subreddit-posts.html",  
        posts=Post.getBySubreddit(subredditName), 
        subredditName = subredditName)


@app.route("/subscribe/<subName>")
@login_required
def subscribe(subName: str):
    try:
        User(session["userId"]).subscribeToSubreddit(subName)
        return redirect("/")
    except IntegrityError:
        return """
            <h1>Cannot subscribe to subreddit
            you are already subscribed to!</h1><a href="/">BACK TO HOME</a>
            """