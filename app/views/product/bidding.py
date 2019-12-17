from flask import redirect, render_template, url_for, abort, request
from flask.views import MethodView
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from flask_socketio import emit ##for test socketio

from wtforms import SubmitField, IntegerField
from wtforms.validators import InputRequired, ValidationError

import datetime

from app.models.user import User
from app.models.product import Product
from app.models.information import Information, History
from app.models.order import Order
from app import socketio, app

class ShowBiddingView(MethodView):
    def get(self, product_id):
        form = BiddingForm()
        product = Product.objects(id=product_id, bidding=True).first()
        like = "far fa-heart"
        
        if product == None:
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

            product.view += 1
            product.save()
        return render_template('product/bidding.html', form=form, product=product, like=like, now=datetime.datetime.utcnow() + datetime.timedelta(hours=8), app=app)

    @login_required
    def post(self, product_id):
        form = BiddingForm()
        product = Product.objects(id=product_id, status=0, bidding=True,
                            bid__due_time__gt=datetime.datetime.utcnow()+datetime.timedelta(hours=8)).first()
        if product == None:
            abort(404)

        if form.validate_on_submit():
            your_price = product.bid.now_price + product.bid.per_price * form.price.data
            if your_price > product.price:
                your_price = product.price

            if current_user != product.bid.buyer_id and current_user.hicoin < your_price:
                form.price.errors.append('金額不足')
            elif current_user == product.bid.buyer_id and current_user.hicoin < (your_price - product.bid.now_price):
                form.price.errors.append('金額不足')
            else:
                if product.bid.buyer_id != None:
                    if product.bid.buyer_id == current_user:
                        current_user.hicoin += product.bid.now_price
                    else:
                        pre_buyer = User.objects(id=product.bid.buyer_id.id).first()
                        pre_buyer.hicoin += product.bid.now_price
                        pre_buyer.save()

                product.bid.buyer_id = current_user.id
                if your_price >= product.price:
                    Order(buyer_id=current_user.id, product_id=product_id).save()
                    product.status = 1
                product.bid.now_price = your_price
                current_user.hicoin -= your_price
                current_user.save()
                product.save()
                updatePriceViaSocketIO(product.id, your_price)


        like = "far fa-heart"
        information = Information.objects(user_id=current_user.id).first()
        if product in information.like:
            like = "fas fa-heart"

        return render_template('product/bidding.html', form=form, product=product, like=like, product_json=product.to_json())

def validate_price(form, price):
    try:
        price = int(price.data)
    except:
        raise ValidationError('請輸入數字')

    product_id = request.base_url.split('/')[-1]
    product = Product.objects(id=product_id, bidding=True).first()

    if price > current_user.hicoin:
        raise ValidationError('金額不足')

class BiddingForm(FlaskForm):
    like = SubmitField('喜歡')
    price = IntegerField("起標價", validators=[InputRequired(), validate_price])
    submit = SubmitField('出價')

def updatePriceViaSocketIO(product_id, newPrice):
    print(str(product_id))
    socketio.emit(str(product_id), {'newPrice': newPrice}, broadcast=True)
