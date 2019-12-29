from flask import redirect, render_template, url_for, abort
from flask.views import MethodView
from flask_login import login_user, current_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError

from app import bcrypt, send_mail
from app.models.user import User
from app.models.information import Information

class RegisterView(MethodView):
    def get(self):
        form = RegisterForm()

        if current_user.is_active == False:
            return render_template('auth/register.html', form=form)
        else:
            return redirect(url_for('user.profile'))
    
    def post(self):
        form = RegisterForm()
        
        if form.validate_on_submit():
            user = User(account=form.account.data,
                        password=bcrypt.generate_password_hash(form.password.data).decode(),
                        name=form.name.data,
                        store_name=form.name.data,
                        email=form.email.data,
                        phone=form.phone.data,
                        birth=form.birth.data,
                        address='',
                        prefer_begin_time='',
                        prefer_end_time='')
            
            user.save()

            information = Information(user_id = user.id)
            information.save()

            send_mail("HiShop帳號認證", [form.email.data], url_for("verification", _external=True, user_id=user.id))

            return redirect(url_for('login'))
        
        return render_template('auth/register.html', form=form)

    
def validate_account(form, account):
    user = User.objects(account=account.data).first()
    
    if user:
        raise ValidationError('此帳號已經有人使用')

def validate_email(form, email):
    user = User.objects(email=email.data).first()
    if user:
        raise ValidationError('此信箱已經有人使用')
    elif (email.data.endswith("email.ntou.edu.tw") or email.data.endswith("mail.ntou.edu.tw")) == False:
        raise ValidationError('信箱必須為@email.ntou.edu.tw或@mail.ntou.edu.tw結尾')
        
class RegisterForm(FlaskForm):
    account = StringField('帳號', validators=[InputRequired("帳號不得為空"), Length(min=4, max=20,message="帳號介於4~20個字"), validate_account])
    password = PasswordField("密碼", validators=[InputRequired("密碼不得為空"), Length(min=6,max=20,message="密碼介於6~20個字")])
    confirm  = PasswordField("確認密碼", validators=[
        InputRequired("確認密碼不得為空"),
        EqualTo('password', "密碼前後不一致")])
    name = StringField("姓名", validators=[InputRequired("姓名不得為空"), Length(min=2, max=20, message="姓名介於2~20個字")])
    email = EmailField("海大信箱", validators=[InputRequired("信箱不得為空"), validate_email])
    phone = StringField("電話", validators=[InputRequired("電話不得為空"), Length(max=15,message="電話不得超過15個字")])
    birth = DateField('生日', validators=[InputRequired("生日不得為空")])
    submit = SubmitField('註冊')