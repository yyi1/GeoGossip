from channels.auth import channel_session_user_from_http
from channels.auth import channel_session_user
from channels import Group
from django.utils.timezone import get_current_timezone
import models
import forms
import json
import datetime
import logging

EPOCH = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=get_current_timezone())
logger = logging.getLogger(__name__)


# Connected to websocket.connect
@channel_session_user_from_http
def connect(message):
    group_id = message['path'].strip('/')
    if models.Group.objects.filter(id=group_id).exists():
        Group(group_id).add(message.reply_channel)
        Group(group_id).send({
            'text': json.dumps({
                'type': 'online',
                'username': message.user.username,
                'time': (datetime.datetime.now(tz=get_current_timezone()) - EPOCH).total_seconds() * 1000
            })
        })
        pass
    pass


# Connected to websocket.receive
@channel_session_user
def receive(message):
    group_id = message['path'].strip('/')
    try:
        if models.Group.objects.filter(id=group_id).exists():
            group = models.Group.objects.get(id=group_id)
            user = message.user
            content = message['text']
            message_form = forms.MessageForm({'content': content})
            if message_form.is_valid():
                new_message = models.Message(group=group, user=user, content=content)
                try:
                    new_message.save()
                    pass
                except Exception as e:
                    logger.error(e.message)
                    pass
                Group(group_id).send({
                    'text': json.dumps({
                        'type': 'message',
                        'username': user.username,
                        'user_id': user.id,
                        'content': content,
                        'time': (new_message.created_on - EPOCH).total_seconds() * 1000
                    })
                })
                pass
            pass
        else:
            Group(group_id).send({
                'text': json.dumps({
                    'type': 'alert',
                    'content': 'This group has been deleted. Please go back to the main view or log out.'
                })
            })
            pass
        pass
    except Exception as e:
        logger.error(e.message)
        pass
    pass


# Connected to websocket.disconnect
@channel_session_user
def disconnect(message):
    group_id = message['path'].strip('/')
    if models.Group.objects.filter(id=group_id).exists():
        Group(group_id).discard(message.reply_channel)
        Group(group_id).send({
            'text': json.dumps({
                'type': 'offline',
                'username': message.user.username,
                'time': (datetime.datetime.now(tz=get_current_timezone()) - EPOCH).total_seconds() * 1000
            })
        })
        pass
    pass
