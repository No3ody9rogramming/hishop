from flask import redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError

from app.models.product import Product

class IndexView(MethodView):
    def get(self):
        form = SearchForm()
        
        popular_products = Product.objects(bidding=False).order_by('-view')[:12]
        normal_products = Product.objects(bidding=False).order_by('-create_time')[:12]
        bidding_products = Product.objects(bidding=True).order_by('-create_time')[:12]

        return render_template('index.html', form=form,
         				popular_products=popular_products,
         				normal_products=normal_products,
         				bidding_products=bidding_products)
        
class SearchForm(FlaskForm):
    keyword = StringField("輸入搜尋", validators=[InputRequired(), Length(min=1, max=20)])
    submit = SubmitField("搜尋")