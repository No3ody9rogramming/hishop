from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from app import bcrypt

def validate_old_password(form, oldPassword):
    if bcrypt.check_password_hash(current_user.password, oldPassword.data) == False:
        raise ValidationError('密碼錯誤')

class PasswordForm(FlaskForm):
    old_password = PasswordField("當前密碼", validators=[InputRequired(), Length(min=6,max=20), validate_old_password])
    password = PasswordField("新密碼", validators=[InputRequired(), Length(min=6,max=20)])
    confirm  = PasswordField("再輸入一次密碼", validators=[
        InputRequired(),
        Length(min=6,max=20),
        EqualTo('password', "Password must match")])
    submit = SubmitField('確認')