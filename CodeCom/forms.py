from CodeCom.models import User 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    button = SubmitField("Fazer Login")

class FormCreateAccount(FlaskForm):
    username = StringField("Nome", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirm_password = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("password")])
    button = SubmitField("Criar conta")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user: 
            return ValidationError("E-mail já cadastrado, faça login para continuar")