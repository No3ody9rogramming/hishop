from flask import redirect, render_template, url_for, flash, request
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import BooleanField, SubmitField, FieldList, SelectField
from wtforms.validators import InputRequired, NumberRange

from bson.objectid import ObjectId
import uuid, json, requests, shelve

from app import app
from app.models.payment import Payment
from app.models.information import Information
from app.models.product import Product
from app.models.order import Order

class CartView(MethodView):
    def get(self):
        form = CartForm()
        products = Information.objects(user_id=current_user.id).first().cart

        return render_template('user/account/cart.html', form=form, hicoin=current_user.hicoin, products = products)
    
    def post(self):
        form = CartForm()
        checkedProducts = request.form.getlist("productCheck")

        information = Information.objects(user_id=current_user.id).first()
        products = Product.objects(id__in=checkedProducts, seller_id__ne=current_user.id, status=0, bidding=False)
        total_price = sum(product['price'] for product in products)
        if current_user.hicoin >= total_price:
            current_user.hicoin -= total_price
            current_user.save()
            for product in products:
                Order(buyer_id=current_user.id, product_id=product.id).save()
                product.status = 1
                product.save()
                information.cart.remove(product)
                information.save()

        return redirect(url_for('cart'));

class CartForm(FlaskForm):
    submit = SubmitField('結帳GO')