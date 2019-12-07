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

class ShowNormalView(MethodView):
    def get(self, product_id):
        form = NormalForm()
        product = Product.objects(id=product_id, bidding=False).first()
        like = "far fa-heart"
        cart = "加入購物車"
        
        if product == None:
            abort(404)
        if current_user.is_active:
            #update history
            information = Information.objects(user_id=current_user.id).first()
            update = False
            for history in information.history:
                if history.product.id == product.id:
                    history.create_time = datetime.datetime.utcnow()
                    update = True
                    break
            if update == False:
                information.history.append(History(product=product.id))
            information.save()

            for like_product in information.like:
                if like_product.id == product.id:
                    like = "fas fa-heart"

            for cart_product in information.cart:
                if cart_product.id == product.id:
                    cart = "移出購物車"

            #update view times
            product.view += 1
            product.save()
        return render_template('product/normal.html', form=form, product=product, like=like, cart=cart, product_json=product.to_json())


    
    def post(self, product_id):
        form = NormalForm()
        product = Product.objects(id=product_id).first()

        if product == None:
            abort(404)
        if form.validate_on_submit():
            if form.like.data == True:
                information = Information.objects(user_id=current_user.id).first()
                for (idx, like) in enumerate(information.like):
                    if product.id == like.id:
                        del information.like[idx]
                        information.save()
                        return "far fa-heart"

                information.like.append(product.id)
                information.save()
                return "fas fa-heart"

            elif form.cart.data == True and product.seller_id.id != current_user.id:
                information = Information.objects(user_id=current_user.id).first()
                for (idx, cart) in enumerate(information.cart):
                    if product.id == cart.id:
                        del information.cart[idx]
                        information.save()
                        return "加入購物車"

                information.cart.append(product.id)
                information.save()
                return "移出購物車"
            #print(form.like.data)
            #print(form.cart.data)
        abort(404)
        
class NormalForm(FlaskForm):
    like = SubmitField('喜歡')
    cart = SubmitField('加入購物車')