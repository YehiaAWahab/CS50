import os
import sqlite3
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    def getListOfCompanies(username, symbolOrPriceOrNumber):
        if symbolOrPriceOrNumber == "symbol" or symbolOrPriceOrNumber == "price" or symbolOrPriceOrNumber == "number":
            rows = db.execute("SELECT {0} FROM portfolio WHERE username=:username".format(symbolOrPriceOrNumber), username=username)
            if symbolOrPriceOrNumber == "symbol" and len(rows) >= 1:
                namesList = []
                for row in rows:
                    namesList.append(lookup(row[symbolOrPriceOrNumber])["name"])
                return namesList
            elif symbolOrPriceOrNumber == "price" and len(rows) >= 1:
                pricseList = []
                for row in rows:
                    pricseList.append(row[symbolOrPriceOrNumber])
                return pricseList
            elif symbolOrPriceOrNumber == "number" and len(rows) >= 1:
                numbersList = []
                for row in rows:
                    numbersList.append(row[symbolOrPriceOrNumber])
                return numbersList
            else:
                return None
        else:
            return None

    def getTotalValueHolding(username):
        priceRow = db.execute("SELECT price FROM portfolio WHERE username=:username", username=username)
        numberRow = db.execute("SELECT number FROM portfolio WHERE username=:username", username=username)

        if len(priceRow) >= 1 and len(numberRow) >= 1 and len(priceRow) == len(numberRow):
            totalList = []
            for i in range(len(priceRow)):
                totalList.append(float(priceRow[i]["price"]) * float(numberRow[i]["number"]))

            return totalList

    username = db.execute("SELECT username FROM users WHERE id=:userId", userId=session["user_id"])[0]["username"]
    companiesNames = getListOfCompanies(username, "symbol")
    numberOfShares = getListOfCompanies(username, "number")
    prices = getListOfCompanies(username, "price")
    totalValueHolding = getTotalValueHolding(username)

    currentCashBalance = db.execute("SELECT cash FROM users WHERE id=:userId", userId=session["user_id"])[0]["cash"]
    total = 0
    if totalValueHolding:
        for totalValue in totalValueHolding:
            total = total + totalValue

    cashAndStocksTotalValue = float(currentCashBalance) + total

    return render_template("index.html", username=username, companiesNames=companiesNames, numberOfShares=numberOfShares,
                           prices=prices, totalValueHolding=totalValueHolding, currentCashBalance=currentCashBalance, cashAndStocksTotalValue=cashAndStocksTotalValue)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide ticker", 400)
        elif not request.form.get("shares"):
            return apology("must provide number of shares", 400)
        elif not request.form.get("shares").isdigit():
            return apology("must enter numbers", 400)
        elif float(request.form.get("shares")) <= 0 or (float(request.form.get("shares")) % 1 != 0):
            return apology("number must be integer greater than one", 400)
        elif not lookup(request.form.get("symbol")):
            return apology("couldn't find company", 400)

        currentSymbols = db.execute("SELECT symbol FROM portfolio WHERE username=:username",
                                    username=db.execute("SELECT username FROM users WHERE id=:userId", userId=session["user_id"])[0]["username"])

        for symbol in currentSymbols:
            if symbol["symbol"].lower() == request.form.get("symbol").lower():
                return apology("you've already bought that stock", 403)

        currentBalance = db.execute("SELECT cash from users WHERE id=:userId", userId=session["user_id"])[0]["cash"]
        buyingPrice = lookup(request.form.get("symbol"))["price"] * float(request.form.get("shares"))
        if currentBalance < buyingPrice:
            return apology("not enough cash", 403)
        else:
            db.execute("UPDATE users SET cash = cash - {0} WHERE id=:userId".format(buyingPrice), userId=session["user_id"])
            username = db.execute("SELECT username FROM users WHERE id=:userId", userId=session["user_id"])[0]["username"]
            symbol = lookup(request.form.get("symbol"))["symbol"]
            numberOfShares = float(request.form.get("shares"))
            price = lookup(request.form.get("symbol"))["price"]
            date = datetime.datetime.utcnow()
            db.execute("INSERT INTO portfolio (username, symbol, number, price, date) VALUES(:username, :symbol, :number, :price, :date)",
                       username=username, symbol=symbol, number=numberOfShares, price=price, date=date)

            db.execute("INSERT INTO history (username, symbol, buyorsell, number, price, date) VALUES(:username, :symbol, :buyorsell, :number, :price, :date)",
                       username=db.execute("SELECT username FROM users WHERE id=:userId", userId=session["user_id"])[0]["username"],
                       symbol=symbol, buyorsell=1, number=float(request.form.get("shares")),
                       price=price, date=datetime.datetime.utcnow())

            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    enteredUsername = request.args.get('username')
    if not enteredUsername:
        return jsonify(False)
    currentUsernames = db.execute("SELECT username FROM users")
    for username in currentUsernames:
        if enteredUsername == username["username"]:
            return jsonify(False)

    return jsonify(True)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    username = db.execute("SELECT username FROM users WHERE id=:userId", userId=session["user_id"])[0]["username"]
    symbols = db.execute("SELECT symbol FROM history WHERE username=:username", username=username)
    buyorsells = []
    for item in db.execute("SELECT buyorsell FROM history WHERE username=:username", username=username):
        if item["buyorsell"]:
            buyorsells.append("Bought")
        else:
            buyorsells.append("Sold")
    numbers = db.execute("SELECT number FROM history WHERE username=:username", username=username)
    prices = db.execute("SELECT price FROM history WHERE username=:username", username=username)
    dates = db.execute("SELECT date FROM history WHERE username=:username", username=username)
    return render_template("history.html", username=username, symbols=symbols, buyorsells=buyorsells, numbers=numbers,
                           prices=prices, dates=dates)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide ticker", 400)
        quoted = lookup(request.form.get("symbol"))
        if not quoted:
            return apology("couldn't find company", 400)
        else:
            return render_template("quoted.html", name=quoted["name"], price=quoted["price"], symbol=quoted["symbol"])
    else:
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must select a stock", 400)
        elif not request.form.get("shares"):
            return apology("must provide number of shares", 400)
        elif float(request.form.get("shares")) <= 0:
            return apology("number of shares must be greater than one", 400)
        elif float(request.form.get("shares")) > db.execute("SELECT number FROM portfolio WHERE username=:username AND symbol=:symbol",
                                                            username=db.execute("SELECT username FROM users WHERE id=:userId",
                                                                                userId=session["user_id"])[0]["username"],
                                                            symbol=request.form.get("symbol"))[0]["number"]:
            return apology("you don't own enough shares", 400)

        numberOfShares = float(request.form.get("shares"))

        priceOfEachShare = db.execute("SELECT price FROM portfolio WHERE username=:username AND symbol=:symbol",
                                      username=db.execute("SELECT username FROM users WHERE id=:userId",
                                                          userId=session["user_id"])[0]["username"],
                                      symbol=request.form.get("symbol"))[0]["price"]

        totalValue = numberOfShares * priceOfEachShare

        db.execute("UPDATE users SET cash = cash + {0} WHERE id=:userId".format(totalValue), userId=session["user_id"])

        db.execute("UPDATE portfolio SET number = number - {0} WHERE username=:username AND symbol=:symbol".format(request.form.get("shares")),
                   username=db.execute("SELECT username FROM users WHERE id=:userId", userId=session["user_id"])[0]["username"],
                   symbol=request.form.get("symbol"))

        if db.execute("SELECT number FROM portfolio WHERE username=:username AND symbol=:symbol",
                      username=db.execute("SELECT username FROM users WHERE id=:userId", userId=session["user_id"])[0]["username"],
                      symbol=request.form.get("symbol"))[0]["number"] == 0:
            db.execute("DELETE FROM portfolio WHERE username=:username AND symbol=:symbol",
                       username=db.execute("SELECT username FROM users WHERE id=:userId", userId=session["user_id"])[0]["username"],
                       symbol=request.form.get("symbol"))

        db.execute("INSERT INTO history (username, symbol, buyorsell, number, price, date) VALUES(:username, :symbol, :buyorsell, :number, :price, :date)",
                   username=db.execute("SELECT username FROM users WHERE id=:userId", userId=session["user_id"])[0]["username"],
                   symbol=request.form.get("symbol"), buyorsell=0, number=float(request.form.get("shares")),
                   price=priceOfEachShare, date=datetime.datetime.utcnow())

        return redirect("/")

    else:
        symbolsList = db.execute("SELECT symbol FROM portfolio WHERE username=:username",
                                 username=db.execute("SELECT username FROM users WHERE id=:userId", userId=session["user_id"])[0]["username"])
        return render_template("sell.html", stocks=symbolsList)


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
