from flask import redirect, render_template, url_for
from flask.views import MethodView
from flask_login import login_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError

from app import bcrypt
from app.models.user import User

class RegisterView(MethodView):
    def get(self):
        form = RegisterForm()
        return render_template('auth/register.html', form=form)
    
    def post(self):
        form = RegisterForm()
        
        if form.validate_on_submit():
            user = User(name=form.name.data,
                        account=form.account.data,
                        password=bcrypt.generate_password_hash(form.password.data).decode(),
                        born = form.born.data,
                        phone=form.phone.data)
            user.save()
            login_user(user)
            return redirect(url_for('profile'))
        
        return render_template('auth/register.html', form=form)

    
def validate_account(form, account):
    user = User.objects(account=account.data).first()
    
    if user:
        raise ValidationError('此帳號已經有人使用')
        
class RegisterForm(FlaskForm):
    name = StringField("名稱", validators=[InputRequired(), Length(max=50)])
    account = StringField('帳號', validators=[InputRequired(), Length(min=4, max=20), validate_account])
    password = PasswordField("密碼", validators=[InputRequired(), Length(min=6,max=20)])
    confirm  = PasswordField("確認密碼", validators=[
        InputRequired(),
        Length(min=6,max=20),
        EqualTo('password', "Password must match")])
    born = DateField('出生日期', validators=[InputRequired()])
    phone = StringField("電話號碼", validators=[InputRequired(), Length(max=15)])
    submit = SubmitField('註冊')