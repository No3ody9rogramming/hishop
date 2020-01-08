from flask import redirect, render_template, url_for, request, flash, abort
from flask.views import MethodView
from flask_login import current_user, login_required
from wtforms import SubmitField, TextAreaField, HiddenField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, ValidationError

from app.models.order import Order, ORDER_STATUS
from app.models.product import Product
from app.models.user import User

import datetime
class OrderListView(MethodView):
    def get(self):
        form = OrderListForm()
        products = Product.objects(seller_id=current_user.id)

        status = request.args.get('status')
        if status == ORDER_STATUS['TRANSFERING']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["TRANSFERING"])
        elif status == ORDER_STATUS['RECEIPTING']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["RECEIPTING"])
        elif status == ORDER_STATUS['COMPLETE']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["COMPLETE"])
        elif status == ORDER_STATUS['CANCEL']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["CANCEL"])
        else:
            status = ORDER_STATUS["ALL"]
            orders = Order.objects(product_id__in=products)

        orders = sorted(orders, key=lambda k: k.create_time, reverse=False)

        return render_template('user/selling/order.html', orders=orders, ORDER_STATUS=ORDER_STATUS, status=status,form=form)
    def post(self):
        form = OrderListForm()
        
        if 'cancelOrderID' in request.form:
            if form.validate_on_submit:
                print(request.values['cancelOrderID'])
                order = Order.objects(id=request.values['cancelOrderID'],product_id__in=(Product.objects(seller_id=current_user.id))).first()
                if(order==None):
                    abort(404)
                else:
                    if str(order.status) == ORDER_STATUS['TRANSFERING']:
                        order.status = int(ORDER_STATUS['CANCEL'])
                        order.save()
                        buyer = User.objects(id=order.buyer_id.id).first()
                        if order.product_id.bidding:
                            buyer.hicoin += order.product_id.bid.now_price
                        else:
                            buyer.hicoin += order.product_id.price
                        buyer.save()

                    else:
                        abort(404)
        else:
            if 'score' not in request.form:
                flash('請點選評價星星',category='error')
            

            if form.validate_on_submit and 'score' in request.form:
                order = Order.objects(product_id__in=Product.objects(id=request.values['ProductID'],seller_id=current_user.id)).first()
                print(request.values['ProductID'])
                if order == None:
                    abort(404)
                else:
                    if str(order.status) !=ORDER_STATUS["TRANSFERING"]:
                        abort(404)
                    else:
                        order.seller_comment = form.detail.data      # correct
                        order.seller_rating = request.values['score']  # correct
                        order.status = ORDER_STATUS["RECEIPTING"]
                        order.transfer_time = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
                        order.save()
                print(request.values['score'])

        products = Product.objects(seller_id=current_user.id)

        status = request.args.get('status')
        if status == ORDER_STATUS['TRANSFERING']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["TRANSFERING"])
        elif status == ORDER_STATUS['RECEIPTING']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["RECEIPTING"])
        elif status == ORDER_STATUS['COMPLETE']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["COMPLETE"])
        elif status == ORDER_STATUS['CANCEL']:
            orders = Order.objects(product_id__in=products, status=ORDER_STATUS["CANCEL"])
        else:
            status = ORDER_STATUS["ALL"]
            orders = Order.objects(product_id__in=products)



        orders = sorted(orders, key=lambda k: k.create_time, reverse=False)

        return render_template('user/selling/order.html', orders=orders, ORDER_STATUS=ORDER_STATUS, status=status,form=form)




class OrderListForm(FlaskForm):
    #ProductID = HiddenField()
    detail = StringField("評論")
    submit = SubmitField('確定')
    cancel = SubmitField('取消訂單')