import datetime

from flask import abort
# from flask_socketio import emit  # for using emit in socketio.on function
from app.models.user import User
from app.models.message import Message
from flask_login import current_user

from app import socketio


class socketServiceOn():

    def __init__(self):
        @socketio.on('client send message')
        def handle_message(senderID, receiverID, message):  # 函式名自訂
            if(senderID != str(current_user.id)):
                abort(403)
            sendMessageViaSocketIO(senderID, receiverID, message)


def updatePriceViaSocketIO(product_id, newPrice):
    socketio.emit(str(product_id), {'newPrice': newPrice}, broadcast=True)


def sendMessageViaSocketIO(senderID, receiverID, message):
    sender = User.objects.get(id=senderID)

    messageDocument = Message(
        sender_id=sender,
        receiver_id=receiverID,
        message=message,
        create_time=datetime.datetime.utcnow())
    messageDocument.save()

    data = {
        "sender_id": {
            "$oid": senderID,
            "name": sender.name
        },
        "message": message,
        "messageID": str(messageDocument.id),
        "isRead": messageDocument.isRead
    }
    if receiverID != senderID:
        socketio.emit(senderID + 'To' + receiverID, data, broadcast=True)
        socketio.emit('messageTo' + receiverID, data, broadcast=True)
    # send to object
    # if receiverID != senderID:
    #     socketio.emit(receiverID + 'To' + senderID, data, broadcast=True)
    #     socketio.emit('messageTo' + senderID, data, broadcast=True)
    # send to sender
