from flask import redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_login import login_user, current_user, logout_user

from app.models.user import User
from app.forms.user.account.profile import ProfileForm

class ProfileView(MethodView):
    def get(self):
        form = ProfileForm(name=current_user.name, phone=current_user.phone)

        return render_template('user/account/profile.html', form=form)
    
    def post(self):
        form = ProfileForm()
        if form.validate_on_submit():
            current_user.name = form.name.data
            current_user.save()
            flash('修改成功')
        return redirect(url_for('profile'))