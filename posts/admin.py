from django.contrib import admin
from posts import models

admin.site.register(models.Post)
admin.site.register(models.Question)
admin.site.register(models.QuestionResponse)
admin.site.register(models.Interaction)
admin.site.register(models.PostLocale)

admin.site.register(models.Response)
