from flask import redirect, render_template, url_for, abort
from flask.views import MethodView
from flask_login import login_user, current_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError

from app import bcrypt
from app.models.user import User
from app.models.information import Information

class RegisterView(MethodView):
    def get(self):
        form = RegisterForm()

        if current_user.is_active == False:
            return render_template('auth/register.html', form=form)
        else:
            abort(403)
    
    def post(self):
        form = RegisterForm()
        
        if form.validate_on_submit():
            user = User(account=form.account.data,
                        password=bcrypt.generate_password_hash(form.password.data).decode(),
                        name=form.name.data,
                        email=form.email.data,
                        phone=form.phone.data,
                        birth=form.birth.data)      
            user.save()

            information = Information(user_id = user.id)
            information.save()
            login_user(user)
            return redirect(url_for('profile'))
        
        return render_template('auth/register.html', form=form)

    
def validate_account(form, account):
    user = User.objects(account=account.data).first()
    
    if user:
        raise ValidationError('此帳號已經有人使用')

def validate_email(form, email):
    user = User.objects(email=email.data).first()

    if user:
        raise ValidationError('此信箱已經有人使用')
        
class RegisterForm(FlaskForm):
    account = StringField('帳號', validators=[InputRequired(), Length(min=4, max=20), validate_account])
    password = PasswordField("密碼", validators=[InputRequired(), Length(min=6,max=20)])
    confirm  = PasswordField("確認密碼", validators=[
        InputRequired(),
        Length(min=6,max=20),
        EqualTo('password', "Password must match")])
    name = StringField("姓名", validators=[InputRequired(), Length(min=2, max=20)])
    email = EmailField("海大信箱", validators=[InputRequired(), validate_email])
    phone = StringField("電話", validators=[InputRequired(), Length(max=15)])
    birth = DateField('生日', validators=[InputRequired()])
    submit = SubmitField('註冊')