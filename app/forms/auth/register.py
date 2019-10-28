from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError

from app.models.user import User

    
def validate_account(form, account):
    user = User.objects(account=account.data).first()
    
    if user:
        raise ValidationError('此帳號已經有人使用')
        
class RegisterForm(FlaskForm):
    name = StringField("名稱", validators=[InputRequired(), Length(max=50)])
    account = StringField('帳號', validators=[InputRequired(), Length(min=4, max=20), validate_account])
    password = PasswordField("密碼", validators=[InputRequired(), Length(min=6,max=20)])
    confirm  = PasswordField("再輸入一次密碼", validators=[
        InputRequired(),
        Length(min=6,max=20),
        EqualTo('password', "Password must match")])
    phone = StringField("電話號碼", validators=[InputRequired(), Length(max=15)])
    submit = SubmitField('註冊')