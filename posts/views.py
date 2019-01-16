from django.views.generic import TemplateView
from posts.models import Post, Interaction
from django.shortcuts import get_object_or_404, render
from posts.forms import CreatePostFormModel, CreatePostForm
from django.http import JsonResponse


class HomeView(TemplateView):
    template_name = 'posts/index.html'

def post(request, id):

    if request.method == 'GET':
        post = Post.objects.get(id=id)
        try:
            messenger_id = request.GET['messenger_id']
            Interaction\
                .objects\
                .create(
                    post=post,
                    messenger_id=messenger_id,
                    type='opened'
            )
        except:
            pass

        return render(request, 'posts/post.html', {'post': post})


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

    return render(request, 'posts/new.html', {'form': form})

