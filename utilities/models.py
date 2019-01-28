from django.db import models


class Web2pyData(models.Model):

    class Meta:
        app_label = 'utilities'

    answer_timestamp = models.DateTimeField(auto_now_add=True)
    messenger_id = models.CharField(max_length=30)
    answer = models.CharField(max_length=255)
    field = models.IntegerField(default=0)