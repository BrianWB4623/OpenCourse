from flask import render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from . import auth_bp
from app import db
from app.models import User
from app.forms import LoginForm, RegistrationForm


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # user logged in, dont show login page 
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    # creates a login form
    form = LoginForm()
    # true if request is post, validators past
    if form.validate_on_submit():
        # look up the user in database with their username
        user = User.query.filter_by(username=form.username.data).first()
        # user exists and password matches the hashed database password
        if user and check_password_hash(user.password_hash, form.password.data):
            # login user
            login_user(user, remember=form.remember_me.data)
            flash("Log in successfull")
            # back to dashboard
            return redirect(url_for("main.index"))
        else:
            # user doesnt exist, or password wrong
            flash("Invalid username or password")
    # show login page again
    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # user already logged in
    if current_user.is_authenticated:
        # back to dashboard
        return redirect(url_for("main.index"))
    # make a registration form
    form = RegistrationForm()
    if form.validate_on_submit():
        # to hold if username is taken
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            # display error, new form
            flash("Username taken, choose another")
            return render_template("auth/register.html", form=form)
        # create the user
        # NOTE: User model now requires email, we will plug in a real form field later.
        user = User(username=form.username.data, email="placeholder@example.com")
        # make the password
        user.set_password(form.password.data)
        # to the database
        db.session.add(user)
        db.session.commit()
        # success message
        flash("Youve succesfully created an account, you may now login")
        # bring to login page
        return redirect(url_for("auth.login"))
    # validation failed, show the form again
    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))
