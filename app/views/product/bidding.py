from flask import redirect, render_template, url_for, abort, request, flash
from flask.views import MethodView
from flask_login import current_user, login_required
from flask_wtf import FlaskForm

from wtforms import SubmitField, IntegerField
from wtforms.validators import InputRequired, ValidationError

import datetime

from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.information import Information, History
from app.models.order import Order
from app.socketioService import updatePriceViaSocketIO, sendMessageViaSocketIO

PRODUCT_STATUS = {"SELLING" : "0", "SOLD" : "1", "FROZEN" : "2", "REMOVE" : "3", "ALL" : "4"}

class ShowBiddingView(MethodView):
    def get(self, product_id):
        form = BiddingForm()
        product = Product.objects(id=product_id, bidding=True).first()
        categories = Category.objects(categorycontains = product.categories)
        orders = Order.objects(product_id__in=Product.objects(seller_id=product.seller_id))
        similar_product =  Product.objects(id__ne=product_id, bid__due_time__gt=datetime.datetime.utcnow()+datetime.timedelta(hours=8),
                         bidding=True, status=0, categories__in=product.categories).order_by('-create_time')[:12]
        like = "far fa-heart"
        remove = "下架此商品"
        
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
        return render_template('product/bidding.html', form=form, orders=orders, product=product, similar_product=similar_product, PRODUCT_STATUS=PRODUCT_STATUS, remove=remove, like=like, now=datetime.datetime.utcnow() + datetime.timedelta(hours=8))

    @login_required
    def post(self, product_id):
        form = BiddingForm()
        product = Product.objects(id=product_id, status=0, bidding=True,
                            bid__due_time__gt=datetime.datetime.utcnow()+datetime.timedelta(hours=8)).first()
        if product == None:
            abort(404)

        if form.remove.data == True:
            remove = "商品已下架"
            product = Product.objects(id=product_id, bidding=False).first()
            product.status = PRODUCT_STATUS['REMOVE']
            product.save()
            return remove

        if form.validate_on_submit():
            your_price = product.bid.now_price + product.bid.per_price * form.price.data
            if your_price > product.price:
                your_price = product.price
                flash('金額過多', 'toomuch')

            if product.bid.per_price * form.price.data <= 0 or product.seller_id.id == current_user.id:
                flash('錯誤', 'error')
                
            else:
                if current_user != product.bid.buyer_id and current_user.hicoin < your_price:
                    form.price.errors.append('金額不足')
                    flash('金額不足', 'error')
                elif current_user == product.bid.buyer_id and current_user.hicoin < (your_price - product.bid.now_price):
                    form.price.errors.append('金額不足')
                    flash('金額不足', 'error')
                else:
                    if product.bid.buyer_id != None:
                        if product.bid.buyer_id == current_user:
                            current_user.hicoin += product.bid.now_price
                        else:
                            pre_buyer = User.objects(id=product.bid.buyer_id.id).first()
                            pre_buyer.hicoin += product.bid.now_price
                            pre_buyer.save()
                            flash('出價成功', 'success')
                    if product.bid.due_time - (datetime.datetime.utcnow() + datetime.timedelta(hours=8)) < datetime.timedelta(seconds=30):
                        product.bid.due_time += datetime.timedelta(minutes=3)
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

        return redirect(url_for('show_bidding', product_id=product_id))

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
    remove = SubmitField('下架此商品')
