from flask import Flask, render_template, url_for, make_response, request, redirect, flash, abort
import random
from models import User, db
from uuid import uuid4
import hashlib

app = Flask(__name__)
app.secret_key= "foH_C1JpvVdtMtVHzGLInQ"
db.create_all()

@app.route("/", methods=["GET"])
def index():

    token = request.cookies.get("token")

    if token:
        user = db.query(User).filter_by(session_token=token).first()
        print(type(user))
        return render_template("user.html", user=user)
    else:
        user = None
    return render_template("index.html", user=user)


@app.route("/user", methods=["POST"])
def user():

    req = request.form
    if db.query(User).filter_by(email=req.get("email")).first():
        print("email already exists")

        email = req.get("email")
        user = db.query(User).filter_by(email=email).first()
        hashed_pwd = hashlib.sha256(req.get("password").encode()).hexdigest()

        if user.password != hashed_pwd:
            abort(401)

        response = make_response(render_template("user.html", user=user))
        response.set_cookie("token", user.session_token)
        response.set_cookie("email", email)
        return response
    else:
        email = req.get("email")
        username = req.get("username")
        password = req.get("password")
        session_token = str(uuid4())
        pwd = hashlib.sha256(password.encode()).hexdigest()
        secret_number = random.randint(1, 100)
        attempts = 100
        games_played = 0
        user = User(username=username, email=email, password=pwd,
                    secret_number=secret_number, attempts=attempts, games_played=games_played,
                    session_token=session_token)
        db.add(user)
        db.commit()

        response = make_response(redirect(url_for("index")))
        response.set_cookie("token", session_token)
        response.set_cookie("email", email)
        return response

@app.route("/game", methods=["GET", "POST"])
def game():
    email = request.cookies.get("email")
    user = db.query(User).filter_by(email=email).first()


    if request.method == "POST":
        guess = int(request.form.get("guess"))
        user_secret = int(user.secret_number)

        if guess == user_secret:
            message = f"Correct! The secret number was {user_secret}"
            flash(message)
            new_secret = random.randint(1, 100)
            user.secret_number = str(new_secret)
            user.games_played += 1
            db.add(user)
            db.commit()
            print(user.secret_number)
            return render_template("game.html", guess=True)
        elif guess > user_secret:
            message = "Lower"
            flash(message)
        else:
            message = "Higher"
            flash(message)

    return render_template("game.html")

@app.route("/sign-out")
def sign_out():
    response = make_response(redirect(url_for("index")))
    response.delete_cookie("token")
    return response
