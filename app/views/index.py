from flask import redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError

from app.models.user import User

class IndexView(MethodView):
    def get(self):
        form = SearchForm()

        return render_template('index.html', form=form)
    
    def post(self):
        form = SearchForm()
        if form.validate_on_submit():
            products = 
        return redirect(url_for('profile'))
        
class SearchForm(FlaskForm):
    search = StringField("姓名", validators=[InputRequired(), Length(min=2, max=200)])
    submit = SubmitField("搜尋")