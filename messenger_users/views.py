from django.shortcuts import render
from messenger_users.models import User, UserData
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import slugify
from messenger_users.forms import CreateUserFormModel

import random
import string
import logging

logger = logging.getLogger(__name__)

## FIXME: convert to django rest views.

'''Creates user from a request.'''
@csrf_exempt
def new_user(request):


    # hackish hak :( for chatfuel mishap
    c_fid = request.POST.get("chatfuel_id")

    if c_fid:
        # we're in
        muid = request.POST['messenger_user_id']
        us = User.objects.get(last_channel_id=c_fid)
        us.last_channel_id = muid

    if request.method == 'POST':

        ### TODO: Split in functions, should not be named new_user smth like refresh session (?)

        found_user = None
        try:
            found_user = User.objects.get(last_channel_id=request.POST['messenger_user_id'])
            logger.info('user id found')
        except:
            logger.error(request.POST)
            logger.error('user could not be found from user id')

        if found_user:
            return JsonResponse(dict(
                            set_attributes=dict(
                                hasLoggedIn=True,
                                username=found_user.username
                            ),
                            messages=[]
                        ))

        else:
            logger.warning('Creating New User')
            user = dict(bot_id=None, last_channel_id=None, backup_key=None)
            logger.info(request.POST)

            try:
                mess_id = request.POST['messenger_user_id']
            except:
                logger.error(exc_info=True)
                logger.error("no messenger_user_id try messenger user id ")
                mess_id = request.POST['messenger user id']

            fname = request.POST.get('first_name', "no{}".format(mess_id))
            lname = request.POST.get('last_name', "no{}".format(mess_id))

            user['last_channel_id'] = mess_id
            user['username'] = slugify(fname + lname)
            user['backup_key'] = user['username']+request.POST['messenger_user_id']
            user['bot_id'] = request.POST['bot_id']
            user_to_save = User(**user)
            user_to_save.save()

            UserData.objects.create(user=user_to_save, data_key='channel_first_name', data_value=fname)
            UserData.objects.create(user=user_to_save, data_key='channel_last_name', data_value=lname)

            logger.warning("Created user")
            logger.warning(user_to_save)

            return JsonResponse(dict(
                            set_attributes=dict(
                                username=user_to_save.username,
                                backup_key=user['backup_key'],
                                user_id=user_to_save.pk
                            ),
                            messages=[]
                        ))
    else:
        logger.error("New user only POST valid.")
        raise Http404('Not auth')


@csrf_exempt
def add_attribute(request, channel_id):

    users = User.objects.filter(channel_id=channel_id)
    user = None
    if users:
        user = users[0]
    else:
        users = User.objects.filter(last_channel_id=channel_id)
        if users:
            user = users[0]

    if request.method == 'POST':
        if not user:
            return JsonResponse(dict(status="error", error="User not exists with channel id: {}".format(channel_id)))
        else:
            results = []
            for param in request.POST:
                UserData.objects.create(
                    user=user,
                    data_key=str(param),
                    data_value=str(request.POST[param])
                )
                results.append(dict(attribute=param, value=request.POST[param]))
            print(request.POST)
            return JsonResponse(dict(status="finished", data=dict(user_id=user.pk, added_attributes=results)))
    else:
        return JsonResponse(dict(hello='world'))


@csrf_exempt
def by_username(request, username):
    print(username)
    if request.method == 'POST':
        return JsonResponse(dict(status='error', error='Invalid method'))
    else:
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            logger.error("No username")
            return JsonResponse(dict(status='error', error=str(e)))

        return JsonResponse(dict(
                                set_attributes=dict(
                                    user_id=user.pk
                                ),
                                messages=[]
                            ))
