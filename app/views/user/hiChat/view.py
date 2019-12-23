import datetime

from flask import redirect, render_template, url_for, flash, request, abort
from flask.views import MethodView
from flask_login import current_user

from app.models.user import User
from app.models.message import Message

from mongoengine.queryset.visitor import Q

class HiChatView(MethodView):
    def get(self):
        messagesOwners = Message.objects(Q(sender_id=current_user.id) | Q(receiver_id=current_user.id)).aggregate(
            {
                '$lookup': {
                    'from': 'user',
                    'localField': 'sender_id' ,
                    'foreignField': '_id',
                    'as': 'userS'
                }
            },
            {
                '$lookup': {
                    'from': 'user',
                    'localField': 'receiver_id' ,
                    'foreignField': '_id',
                    'as': 'userR'
                }
            },
            {
                '$addFields': {
                    'current_user': current_user.id
                }
            },
            {
                '$lookup': {
                    'from': 'user',
                    'localField': 'current_user' ,
                    'foreignField': '_id',
                    'as': 'userC'
                }
            },
            {
                '$addFields': {
                    'userSR': {
                        '$let': {
                            'vars': {
                                'userSS': '$userS',
                                'userRR': '$userR'
                            },
                            'in': { '$setUnion': [ '$$userSS', '$$userRR' ] }
                        }
                    }
                }
            },
            {
                '$group': {
                    '_id': {
                        '$setDifference': [ '$userSR', '$userC']
                    },
                    'create_time': {
                        '$max': '$create_time'
                    }
                }
            })

        users = list(messagesOwners)
        for u in users:
            if(len(u['_id']) == 0):
                dummyCurrentUserDict = {
                    '_id': current_user.id,
                    'name': current_user.name
                }
                u['_id'].append(dummyCurrentUserDict)

        users = sorted(users, key = lambda i: i['create_time'], reverse=True)

        return render_template('user/hichatT.html', Tusers=User.objects, users=users, currentUser=current_user)

    def post(self):
        receiverID = request.values["receiverID"]
        messages = Message.objects((Q(sender_id=current_user) & Q(receiver_id=receiverID)) | (Q(sender_id=receiverID) & Q(receiver_id=current_user))).order_by("+create_time")
        return messages.to_json()