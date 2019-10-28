from flask import redirect, render_template
from flask.views import MethodView

from app import bcrypt
from app.forms.auth.register import RegisterForm
from app.models.user import User

class RegisterView(MethodView):
    def get(self):
        form = RegisterForm()
        return render_template('auth/register.html', form=form)
    
    def post(self):
        form = RegisterForm()
        
        if form.validate_on_submit():
            print(bcrypt.generate_password_hash(form.password.data))
            user = User(name=form.name.data,
                        account=form.account.data,
                        password=bcrypt.generate_password_hash(form.password.data),
                        phone=form.phone.data)
            user.save()
            return 'save'
        
        return render_template('auth/register.html', form=form)