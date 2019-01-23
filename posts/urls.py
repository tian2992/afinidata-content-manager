from django.urls import path
from posts.views import HomeView, new_post, post, edit_interaction

app_name = 'posts'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('<int:id>/', post, name="post"),
    path('new/', new_post, name="new"),
    path('interaction/<int:id>/edit/', edit_interaction, name="interaction-edit")
]
