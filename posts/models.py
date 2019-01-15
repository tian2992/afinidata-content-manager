from django.db import models

class Post(models.Model):
    name = models.CharField(max_length=255)
    pretty_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)