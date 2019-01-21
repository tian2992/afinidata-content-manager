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