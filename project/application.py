import os
import sqlite3
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///todo.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    tasks = db.execute("SELECT task, date FROM tasks WHERE username=:username",
                        username=db.execute("SELECT username FROM users WHERE id=:userId", userId=session["user_id"])[0]["username"])

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":
        task = request.form.get("task")
        if not task:
            return apology("must provide task", 400)

        db.execute("INSERT INTO tasks (username, task, date) VALUES(:username, :task, :date)",
        username=db.execute("SELECT username FROM users WHERE id=:userId", userId=session["user_id"])[0]["username"],
        task=task,
        date=datetime.datetime.utcnow())

        return redirect("/")
    else:
        return render_template("add.html")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        if not request.form.get("current_tasks"):
            return apology("must select a task to delete")

        db.execute("DELETE FROM tasks WHERE username=:username AND task=:task",
                    username=db.execute("SELECT username FROM users WHERE id=:userId", userId=session["user_id"])[0]["username"],
                    task=request.form.get("current_tasks"))

        return redirect("/")
    else:
        tasks = db.execute("SELECT task FROM tasks WHERE username=:username",
                        username=db.execute("SELECT username FROM users WHERE id=:userId", userId=session["user_id"])[0]["username"])
        return render_template("delete.html", tasks=tasks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        currentUsernames = db.execute("SELECT username FROM users")
        for item in currentUsernames:
            if request.form.get("username") == item["username"]:
                return apology("This username is unavailable", 400)

        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                   username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "POST":
        oldPassword = request.form.get("old_password")
        newPassword = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        if not oldPassword or not newPassword or not confirmation:
            return apology("must enter password", 403)
        elif newPassword != confirmation:
            return apology("passwords must match", 403)
        elif not check_password_hash(db.execute("SELECT hash FROM users WHERE id=:userId", userId=session["user_id"])[0]["hash"],
                                     oldPassword):
            return apology("invalid old password", 403)

        db.execute("UPDATE users SET hash = :hash WHERE id=:userId", hash=generate_password_hash(newPassword),
                   userId=session["user_id"])
        return redirect("/")

    else:
        return render_template("password.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
