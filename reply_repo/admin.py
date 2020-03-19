from django.contrib import admin

from reply_repo import models


class MessageModel(admin.ModelAdmin):
    search_fields = ['block_id', 'content']


admin.site.register(models.Message, MessageModel)
