from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from posts.models import Post, Interaction
from messenger_users.models import User, UserData


def index(request):
    return JsonResponse(dict(hello="world"))


class DashView(TemplateView):
    template_name = 'dash/index.html'

    def get_context_data(self, **kwargs):
        posts = Post.objects.all()
        users = User.objects.all()
        interactions = Interaction.objects.all()
        users_data = UserData.objects.all()

        return dict(posts=posts, users=users, interactions=interactions, users_data=users_data)
