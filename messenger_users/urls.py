from django.urls import path
from messenger_users.views import new_user, add_attribute

app_name = 'messenger_users'

urlpatterns = [
    path('new/', new_user, name="new"),
    path('<channel_id>/add_attribute/', add_attribute, name="add_attribute")
]
