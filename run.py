from flask_login import login_required

from app import app, login_manager, mail, socketio

from app.views.index import IndexView
from app.views.search import SearchView, LineChatbotSearch
from app.views.product.normal import ShowNormalView

from app.views.auth.login import LoginView
from app.views.auth.logout import LogoutView
from app.views.auth.register import RegisterView
from app.views.auth.forgot import ForgotPasswordView
from app.views.auth.reset import ResetPasswordView

from app.views.user.account.profile import ProfileView
from app.views.user.account.password import PasswordView
from app.views.user.account.payment import PaymentView, PaymentConfirmView
from app.views.user.account.cart import CartView
from app.views.user.account.cartOperation import CartOperationView

from app.views.user.product.like import LikeView
from app.views.user.product.history import HistoryView

from app.views.user.selling.normal import NormalView
from app.views.user.selling.bidding import BiddingView

from app.views.user.question.report import ReportView
from app.views.user.question.all_question import All_questionView

from flask_mail import Message

from flask import render_template ##for test socketio
from flask_socketio import emit ##for test socketio


app.add_url_rule(rule='/', endpoint='index', view_func=IndexView.as_view('index_view'), methods=['GET'])
app.add_url_rule(rule='/index', view_func=IndexView.as_view('index_view'), methods=['GET'])
app.add_url_rule(rule='/search', endpoint='search', view_func=SearchView.as_view('search_view'), methods=['GET'])
app.add_url_rule(rule='/linesearch', endpoint='linesearch', view_func=LineChatbotSearch.as_view('line_chatbot_search'), methods=['POST'])
app.add_url_rule(rule='/normal/<string:product_id>', endpoint='show_normal', view_func=ShowNormalView.as_view('show_normal_view'), methods=['GET', 'POST'])
app.add_url_rule(rule='/cart', endpoint='cart', view_func=login_required(CartView.as_view('cart_view')), methods=['GET', 'POST'])
app.add_url_rule(rule='/cart/opration', endpoint='cartOperation', view_func=login_required(CartOperationView.as_view('cartOperation_view')), methods=['POST'])

app.add_url_rule(rule='/registration', endpoint='registration', view_func=RegisterView.as_view('register_view'), methods=['GET', 'POST'])
app.add_url_rule(rule='/login', endpoint='login', view_func=LoginView.as_view('login_view'), methods=['GET', 'POST'])
app.add_url_rule(rule='/logout', endpoint='logout', view_func=login_required(LogoutView.as_view('logout_view')), methods=['GET', 'POST'])
app.add_url_rule(rule='/password/reset', endpoint='forgot', view_func=ForgotPasswordView.as_view('forgot_password_view'), methods=['GET', 'POST'])
app.add_url_rule(rule='/password/reset/<string:reset_token>', endpoint='reset', view_func=ResetPasswordView.as_view('reset_password_view'), methods=['GET', 'POST'])

app.add_url_rule(rule='/user/account/profile', endpoint='profile', view_func=login_required(ProfileView.as_view('profile_view')), methods=['GET', 'POST'])
app.add_url_rule(rule='/user/account/password', endpoint='password', view_func=login_required(PasswordView.as_view('password_view')), methods=['GET', 'POST'])
app.add_url_rule(rule='/user/account/payment', endpoint='payment', view_func=login_required(PaymentView.as_view('payment_view')), methods=['GET', 'POST'])
app.add_url_rule(rule='/user/account/payment/confirm', endpoint='payment_confirm', view_func=login_required(PaymentConfirmView.as_view('payment_confirm_view')), methods=['GET'])

app.add_url_rule(rule='/user/product/like', endpoint='like', view_func=login_required(LikeView.as_view('like_view')), methods=['GET', 'POST'])
app.add_url_rule(rule='/user/product/history', endpoint='history', view_func=login_required(HistoryView.as_view('history_view')), methods=['GET', 'POST'])

app.add_url_rule(rule='/user/selling/normal', endpoint='normal', view_func=login_required(NormalView.as_view('normal_view')), methods=['GET', 'POST'])
app.add_url_rule(rule='/user/selling/bidding', endpoint='bidding', view_func=login_required(BiddingView.as_view('bidding_view')), methods=['GET', 'POST'])

app.add_url_rule(rule='/user/question/report', endpoint='report', view_func=login_required(ReportView.as_view('report_view')), methods=['GET', 'POST'])
app.add_url_rule(rule='/user/question/all_question', endpoint='all_question', view_func=login_required(All_questionView.as_view('all_question_view')), methods=['GET', 'POST'])
@app.route('/test')
def hello():
    return render_template('user/hichatT.html', app=app)

@socketio.on('chat message')
def handle_message(message):
    print('received message: ' + message)
    emit('chat message', message)



if __name__ == '__main__':
     socketio.run(app, debug=True)
