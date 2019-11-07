from flask import redirect, render_template, url_for
from flask.views import MethodView
from flask_login import login_user
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField

from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError, NumberRange

from app import bcrypt
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
        
class PublishForm(FlaskForm):
    name = StringField("商品名稱", validators=[InputRequired(), Length(max=50)])
    price = IntegerField("商品價格", validators=[InputRequired(), NumberRange(min=1, max=100000)])
    detail = CKEditorField("商品詳情")
    submit = SubmitField('上架')