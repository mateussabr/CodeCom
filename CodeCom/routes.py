from CodeCom import app, database, bcrypt
from CodeCom.forms import FormLogin, FormCreateAccount
from CodeCom.models import User, Post
from flask import url_for, render_template, redirect
from flask_login import login_required, login_user, logout_user


@app.route("/criarconta", methods=["GET", "POST"])
def create_account():
    form_create_account = FormCreateAccount()
    if form_create_account.validate_on_submit():
        password = bcrypt.generate_password_hash(form_create_account.password.data)
        user = User(username=form_create_account.username.data , password=password, email=form_create_account.email.data)
        database.session.add(user)
        database.session.commit()
        login_user(user, remember=True)
        return redirect(url_for("profile", user=user.username))

    return render_template("create_account.html", form=form_create_account)

@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        user = User.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user)
            return redirect(url_for("profile", user=user.username))
    return render_template("homepage.html", form=form_login)

@app.route("/perfil/<user>")
@login_required
def profile(user):
    return render_template("profile.html", user=user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))