from django.db import models


class Post(models.Model):
    name = models.CharField(max_length=255)
    pretty_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Interaction(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    messenger_id = models.CharField(default="", max_length=50)
    type = models.CharField(max_length=255, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.messenger_id