from CodeCom import app, database, bcrypt
from CodeCom.forms import FormLogin, FormCreateAccount
from CodeCom.models import User, Post
from flask import url_for, render_template, redirect
from flask_login import login_required


@app.route("/criarconta", methods=["GET", "POST"])
def create_account():
    form_create_account = FormCreateAccount()
    if form_create_account.validate_on_submit():
        password = bcrypt.generate_password_hash(form_create_account.password.data)
        user = User(username=form_create_account.username.data , password=password, email=form_create_account.email.data)
        database.session.add(user)
        database.session.commit()

    return render_template("create_account.html", form=form_create_account)

@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    return render_template("homepage.html", form=form_login)

@app.route("/perfil/<user>")
@login_required
def profile(user):
    return render_template("profile.html", user=user)