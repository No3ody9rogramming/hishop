from flask import redirect, render_template, url_for, request
from flask.views import MethodView
from flask_login import current_user, login_required

from app.models.order import Order

#移交中 領收中 已完成 已取消 全部
ORDER_STATUS = {"TRANSFERING" : "0", "RECEIPTING" : "1", "COMPLETE" : "2", "CANCEL" : "3", "ALL" : "4"}
class PurchaseListView(MethodView):
    def get(self):
        status = request.args.get('status')
        if request.args.get('status') == ORDER_STATUS['TRANSFERING']:
            orders = Order.objects(buyer_id=current_user.id, status=ORDER_STATUS["TRANSFERING"])
        elif request.args.get('status') == ORDER_STATUS['RECEIPTING']:
            orders = Order.objects(buyer_id=current_user.id, status=ORDER_STATUS["RECEIPTING"])
        elif request.args.get('status') == ORDER_STATUS['COMPLETE']:
            orders = Order.objects(buyer_id=current_user.id, status=ORDER_STATUS["COMPLETE"])
        elif request.args.get('status') == ORDER_STATUS['CANCEL']:
            orders = Order.objects(buyer_id=current_user.id, status=ORDER_STATUS["CANCEL"])
        else:
            status = ORDER_STATUS["ALL"]
            orders = Order.objects(buyer_id=current_user.id)

        orders = sorted(orders, key=lambda k: k.create_time, reverse=False)

        return render_template('user/product/list.html', orders=orders, ORDER_STATUS=ORDER_STATUS, status=status)
    def post(self):
        pass