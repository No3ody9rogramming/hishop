from app import app, login_manager
from app.views.login import LoginAPI
from app.views.logout import LogoutAPI
from app.views.auth.register import RegisterView

app.add_url_rule('/login', endpoint='login', view_func=LoginAPI.as_view('login_view'), methods=['POST', 'GET'])
app.add_url_rule('/logout', view_func=LogoutAPI.as_view('logout_view'), methods=['POST', 'GET'])
app.add_url_rule(rule='/registration', endpoint='registration', view_func=RegisterView.as_view('register_view'), methods=['GET', 'POST'])


if __name__ == '__main__':
    app.run()