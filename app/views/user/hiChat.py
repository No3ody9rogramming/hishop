from flask import redirect, render_template, url_for, flash, request, abort
from flask.views import MethodView
from flask_login import current_user

from flask_socketio import emit ##for test socketio

from app.models.user import User
from app.models.message import Message
from app import app, socketio

import json

class HiChatView(MethodView):
    def get(self):
        return render_template('user/hichatT.html', app=app, users=User.objects, currentUser=current_user)

    def post(self):
        senderID = request.values["senderID"]
        receiverID = request.values["receiverID"]        
        if senderID != str(current_user.id):
            print(senderID)
            print(current_user.id)
            abort(403)        
        messages = Message.objects(sender_id=senderID, receiver_id=receiverID).to_json()
        if receiverID != senderID:
            messagesRtoS = Message.objects(sender_id=receiverID, receiver_id=senderID)
            if(messagesRtoS.count() > 0 ):
                messagesList = json.loads(messages)
                messagesRtoSList = json.loads(messagesRtoS.to_json())
                messagesList.append(messagesRtoSList);
                messages = json.dumps(messagesList)
        return messages;

@socketio.on('chat message')
def handle_message(senderID, receiverID, message):
    sender = User.objects.get(id=senderID)
    data = {
        "senderID" : str(sender.id),
        "senderName": sender.name,
        "message" : message
    }
    emit(receiverID, data, broadcast=True)
    if receiverID != senderID:
        emit(senderID, data, broadcast=True)
    message = Message(sender_id=senderID, receiver_id=receiverID, message=message)
    message.save()