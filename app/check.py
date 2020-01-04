from app.models.product import Product, PRODUCT_STATUS
from app.models.order import Order, ORDER_STATUS
from app.models.user import User
import datetime

def check_time():
    while True:
        products = Product.objects(status=PRODUCT_STATUS["SELLING"], bid__due_time__lte=datetime.datetime.utcnow()+datetime.timedelta(hours=8))

        for product in products:
            if product.bid.buyer_id == None:
                product.status = PRODUCT_STATUS["REMOVE"]
                product.save()
            else:
                user = User.objects(id=product.bid.buyer_id.id).first()
                product.status = PRODUCT_STATUS["SOLD"]
                user.hicoin -= product.bid.now_price
                Order(buyer_id=user.id, product_id=product.id, status=ORDER_STATUS["TRANSFERING"]).save()
                user.save()
                product.save()

        orders = Order.objects(status=ORDER_STATUS["RECEIPTING"], transfer_time__lte=datetime.datetime.utcnow()+datetime.timedelta(hours=-64))
        for order in orders:
            order.finish_time = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
            order.buyer_rating = 5
            order.comment = ""
            order.status = ORDER_STATUS["COMPLETE"]
            user = User.objects(id=order.product_id.seller_id.id).first()
            if order.product_id.bidding == True:
                user.hicoin += int(order.product_id.bid.now_price * 0.88)
            else:
                user.hicoin += int(order.product_id.price * 0.88)
            order.save()
            user.save()