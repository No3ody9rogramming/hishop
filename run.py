from flask_login import login_required

from app import app, login_manager
from app.views.auth.login import LoginView
from app.views.auth.logout import LogoutView
from app.views.auth.register import RegisterView

from app.views.user.account.profile import ProfileView
from app.views.user.account.password import PasswordView
from app.views.user.account.payment import PaymentView, PaymentConfirmView

from app.views.user.selling.normal import NormalView
from app.views.user.selling.bidding import BiddingView

from app.views.user.question.report import ReportView


app.add_url_rule(rule='/registration', endpoint='registration', view_func=RegisterView.as_view('register_view'), methods=['GET', 'POST'])
app.add_url_rule(rule='/login', endpoint='login', view_func=LoginView.as_view('login_view'), methods=['GET', 'POST'])
app.add_url_rule(rule='/logout', endpoint='logout', view_func=login_required(LogoutView.as_view('logout_view')), methods=['GET', 'POST'])

app.add_url_rule(rule='/user/account/profile', endpoint='profile', view_func=login_required(ProfileView.as_view('profile_view')), methods=['GET', 'POST'])
app.add_url_rule(rule='/user/account/password', endpoint='password', view_func=login_required(PasswordView.as_view('password_view')), methods=['GET', 'POST'])

app.add_url_rule(rule='/user/account/payment', endpoint='payment', view_func=login_required(PaymentView.as_view('payment_view')), methods=['GET', 'POST'])
app.add_url_rule(rule='/user/account/payment/confirm', endpoint='payment_confirm', view_func=login_required(PaymentConfirmView.as_view('payment_confirm_view')), methods=['GET'])

app.add_url_rule(rule='/user/selling/normal', endpoint='normal', view_func=login_required(NormalView.as_view('normal_view')), methods=['GET', 'POST'])
app.add_url_rule(rule='/user/selling/bidding', endpoint='bidding', view_func=login_required(BiddingView.as_view('bidding_view')), methods=['GET', 'POST'])

app.add_url_rule(rule='/user/question/report', endpoint='report', view_func=login_required(ReportView.as_view('report_view')), methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run()