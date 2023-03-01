from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///userinfo.db"
db.init_app(app)
app.secret_key = os.urandom(24)


class UserInfo(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)


@app.route('/')
def hello_world():
    return render_template("cover.html")
    

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template("index.html")
    else:
        return redirect('/login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        info = UserInfo(email=email, password=password)
        db.session.add(info)
        db.session.commit()
        return redirect("/login")
    return render_template("signup.html")


@app.route('/login-action', methods=['GET', 'POST'])
def login_action():
    email = request.form["email"]
    password = request.form["password"]
    users = UserInfo.query.filter_by(email=email, password=password)
    verify = [user for user in users]
    if verify:
        session["user_id"] = verify[0].user_id
        return redirect("/home")
    else:
        return redirect("/login")


@app.route('/login')
def login():

    return render_template("login.html")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("user_id")
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
