import datetime

from flask_socketio import emit ##for test socketio
from app.models.user import User
from app.models.message import Message
from flask_login import current_user

from mongoengine.queryset.visitor import Q

from app import app, socketio

@socketio.on('send message')
def handle_message(senderID, receiverID, message): #函式名自訂    
    if(senderID != str(current_user.id)):
        abort(403)
    sender = User.objects.get(id=senderID)
    messageDocument = Message(sender_id=sender, receiver_id=receiverID, message=message, create_time=datetime.datetime.utcnow())
    messageDocument.save()
    data = {
        "senderID" : senderID,
        "senderName": sender.name,
        "message" : message,
        "messageID" : str(messageDocument.id)
    }
    emit(senderID + 'To' + receiverID, data, broadcast=True)
    if receiverID != senderID:
        emit(receiverID + 'To' + senderID, data, broadcast=True)


def updatePriceViaSocketIO(product_id, newPrice):
    print(str(product_id))
    socketio.emit(str(product_id), {'newPrice': newPrice}, broadcast=True)
