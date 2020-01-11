from flask import redirect, render_template, url_for, flash, request
from flask.views import MethodView
from flask_login import current_user
from flask_wtf import FlaskForm

from app import app
from app.models.payment import Payment
from app.models.information import Information
from app.models.product import Product, RATE
from app.models.order import Order, ORDER_STATUS

class RecordView(MethodView):
	def get(self):
		payments = Payment.objects(payer_id=current_user.id, confirm=True)
		buy_orders = Order.objects(buyer_id=current_user.id, status__ne=ORDER_STATUS["CANCEL"])
		sell_orders = Order.objects(product_id__in=Product.objects(seller_id=current_user.id), status=ORDER_STATUS["COMPLETE"])

		records = list()
		for payment in payments:
			record = Record("儲值", payment.amount, payment.create_time)
			records.append(record)
		for order in buy_orders:
			if order.product_id.bidding == False:
				if order.coupon_id == None:
					record = Record("購買" + order.product_id.name, -1 * int(order.product_id.price * order.product_id.discount), order.create_time)
				else:
					record = Record("購買" + order.product_id.name, -1 * max(0, int(order.product_id.price * order.product_id.discount - order.coupon_id.discount)), order.create_time)
			else:
				record = Record("購買" + order.product_id.name, -1 * order.product_id.bid.now_price, order.create_time)
			records.append(record)
		for order in sell_orders:
			if order.product_id.bidding == False:
				record = Record("販賣" + order.product_id.name, int(order.product_id.price * RATE), order.finish_time)
			else:
				record = Record("販賣" + order.product_id.name, int(order.product_id.bid.now_price * RATE), order.finish_time)
			records.append(record)
		records = sorted(records, key=lambda k: k.time, reverse=True)
		return render_template('user/hicoin/record.html', records=records)

class Record(object):
	def __init__(self, title, price, time):
		self.title = title
		self.price = price
		self.time = time