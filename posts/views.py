from django.views.generic import TemplateView
from posts.models import Post, Interaction, Feedback
from django.shortcuts import get_object_or_404, render
from posts.forms import CreatePostFormModel, CreatePostForm
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


class HomeView(TemplateView):
    template_name = 'posts/index.html'


def post(request, id):

    if request.method == 'GET':
        post = Post.objects.get(id=id)
        try:
            channel_id = request.GET['channel_id']
            bot_id = request.GET['bot_id']
            Interaction\
                .objects\
                .create(
                    post=post,
                    channel_id=channel_id,
                    bot_id=bot_id,
                    type='opened'
            )
            post_session = Interaction(post=post,
                                       channel_id=channel_id,
                                       bot_id=bot_id,
                                       type='session')
            post_session.save()
            return render(request, 'posts/post.html',
                          {'post': post, 'session_id': post_session.pk})
        except:
            pass

        return render(request, 'posts/post.html', {'post': post, 'session_id': 'null'})


def new_post(request):

    form = CreatePostFormModel(request.POST or None)

    if form.is_valid():

        post = form.save()

        return JsonResponse(dict(
            status='created',
            post=dict(
                id=str(post.id),
                name=str(post.name)
            )
        ))

    try:
        if request.GET['quest'] == 'afini':

            return render(request, 'posts/new.html', {'form': form})

        else:
            raise Http404('Not found')
    except:
        raise Http404('Not found')

@csrf_exempt
def edit_interaction(request, id):

    if request.method == 'POST':

        print(request.POST)

        try:
            interaction = Interaction.objects.filter(pk=id).update(minutes=request.POST['minutes'])
            return JsonResponse(dict(
                status='updated',
                interaction=interaction
            ))
        except:
            raise Http404('Error')

    else:
        return JsonResponse(dict(hello="world"))


@csrf_exempt
def feedback(request):
    if request.method == 'POST':
        try:
            if request.POST \
               and len(request.POST) >= 4 \
               and request.POST['bot_id'] \
               and request.POST['channel_id'] \
               and request.POST['post_id'] \
               and request.POST['value']:
                print(request.POST)
                active_feedback = Feedback.objects.filter(bot_id=request.POST['bot_id'],
                                                          channel_id=request.POST['channel_id'],
                                                          post_id=request.POST['post_id'])
                if not active_feedback:
                    if 1 <= int(request.POST['value']) <= 5:
                        new_feedback = Feedback.objects.create(bot_id=request.POST['bot_id'],
                                                               channel_id=request.POST['channel_id'],
                                                               post_id=request.POST['post_id'],
                                                               value=request.POST['value'])

                        return JsonResponse(dict(status='created',
                                                 data=dict(
                                                     id=new_feedback.pk,
                                                     post_id=new_feedback.post_id,
                                                     channel_id=new_feedback.channel_id,
                                                     bot_id=new_feedback.bot_id,
                                                     value=new_feedback.value
                                                 )))
                    else:
                        return JsonResponse(dict(status='error',
                                                 error='value is not valid'))
                else:
                    change_feedback = Feedback.objects.get(bot_id=request.POST['bot_id'],
                                                           channel_id=request.POST['channel_id'],
                                                           post_id=request.POST['post_id'])

                    if change_feedback.value != int(request.POST['value']) \
                       and 1 <= int(request.POST['value']) <= 5:

                        change_feedback.value = request.POST['value']
                        change_feedback.save(update_fields=['value'])
                        return JsonResponse(dict(status='updated',
                                                 data=dict(
                                                     id=change_feedback.pk,
                                                     post_id=change_feedback.post_id,
                                                     channel_id=change_feedback.channel_id,
                                                     bot_id=change_feedback.bot_id,
                                                     value=change_feedback.value
                                                 )))
                    else:
                        return JsonResponse(dict(status='not-updated',
                                                 data=dict(
                                                     id=change_feedback.pk,
                                                     post_id=change_feedback.post_id,
                                                     channel_id=change_feedback.channel_id,
                                                     bot_id=change_feedback.bot_id,
                                                     value=change_feedback.value
                                                 )))

            else:
                return JsonResponse(dict(status='error',
                                         error='invalid params'))
        except Exception as e:
            return JsonResponse(dict(status='error',
                                     error='invalid params'))

    else:
        raise Http404('Not found')