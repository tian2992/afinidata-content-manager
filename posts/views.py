from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'posts/index.html'


class PostView(TemplateView):

    template_name = 'posts/post.html'

    def get_context_data(self, *args, **kwargs):

        id = kwargs['id']

        return dict(id=id)