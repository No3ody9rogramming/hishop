from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, ValidationError

from app.models.user import User
from app import bcrypt

    
def validate_account(form, account):
    user = User.objects(account=account.data).first()
    print(user)
    if user == None:
        raise ValidationError('此帳號尚未註冊')

def validate_password(form, password):
    user = User.objects(account=form.account.data).first()
    if user == None:
        pass
    else:
        if bcrypt.check_password_hash(user.password, password.data) == False:
            raise ValidationError('密碼錯誤')
        
class LoginForm(FlaskForm):
    account = StringField('帳號', validators=[InputRequired(), validate_account])
    password = PasswordField("密碼", validators=[InputRequired(), validate_password])
    submit = SubmitField('登入')