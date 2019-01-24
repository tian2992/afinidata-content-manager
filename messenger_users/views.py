from django.shortcuts import render
from messenger_users.models import User, UserData
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from messenger_users.forms import CreateUserFormModel


@csrf_exempt
def new_user(request):

    if request.method == 'POST':
        form = CreateUserFormModel(request.POST or None)

        if form.is_valid():
            user = form.save()

            params = dict(request.POST)

            del params['last_channel_id']
            del params['backup_key']
            del params['bot_id']

            for param in params:
                UserData.objects.create(
                    user=user,
                    data_key=str(param),
                    data_value=str(params[param][0])
                )

            return JsonResponse(dict(
                status='created',
                data=dict(
                    id=user.id,
                    last_channel_id=user.last_channel_id,
                    backup_key=user.backup_key
                )
            ))

        else:
            return JsonResponse(dict(
                status="error",
                error="Invalid Params"
            ))
    else:
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