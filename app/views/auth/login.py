from flask import redirect, render_template, url_for, request, abort
from flask.views import MethodView
from flask_login import login_user, current_user, login_required, logout_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, ValidationError

from app import bcrypt, send_mail
from app.models.user import User

class LoginView(MethodView):
    def get(self):
        form = LoginForm()
        if current_user.is_active == False:
            return render_template('auth/login.html', form=form, next=request.args.get('next'))
        else:
            return redirect(url_for('user.profile'))
    
    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.objects(account=form.account.data).first()
            login_user(user)

            if request.args.get('next') == None:
                return redirect(url_for('index'))
            else:
                return redirect(request.args.get('next'))
        return render_template('auth/login.html', form=form)

    
def validate_account(form, account):
    user = User.objects(account=account.data).first()
    if user == None:
        raise ValidationError('此帳號尚未註冊')
    elif user.status == 0:
        send_mail("HiShop帳號認證", [user.email], url_for("verification", _external=True, user_id=user.id))
        raise ValidationError('此帳號尚未認證')

def validate_password(form, password):
    user = User.objects(account=form.account.data).first()
    if user == None:
        pass
    else:
        if bcrypt.check_password_hash(user.password, password.data) == False:
            raise ValidationError('密碼輸入錯誤')
        
class LoginForm(FlaskForm):
    account = StringField('帳號', validators=[InputRequired(), validate_account])
    password = PasswordField("密碼", validators=[InputRequired(), validate_password])
    submit = SubmitField('登入')