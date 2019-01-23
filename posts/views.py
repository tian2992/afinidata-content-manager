from django.views.generic import TemplateView
from posts.models import Post, Interaction
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
