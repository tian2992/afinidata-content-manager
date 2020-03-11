from django.contrib import admin
from django.urls import path
from reply_repo.views import index, download_messages, upload_messages, fix_messages_view

app_name = 'dash'

urlpatterns = [
    path('', index, name="index"),
    path('fix_core', fix_messages_view(), name='fixer'),
    path('download', download_messages, name="down"),
    path('upload', upload_messages, name="up")
]
