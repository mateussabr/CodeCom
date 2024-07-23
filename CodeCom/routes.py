from CodeCom import app, database, bcrypt
from CodeCom.forms import FormLogin, FormCreateAccount, FormPhoto
from CodeCom.models import User, Post
from flask import url_for, render_template, redirect
from flask_login import login_required, login_user, logout_user, current_user
import os
from werkzeug.utils import secure_filename

@app.route("/criarconta", methods=["GET", "POST"])
def create_account():
    form_create_account = FormCreateAccount()
    if form_create_account.validate_on_submit():
        password = bcrypt.generate_password_hash(form_create_account.password.data)
        user = User(username=form_create_account.username.data , password=password, email=form_create_account.email.data)
        database.session.add(user)
        database.session.commit()
        login_user(user, remember=True)
        return redirect(url_for("profile", id_user=user.id))

    return render_template("create_account.html", form=form_create_account)

@app.route("/minhasfotos")
@login_required
def my_posts():
    user = User.query.get(int(current_user.id))
    return render_template("my_posts.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        user = User.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user)
            return redirect(url_for("profile", id_user=user.id))
    return render_template("login.html", form=form_login)


@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    form_photo = FormPhoto()
    if form_photo.validate_on_submit():
        file = form_photo.photo.data 
        name = secure_filename(file.filename)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
        app.config["UPLOAD_FOLDER"], name)
        file.save(path)
        photo = Post(image=name, user_id=current_user.id)
        database.session.add(photo)
        database.session.commit()
    return render_template("post.html", form=form_photo)

@app.route("/perfil/<id_user>", methods=["GET", "POST"])
@login_required
def profile(id_user):
    if int(id_user) == int(current_user.id):
        return render_template("profile.html", user=current_user)
    else:        
        user = User.query.get(int(id_user))
        return render_template("profile.html", user=user)

@app.route('/feed')
@login_required
def feed():
    posts = Post.query.order_by(Post.date).all()
    return render_template('feed.html', posts=posts)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))