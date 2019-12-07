from flask import redirect, render_template, url_for, flash, request
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange

import uuid, json, requests, shelve

from app import app
from app.models.product import Product
from app.models.information import Information


class CartOperationView(MethodView):
    def post(self):
        product_id = request.values['product_id']
        product = Product.objects(id=product_id).first()

        if product == None:
            abort(404)
        information = Information.objects(user_id=current_user.id).first()
        for (idx, cart) in enumerate(information.cart):
            if product.id == cart.id:
                del information.cart[idx]
                information.save()
                return "加入購物車"

        information.cart.append(product.id)
        information.save()
        return "移出購物車"
        return abort(404);