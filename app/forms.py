from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import MyDb
from app.models import Utilisateur

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

class RegisterForm(FlaskForm):
    prenom = StringField('Votre prénom', validators=[DataRequired()])
    email = EmailField('Votre email', validators=[DataRequired(), Email()])
    password = PasswordField('Votre mot de passe', validators=[DataRequired()])
    password2 = PasswordField('Confirmer votre mot de passe', validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('Enregistrer')

    def validate_email(self, email):
        user = MyDb.session.scalar(sa.select(Utilisateur).where(Utilisateur.email == email.data))
        if user is not None:
            raise ValidationError("Cette adresse email existe déjà !")