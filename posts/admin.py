from django.contrib import admin
from posts import models

admin.site.register(models.Post)


class QuestionModel(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(models.Question, QuestionModel)


class QuestionResponseModel(admin.ModelAdmin):
    search_fields = ['question', 'response']


admin.site.register(models.QuestionResponse, QuestionResponseModel)
admin.site.register(models.Interaction)
admin.site.register(models.PostLocale)


admin.site.register(models.Response)
