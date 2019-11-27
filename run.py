from flask_login import login_required

from app import app, login_manager, mail

from app.views.index import IndexView
from app.views.search import SearchView, LineChatbotSearch
from app.views.product.normal import ShowNormalView

from app.views.auth.login import LoginView
from app.views.auth.logout import LogoutView
from app.views.auth.register import RegisterView

from app.views.user.account.profile import ProfileView
from app.views.user.account.password import PasswordView
from app.views.user.account.payment import PaymentView, PaymentConfirmView

from app.views.user.selling.normal import NormalView
from app.views.user.selling.bidding import BiddingView

from app.views.user.question.report import ReportView

from flask_mail import Message


app.add_url_rule(rule='/', endpoint='index', view_func=IndexView.as_view('index_view'), methods=['GET'])
app.add_url_rule(rule='/index', view_func=IndexView.as_view('index_view'), methods=['GET'])
app.add_url_rule(rule='/search', endpoint='search', view_func=SearchView.as_view('search_view'), methods=['GET'])
app.add_url_rule(rule='/linesearch', endpoint='linesearch', view_func=LineChatbotSearch.as_view('line_chatbot_search'), methods=['POST'])
app.add_url_rule(rule='/normal/<string:product_id>', endpoint='show_normal', view_func=ShowNormalView.as_view('show_normal_view'), methods=['GET', 'POST'])

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

@app.route("/message", endpoint="message")
def index():
    #  主旨
    msg_title = 'Hello It is Flask-Mail'
    #  收件者，格式為list，否則報錯
    msg_recipients = ['00557043@email.ntou.edu.tw']
    #  郵件內容
    msg_body = 'Hey, I am mail body!'
    #  也可以使用html
    #  msg_html = '<h1>Hey,Flask-mail Can Use HTML</h1>'
    msg = Message(msg_title,
				  sender="chu-yu",
                  recipients=msg_recipients)
    msg.body = msg_body
    #  msg.html = msg_html
    
    #  mail.send:寄出郵件
    mail.send(msg)
    return 'You Send Mail by Flask-Mail Success!!'

if __name__ == '__main__':
    app.run(host="0.0.0.0")
