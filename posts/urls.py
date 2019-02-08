from django.urls import path
from posts.views import HomeView, new_post, post, \
     edit_interaction, feedback, edit_post, create_tag, \
     tags, set_tag_to_post, get_tags_for_post, remove_tag_for_post, \
     StatisticsView, PostsListView

app_name = 'posts'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('<int:id>/', post, name="post"),
    path('new/', new_post, name="new"),
    path('interaction/<int:id>/edit/', edit_interaction, name="interaction-edit"),
    path('feedback/', feedback, name="feedback"),
    path('<int:id>/edit', edit_post, name="edit-post"),
    path('<int:id>/statistics/', StatisticsView.as_view(), name='post-statistics'),
    path('tags/create', create_tag, name="create-tag"),
    path('tags/', tags, name='tags'),
    path('<int:id>/set_tag', set_tag_to_post, name="set-tag-to-post"),
    path('<int:id>/get_tags', get_tags_for_post, name="get-tags-for-post"),
    path('<int:id>/remove_tag', remove_tag_for_post, name='remove-tag-for-post'),
    path('list/', PostsListView.as_view(), name="posts-list")
]
