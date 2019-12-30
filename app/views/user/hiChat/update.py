from flask import request, abort
from flask.views import MethodView
from flask_login import current_user

from app import socketio
from app.models.message import Message


class HiChatUpdate(MethodView):
    def get(self):
        pass

    def post(self):
        senderID = request.values["senderID"]
        receiverID = request.values["receiverID"]
        if receiverID != str(current_user.id):
            abort(403)

        Message.objects.filter(
            sender_id=senderID,
            receiver_id=receiverID,
            isRead=False).update(isRead=True)

        socketio.emit(receiverID + "updateTo" + senderID, broadcast=True)
        return ""
