from flask import redirect, render_template, url_for, flash, request, abort
from flask.views import MethodView
from flask_login import current_user

from flask_socketio import emit ##for test socketio

from app.models.user import User
from app import app, socketio

class HiChatView(MethodView):
    def get(self):
        # if request.args.get('way') == "bidding":
        #     products = Product.objects(name__icontains=request.args.get('keyword'), status=0, bidding=True)
            
        #     way = "bidding"
        # elif request.args.get('way') == "normal":
        #     products = Product.objects(name__icontains=request.args.get('keyword'), status=0, bidding=False)
        #     way = "normal"
        # else:
        #     abort(404)

        return render_template('user/hichatT.html', app=app, users=User.objects, currentUserID=current_user.id)

    def post(self):
    	pass

@socketio.on('chat message')
def handle_message(senderID, receiverID, message):
    sender = User.objects.get(id=senderID)
    data = {
        "senderID" : str(sender.id),
        "senderName": sender.name,
        "message" : message
    }
    emit(receiverID, data, broadcast=True)
    emit(senderID, data, broadcast=True)