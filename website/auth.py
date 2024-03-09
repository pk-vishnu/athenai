from flask import Blueprint, redirect, render_template, request, flash, url_for
from .dbconnect import connect_to_database
from flask_login import UserMixin, current_user, login_user, login_required, logout_user
from website import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    connection = connect_to_database()
    cursor = connection.cursor()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        query = "SELECT * FROM auth WHERE email = %s AND pwrd = %s"
        cursor.execute(query, (email, password))
        user_data = cursor.fetchone()
        if user_data:
            user = User(id=user_data[0],email=user_data[0],username=user_data[2])
            login_user(user,remember=True)
            flash("Login Success!",category="success")
            return redirect(url_for("views.home"))
        else:
            flash("Incorrect password!", category="error")
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        connection = connect_to_database()
        cursor = connection.cursor()
        email = request.form.get("email")
        username = request.form.get("name")
        password = request.form.get("password")
        values = (username, password, email)
        query = "INSERT INTO auth (username, pwrd, email) VALUES (%s, %s, %s)"
        cursor.execute(query, values)
        user = User(id=username,email=email,username=username)
        login_user(user,remember=True)
        connection.commit()
        connection.close()
        flash("Account Created!", category="success")

        return redirect(url_for("views.home"))
    return render_template("signup.html",user=current_user)