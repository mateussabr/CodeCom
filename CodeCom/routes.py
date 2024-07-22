from CodeCom import app
from flask import url_for, render_template, redirect
from flask_login import login_required
from CodeCom.forms import FormLogin, FormCreateAccount

@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    return render_template("homepage.html", form=form_login)

@app.route("/criarconta", methods=["GET", "POST"])
def create_account():
    form_create_account = FormCreateAccount()
    return render_template("create_account.html", form=form_create_account)

@app.route("/perfil/<user>")
@login_required
def profile(user):
    return render_template("profile.html", user=user)