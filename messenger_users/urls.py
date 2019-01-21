from django.urls import path
from messenger_users.views import new_user

app_name = 'messenger_users'

urlpatterns = [
    path('new/', new_user, name="new")
]
