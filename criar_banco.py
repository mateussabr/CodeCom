from CodeCom import app, database
from CodeCom.models import User, Post

with app.app_context():
    database.create_all()