from django.urls import path
from posts.views import HomeView, PostView

app_name = 'posts'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('<int:id>/', PostView.as_view(), name="posts")
]
