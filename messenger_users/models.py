from django.db import models


class User(models.Model):
    last_channel_id = models.CharField(max_length=50, unique=True)
    channel_id = models.CharField(max_length=50, null=True, unique=True)
    backup_key = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bot_id = models.IntegerField(default=1)
    username = models.CharField(max_length=100, null=True, unique=True)

    def __str__(self):
        return self.last_channel_id

    class Meta:
        app_label = 'messenger_users'


class UserData(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    data_key = models.CharField(max_length=30)
    data_value = models.TextField()

    def __str__(self):
        return self.data_value

    class Meta:
        app_label = 'messenger_users'
