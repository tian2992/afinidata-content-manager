from django.urls import path
from posts.views import HomeView, new_post, post

app_name = 'posts'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('<int:id>/', post, name="post"),
    path('new/', new_post, name="new")
]
