from flask import Blueprint, flash, render_template, request
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html", user=current_user)

