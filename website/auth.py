from flask import Blueprint, render_template, request, redirect, flash, url_for
from website import views
from .models import User
from .utilities import validEmail
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Welcome back " + user.first_name + "!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Invalid password", category="error")
        else:
            flash("Email not found", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exists", category="error")
        elif validEmail(email) == False:
            flash("Invalid email", category="error")
        elif len(firstName) < 2:
            flash("First name is too short", category="error")
        elif len(lastName) < 7:
            flash("Last name is too short", category="error")
        elif len(password1) < 7:
            flash("Password is too short", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        else:
            new_user = User(
                email=email,
                first_name=firstName,
                last_name=lastName,
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="success")
            login_user(user, remember=True)
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)
