from flask_sqlalchemy import SQLAlchemy
import os
from twilio.rest import Client

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Queue:
    def __init__(self):
        self._queue = []
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'FIFO'
        self.account_sid = 'AC18644d2be962e1a1a79ef5fea23d6607'
        self.auth_token = 'ac86119709ea85e97bbf53c26180f9b7'
        self.client = Client(self.account_sid, self.auth_token)

    def enqueue(self, user):
        if self.size() == 0:
            message = self.client.messages \
                .create(
                     body="Hola "+ user['name']+' ,es tu turno.',
                     from_='+19519633790',
                     to='+56961339843'
                 )
        else:
            message = self.client.messages \
                .create(
                     body="Hola "+ user['name']+' bienvenido/a, '+str(self.size())+' personas se encuentran antes de ti, por favor espera tu turno.',
                     from_='+19519633790',
                     to='+56961339843'
                 )

        self._queue.append(user)


    def dequeue(self):
        if self.size() > 0:
            if self._mode == 'FIFO':
                message = self.client.messages \
                .create(
                    body="Hola "+ self._queue[1]["name"]+' ,es tu turno.',
                    from_='+19519633790',
                    to='+56961339843'
                )
                next_user = self._queue.pop(0)
                return next_user
            elif self._mode == 'LIFO':
                next_user = self._queue.pop(-1)
                return next_user
        else:
            msg = {
                "msg": "No items in Queue"
            }
            return msg

    def get_queue(self):
        return self._queue

    def size(self):
        return len(self._queue)