from flask_login import login_required

from app import app, login_manager, mail, socketio
from app.check import check_time
from app.models.user import check_admin, check_activate
from app.models.product import Product

from app.views.index import IndexView
from app.views.search import SearchView, CatSearchView, LineChatbotSearch, CompSearch
from app.views.product.normal import ShowNormalView
from app.views.product.bidding import ShowBiddingView
from app.views.product.like import ProductLikeView

from app.views.auth.login import LoginView
from app.views.auth.logout import LogoutView
from app.views.auth.register import RegisterView
from app.views.auth.forgot import ForgotPasswordView
from app.views.auth.reset import ResetPasswordView
from app.views.auth.verification import VerificationView

from app.views.user.account.profile import ProfileView
from app.views.user.account.password import PasswordView
from app.views.user.account.payment import PaymentView, PaymentConfirmView
from app.views.user.account.cart import CartView
from app.views.user.account.cartOperation import CartOperationView
from app.views.user.product.like import LikeView
from app.views.user.product.history import HistoryView
from app.views.user.product.list import PurchaseListView
from app.views.user.selling.normal import NormalView
from app.views.user.selling.edit import EditView
from app.views.user.selling.bidding import BiddingView
from app.views.user.selling.list import SellingListView
from app.views.user.selling.order import OrderListView
from app.views.user.question.report import ReportView
from app.views.user.question.list import QuestionListView

from app.views.admin.account.password import AdminPasswordView
from app.views.admin.management.account import AccountView
from app.views.admin.management.product import ProductView
from app.views.admin.management.question import AdminQuestionView
from app.views.admin.management.coupon import AdminCouponView

from app.views.user.hiChat.view import HiChatView
from app.views.user.notification.notification import Notification
from app.views.user.hiChat.update import HiChatUpdate

from app.socketioService import socketServiceOn

from flask_mail import Message
from flask import render_template, Blueprint
from apscheduler.schedulers.background import BackgroundScheduler

socketServiceOn()

admin = Blueprint('admin', __name__)
admin.add_url_rule(rule='/account/password', endpoint='password', view_func=login_required(check_admin(AdminPasswordView.as_view('password_view'))), methods=['GET', 'POST'])
admin.add_url_rule(rule='/management/account', endpoint='account', view_func=login_required(check_admin(AccountView.as_view('account_view'))), methods=['GET', 'POST'])
admin.add_url_rule(rule='/management/product', endpoint='product', view_func=login_required(check_admin(ProductView.as_view('product_view'))), methods=['GET', 'POST'])
admin.add_url_rule(rule='/management/question', endpoint='question', view_func=login_required(check_admin(AdminQuestionView.as_view('admin_question_view'))), methods=['GET', 'POST'])
admin.add_url_rule(rule='/management/coupon', endpoint='coupon', view_func=login_required(check_admin(AdminCouponView.as_view('admin_coupon_view'))), methods=['GET', 'POST'])
app.register_blueprint(admin, url_prefix='/admin')

app.add_url_rule(rule='/', endpoint='index', view_func=IndexView.as_view('index_view'), methods=['GET'])
app.add_url_rule(rule='/index', view_func=IndexView.as_view('index_view'), methods=['GET'])
app.add_url_rule(rule='/search', endpoint='search', view_func=SearchView.as_view('search_view'), methods=['GET'])
app.add_url_rule(rule='/compsearch', endpoint='compsearch', view_func=CompSearch.as_view('comp_search_view'), methods=['GET'])
app.add_url_rule(rule='/search/<string:type_of>', endpoint='catsearch', view_func=CatSearchView.as_view('cat_search_view'), methods=['GET'])
app.add_url_rule(rule='/linesearch', endpoint='linesearch', view_func=LineChatbotSearch.as_view('line_chatbot_search'), methods=['POST'])
app.add_url_rule(rule='/normal/<string:product_id>', endpoint='show_normal', view_func=ShowNormalView.as_view('show_normal_view'), methods=['GET', 'POST'])
app.add_url_rule(rule='/bidding/<string:product_id>', endpoint='show_bidding', view_func=ShowBiddingView.as_view('show_bidding_view'), methods=['GET', 'POST'])
app.add_url_rule(rule='/like/<string:product_id>', endpoint='product_like', view_func=ProductLikeView.as_view('product_like_view'), methods=['POST'])
app.add_url_rule(rule='/cart', endpoint='cart', view_func=login_required(check_activate(CartView.as_view('cart_view'))), methods=['GET', 'POST'])
app.add_url_rule(rule='/cart/opration', endpoint='cartOperation', view_func=login_required(check_activate(CartOperationView.as_view('cartOperation_view'))), methods=['POST'])

app.add_url_rule(rule='/registration', endpoint='registration', view_func=RegisterView.as_view('register_view'), methods=['GET', 'POST'])
app.add_url_rule(rule='/login', endpoint='login', view_func=LoginView.as_view('login_view'), methods=['GET', 'POST'])
app.add_url_rule(rule='/logout', endpoint='logout', view_func=login_required(check_activate(LogoutView.as_view('logout_view'))), methods=['GET', 'POST'])
app.add_url_rule(rule='/verification/<string:user_id>', endpoint='verification', view_func=VerificationView.as_view('verification_view'), methods=['GET'])
app.add_url_rule(rule='/password/reset', endpoint='forgot', view_func=ForgotPasswordView.as_view('forgot_password_view'), methods=['GET', 'POST'])
app.add_url_rule(rule='/password/reset/<string:reset_token>', endpoint='reset', view_func=ResetPasswordView.as_view('reset_password_view'), methods=['GET', 'POST'])

user = Blueprint('user', __name__)
user.add_url_rule(rule='/account/profile', endpoint='profile', view_func=login_required(check_activate(ProfileView.as_view('profile_view'))), methods=['GET', 'POST'])
user.add_url_rule(rule='/account/password', endpoint='password', view_func=login_required(check_activate(PasswordView.as_view('password_view'))), methods=['GET', 'POST'])
user.add_url_rule(rule='/account/payment', endpoint='payment', view_func=login_required(check_activate(PaymentView.as_view('payment_view'))), methods=['GET', 'POST'])
user.add_url_rule(rule='/account/payment/confirm', endpoint='payment_confirm', view_func=login_required(check_activate(PaymentConfirmView.as_view('payment_confirm_view'))), methods=['GET'])

user.add_url_rule(rule='/product/list', endpoint='purchase_list', view_func=login_required(check_activate(PurchaseListView.as_view('purchase_list_view'))), methods=['GET', 'POST'])
user.add_url_rule(rule='/product/like', endpoint='like', view_func=login_required(check_activate(LikeView.as_view('like_view'))), methods=['GET', 'POST'])
user.add_url_rule(rule='/product/history', endpoint='history', view_func=login_required(check_activate(HistoryView.as_view('history_view'))), methods=['GET', 'POST'])

user.add_url_rule(rule='/selling/normal', endpoint='normal', view_func=login_required(check_activate(NormalView.as_view('normal_view'))), methods=['GET', 'POST'])
user.add_url_rule(rule='/selling/bidding', endpoint='bidding', view_func=login_required(check_activate(BiddingView.as_view('bidding_view'))), methods=['GET', 'POST'])
user.add_url_rule(rule='/selling/list', endpoint='selling_list', view_func=login_required(check_activate(SellingListView.as_view('selling_list_view'))), methods=['GET','POST'])
user.add_url_rule(rule='/selling/order', endpoint='order_list', view_func=login_required(check_activate(OrderListView.as_view('order_list_view'))), methods=['GET', 'POST'])
user.add_url_rule(rule='/selling/edit', endpoint='edit', view_func=login_required(check_activate(EditView.as_view('edit_view'))), methods=['GET', 'POST'])

user.add_url_rule(rule='/question/report', endpoint='report', view_func=login_required(check_activate(ReportView.as_view('report_view'))), methods=['GET', 'POST'])
user.add_url_rule(rule='/question/list', endpoint='question_list', view_func=login_required(check_activate(QuestionListView.as_view('question_list_view'))), methods=['GET'])
user.add_url_rule(rule='/hichat', endpoint='hichat', view_func=login_required(check_activate(HiChatView.as_view('hichat_view'))), methods=['GET', 'POST'])
user.add_url_rule(rule='/hichat_update', endpoint='hichat_update', view_func=login_required(check_activate(HiChatUpdate.as_view('hichat_update'))), methods=['POST'])
user.add_url_rule(rule='/notification', endpoint='notification', view_func=login_required(check_activate(Notification.as_view('notification'))), methods=['GET', 'POST'])
app.register_blueprint(user, url_prefix='/user')

if __name__ == '__main__':
	scheduler = BackgroundScheduler()
	scheduler.add_job(func=check_time)
	#scheduler.start()
	socketio.run(app, debug=True, host='0.0.0.0', use_reloader=False)
