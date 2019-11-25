from flask import redirect, render_template, url_for, flash, request
from flask.views import MethodView
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,

from app.models.product import Product
from app import app

class SearchView(MethodView):
    def get(self):
        print(request.args.get('keyword'))

        if request.args.get('keyword') == None:
            products = Product.objects()
        else:
            products = Product.objects(name__icontains=request.args.get('keyword'), bidding=False)

        return render_template('search.html', products=products)

line_bot_api = LineBotApi(app.config['LINE_CHATBOT_ACCESS_TOKEN'])
handler = WebhookHandler(app.config['LINE_CHATBOT_SECRET'])

class LineChatbotSearch(MethodView):
	def get(self):

		# if request.args.get_json() == None:
		# 	products = Product.objects()
		# else:
		# 	products = Product.objects(name__icontains=request.args.get_json(), bidding=False)
		# 	return products.to_json()

		# get X-Line-Signature header value
	    signature = request.headers['X-Line-Signature']

	    # get request body as text
	    body = request.get_data(as_text=True)
	    app.logger.info("Request body: " + body)

	    # handle webhook body
	    try:
	        handler.handle(body, signature)
	    except InvalidSignatureError:
	        print("Invalid signature. Please check your channel access token/channel secret.")
	        abort(400)

	    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# @LineChatbotSearch.handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))