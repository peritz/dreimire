from urllib.parse import urlsplit

import sqlalchemy as sa
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from dreimire import app, db
from dreimire.forms import LoginForm, RegistrationForm
from dreimire.models import User


@app.route("/")
@app.route("/index")
@login_required
def index():
    budgets = db.session.scalars(current_user.budgets.select()).all()
    return render_template("index.html", title="Home", budgets=budgets)


@app.route("/login", methods=["GET", "POST"])
def login():
    next_page = request.args.get("next")
    if not next_page or urlsplit(next_page).netloc != "":
        next_page = url_for("index")

    if current_user.is_authenticated:
        return redirect(next_page)
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(next_page)
    return render_template("login.html", title="Login", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    next_page = request.args.get("next")
    if not next_page or urlsplit(next_page).netloc != "":
        next_page = url_for("index")

    if current_user.is_authenticated:
        return redirect(next_page)
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(
            "Congratulations, you are now a registered user! Please login to continue."
        )
        return redirect(url_for("login", next=next_page))
    return render_template("register.html", title="Register", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile")
@login_required
def profile():
    return "Undefined"
