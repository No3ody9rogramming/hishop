from flask import redirect, render_template, url_for, abort, request
from flask.views import MethodView
from flask_login import current_user, login_required

from app.models.product import Product
from app.models.information import Information

from app.models.order import Order, ORDER_STATUS
from app.models.user import User

PRODUCT_STATUS = {"SELLING" : "0", "SOLD" : "1", "FROZEN" : "2", "REMOVE" : "3", "ALL" : "4"}
SORT_STATUS = {"PRICE":"0","HOT":"1","RATING":"2","CREATE_TIME":"3"}
class LikeView(MethodView):
    def get(self):
        status = request.args.get('status')
        
        products = Information.objects(user_id=current_user.id).order_by(status).first().like

        status = request.args.get('status')
        if(status == SORT_STATUS["CREATE_TIME"]):
            products = sorted(products, key=lambda k: k.create_time, reverse=False)
        elif(status == SORT_STATUS["PRICE"]):
            products = sorted(products, key=lambda k: k.price, reverse=False)
        elif(status == SORT_STATUS["HOT"]):
            products = sorted(products, key=lambda k: k.view, reverse=False)
        elif(status == SORT_STATUS["RATING"]):
            rating_dict = {} # user:rating
            product_rating_dict = {} #product:rating
            for user in User.objects():
                seller_orders = Order.objects(product_id__in=Product.objects(seller_id=user.id),status=ORDER_STATUS["COMPLETE"])
                buyer_orders = Order.objects(product_id__in=Product.objects(seller_id=user.id),status=ORDER_STATUS["COMPLETE"])
                rating = 0
                count_seller_orders = 0
                count_buyer_orders = 0
                for order in seller_orders:
                    print(order.seller_rating)
                    if order.seller_rating != None:
                        rating += order.seller_rating
                        count_seller_orders += 1
                    
                for order in buyer_orders:
                    print(order.buyer_rating)
                    if order.buyer_rating!= None:
                        rating += order.buyer_rating
                        count_buyer_orders += 1
                #rating += buyer_orders.buyer_rating
                if count_buyer_orders + count_seller_orders !=0:
                    rating /= count_buyer_orders + count_seller_orders
                else:
                    rating = 0
                rating_dict[user.id] = rating
            for product in products:
                product_rating_dict[product.id] = rating_dict.get(product.seller_id)

                #print(rating)
            products = [x for _, x in sorted(zip(product_rating_dict,products), key=lambda pair: pair[0])] #sorted products by product_rating_dict
            #sorted(rating_dict.items(), key=lambda d: d[0])
            #products = sorted(products, key=lambda k: k.product.seller_id.rating, reverse=False)

            

        return render_template('user/product/like.html', products=products,PRODUCT_STATUS=PRODUCT_STATUS,SORT_STATUS=SORT_STATUS)
    def post(self):
    	pass