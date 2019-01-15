from django.views.generic import TemplateView
from posts.models import Post
from django.http import Http404
from django.shortcuts import get_object_or_404



class HomeView(TemplateView):
    template_name = 'posts/index.html'


class PostView(TemplateView):

    template_name = 'posts/post.html'

    def get_context_data(self, *args, **kwargs):

        post = get_object_or_404(Post, id=kwargs['id'])

        return dict(post=post)