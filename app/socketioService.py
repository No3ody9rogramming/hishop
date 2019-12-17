from flask_socketio import emit ##for test socketio
from app.models.user import User
from app.models.message import Message

from mongoengine.queryset.visitor import Q

from app import app, socketio

@socketio.on('chat message')
def handle_message(senderID, receiverID, message): #函式名自訂
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
