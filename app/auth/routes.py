from flask import render_template, flash, request
from . import auth_bp
from ..forms import LoginForm

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            flash("Not implemented yet!", "info")
        else:
            flash("Please fix the errors below and try again.", "warning")
    return render_template("auth/login.html", form=form)