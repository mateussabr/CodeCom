from CodeCom.models import User 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()], render_kw={"placeholder": "*E-mail"})
    password = PasswordField("Senha", validators=[DataRequired()], render_kw={"placeholder": "*Senha"})
    button = SubmitField("Fazer Login")

class FormCreateAccount(FlaskForm):
    username = StringField("Nome", validators=[DataRequired()], render_kw={"placeholder": "*Nome"})
    email = StringField("E-mail", validators=[DataRequired(), Email()], render_kw={"placeholder": "*E-mail"})
    password = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)], render_kw={"placeholder": "*Senha"})
    confirm_password = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("password")], render_kw={"placeholder": "*Confirmar Senha"})
    button = SubmitField("Criar conta")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user: 
            return ValidationError("E-mail já cadastrado, faça login para continuar")
        
class FormPhoto(FlaskForm):
    photo = FileField("Foto", validators=[DataRequired()])
    button = SubmitField('Enviar')