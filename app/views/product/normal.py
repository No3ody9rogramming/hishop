from flask import redirect, render_template, url_for, abort
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, InputRequired, Length, EqualTo, ValidationError

import datetime

from app.models.product import Product
from app.models.information import Information, History

PRODUCT_STATUS = {"SELLING" : "0", "SOLD" : "1", "FROZEN" : "2", "REMOVE" : "3", "ALL" : "4"}

class ShowNormalView(MethodView):
    def get(self, product_id):
        form = NormalForm()
        product = Product.objects(id=product_id, bidding=False).first()
        like = "far fa-heart"
        cart = "加入購物車"
        
        if product == None:
            abort(404)
        if product.status != PRODUCT_STATUS["SELLING"]:
            abort(404)
        if current_user.is_active:
            #update history
            information = Information.objects(user_id=current_user.id).first()
            history_product = [h['product'] for h in information.history]
            try:
                index = history_product.index(product)
                information.history[index].create_time = datetime.datetime.utcnow()
            except ValueError:
                information.history.append(History(product=product))
            information.save()

            if product in information.like:
                like = "fas fa-heart"

            if product in information.cart:
                cart = "移出購物車"

            product.view += 1
            product.save()
        return render_template('product/normal.html', form=form, product=product, like=like, cart=cart, product_json=product.to_json())


    
    def post(self, product_id):
        form = NormalForm()
        product = Product.objects(id=product_id, bidding=False).first()

        if product == None:
            abort(404)
        if form.validate_on_submit():
            information = Information.objects(user_id=current_user.id).first()

            if form.like.data == True:
                if product in information.like:
                    information.like.remove(product)
                    like = "far fa-heart"
                else:
                    information.like.append(product)
                    like = "fas fa-heart"
                information.save()

                return like

            elif form.cart.data == True and product.seller_id.id != current_user.id:
                if product in information.cart:
                    information.cart.remove(product)
                    cart = "加入購物車"
                else:
                    information.cart.append(product)
                    cart = "移出購物車"
                information.save()

                return cart

        abort(404)
        
class NormalForm(FlaskForm):
    like = SubmitField('喜歡')
    cart = SubmitField('加入購物車')