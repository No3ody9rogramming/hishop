from flask import redirect, render_template, url_for, flash, request
from flask.views import MethodView
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError

from app.models.product import Product

class SearchView(MethodView):
    def get(self):
        print(request.args.get('keyword'))

        if request.args.get('keyword') == None:
            products = Product.objects()
        else:
            products = Product.objects(name__icontains=request.args.get('keyword'), bidding=False)

        return render_template('search.html', products=products)