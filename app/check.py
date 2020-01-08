from flask import url_for

from app.models.product import Product, PRODUCT_STATUS
from app.models.order import Order, ORDER_STATUS
from app.models.user import User
from app.socketioService import sendMessageViaSocketIO
from app import app
import datetime


def check_time():
    products = Product.objects(status=PRODUCT_STATUS["SELLING"], bid__due_time__lte=datetime.datetime.utcnow()+datetime.timedelta(hours=8))

    for product in products:
        if product.bid.buyer_id is None:
            product.status = PRODUCT_STATUS["REMOVE"]
            product.save()
            sellBiddingNtf(product, PRODUCT_STATUS["REMOVE"])
        else:
            user = User.objects(id=product.bid.buyer_id.id).first()
            product.status = PRODUCT_STATUS["SOLD"]
            user.hicoin -= product.bid.now_price
            Order(buyer_id=user.id, product_id=product.id, status=ORDER_STATUS["TRANSFERING"]).save()
            user.save()
            product.save()
            boughtNtf(product, ORDER_STATUS["TRANSFERING"])

    orders = Order.objects(status=ORDER_STATUS["RECEIPTING"], transfer_time__lte=datetime.datetime.utcnow()+datetime.timedelta(hours=-64))
    for order in orders:
        order.finish_time = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        order.buyer_rating = 5
        order.comment = ""
        order.status = ORDER_STATUS["COMPLETE"]
        user = User.objects(id=order.product_id.seller_id.id).first()
        if order.product_id.bidding is True:
            user.hicoin += int(order.product_id.bid.now_price * 0.88)
        else:
            user.hicoin += int(order.product_id.price * 0.88)
        order.save()
        user.save()
        soldProduct(order.product_id)
        boughtNtf(order.product_id, ORDER_STATUS["COMPLETE"])


def sellBiddingNtf(product, operation):
    # use with for prevent an error about url_for should not be use before run
    with app.app_context(), app.test_request_context():
        userSellingRomovedUrl = url_for('user.selling_list',
                                        status=operation)

    operationNtfs = {
        PRODUCT_STATUS["REMOVE"]: "過期了, 系統自動結標",
        PRODUCT_STATUS["SOLD"]: "已賣出, 買家確認中!!"
    }

    message = ('<div class="d-inline">你的競標商品<a href="' +
               userSellingRomovedUrl + '">' +
               str(product.name) + '</a>' +
               operationNtfs[operation] + '</div>')

    if message is not None:
        sendMessageViaSocketIO(app.config["HISHOP_UID"],
                               str(product.seller_id.id),
                               message)


def boughtNtf(product, operation):

    with app.app_context(), app.test_request_context():
        userSellingRomovedUrl = url_for('user.purchase_list',
                                        status=operation)

    operationNtfs = {
        ORDER_STATUS["ORDER_STATUS['TRANSFERING']"]: "已得標, 請繼續完成領收",
        ORDER_STATUS["COMPLETE"]: "評論時間過期, 系統已自動評分賣家並完成交易!!"
    }

    message = ('<div class="d-inline">你競標的商品<a href="' +
               userSellingRomovedUrl + '">' +
               str(product.name) + '</a>' +
               operationNtfs + '</div>')

    sendMessageViaSocketIO(app.config["HISHOP_UID"],
                           str(product.buyer_id.id),
                           message)


def soldProduct(product):

    with app.app_context(), app.test_request_context():
        userSellingRomovedUrl = url_for('user.order_list',
                                        status=ORDER_STATUS["COMPLETE"])

    message = ('<div class="d-inline">你的競標商品<a href="' +
               userSellingRomovedUrl + '">' +
               str(product.name) + '</a>' +
               '-買家已完成交易, 本次交易獲得' +
               int(product.price * 0.88) +
               'hicoin</div>')

    sendMessageViaSocketIO(app.config["HISHOP_UID"],
                           str(product.seller_id.id),
                           message)
