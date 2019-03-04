from django.urls import path
from posts.views import HomeView, new_post, post, \
     edit_interaction, feedback, edit_post, create_tag, \
     tags, set_tag_to_post, get_tags_for_post, remove_tag_for_post, \
     StatisticsView, PostsListView, set_user_send, post_by_limits, \
     QuestionsView, CreateQuestion, EditQuestion, QuestionView, \
     question_by_post, set_interaction_to_post, get_thumbnail_by_post, \
     create_response_for_cuestion

app_name = 'posts'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('<int:id>/', post, name="post"),
    path('new/', new_post, name="new"),
    path('<int:id>/set_interaction/', set_interaction_to_post, name='set_interaction'),
    path('<int:id>/thumbnail/', get_thumbnail_by_post, name='get_thumbnail'),
    path('interaction/<int:id>/edit/', edit_interaction, name="interaction-edit"),
    path('feedback/', feedback, name="feedback"),
    path('<int:id>/edit', edit_post, name="edit-post"),
    path('<int:id>/statistics/', StatisticsView.as_view(), name='post-statistics'),
    path('tags/create', create_tag, name="create-tag"),
    path('tags/', tags, name='tags'),
    path('<int:id>/set_tag', set_tag_to_post, name="set-tag-to-post"),
    path('<int:id>/get_tags', get_tags_for_post, name="get-tags-for-post"),
    path('<int:id>/remove_tag', remove_tag_for_post, name='remove-tag-for-post'),
    path('list/', PostsListView.as_view(), name="posts-list"),
    path('set_user_send/', set_user_send, name='set-user-send'),
    path('by_limit/', post_by_limits, name='posts_by_limit'),
    path('questions/<int:id>/', QuestionView.as_view(), name='question'),
    path('questions/', QuestionsView.as_view(), name='questions'),
    path('questions/new/', CreateQuestion.as_view(), name='new-question'),
    path('questions/<int:id>/edit/', EditQuestion.as_view(), name='edit-question'),
    path('<int:id>/questions/', question_by_post, name='question_by_post'),
    path('questions/<int:id>/response/', create_response_for_cuestion, name='response_for_cuestion')
]
