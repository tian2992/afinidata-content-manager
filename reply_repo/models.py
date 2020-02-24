from django.db import models
import random
import string


class Message(models.Model):
    block_id = models.CharField(max_length=255, null=False, unique=False, default='')
    language = models.CharField(max_length=2, null=False)
    full_locale = models.CharField(max_length=5, null=False)
    content = models.TextField()
    extra_items = models.TextField(default='')

    def __str__(self):
        return "%s - %s - %s" %(self.block_id, self.language, self.full_locale)
