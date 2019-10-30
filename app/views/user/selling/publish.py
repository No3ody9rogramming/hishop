from flask import redirect, render_template, url_for
from flask.views import MethodView
from flask_login import login_user

from app import bcrypt
from app.forms.user.selling.publish import PublishForm
from app.models.product import Product

class PublishView(MethodView):
    def get(self):
        form = PublishForm()
        return render_template('user/selling/publish.html', form=form)
    
    def post(self):
        form = PublishForm()
        
        if form.validate_on_submit():
            return redirect(url_for('profile'))
        
        return render_template('user/selling/publish.html', form=form)