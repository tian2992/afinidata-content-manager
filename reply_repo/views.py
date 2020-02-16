from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from reply_repo import models
import json
#from posts.models import Post, Interaction
#from messenger_users.models import User, UserData

@csrf_exempt
def index(request):
    '''{
     "messages": [
       {"text": "Welcome to the Chatfuel Rockets!"},
       {"text": "What are you up to?"}
     ]
    }'''
    print (request.body)
    data = json.loads(request.body)
    if not data['locale']:
        raise Http404
    if not data['block_id']:
        raise Http404
    d = data['locale'].split('_')
    if len(d) != 2:
        raise Http404
    language = d[0]
    region = d[1]
    message = models.Message.objects.filter(
            block_id = data['block_id']
        ).filter(
            full_locale = data['locale']
        )
    message = list(message)
    if len(message) > 0:
        message = message[0]
        return JsonResponse(dict(messages=[dict(text=message.content)]))
    if not message:
        message = models.Message.objects.filter(
                block_id = data['block_id']
            ).filter(
                language = language
            )
    message = list(message)
    if len(message) > 0:
        message = message[0]
        return JsonResponse(dict(messages=[dict(text=message.content)]))
    if not message:
        message = models.Message.objects.filter(
                block_id = data['block_id']
            )
    message = list(message)
    if len(message) > 0:
        message = message[0]
        return JsonResponse(dict(messages=[dict(text=message.content)]))
    if not message:
        message = 'Error - No block found for block_id %s and locale %s.' % (data['block_id'],
                                                                             data['locale'])
    return JsonResponse(dict(messages=[dict(text=message)]))
