from django.forms import ModelForm
from messenger_users.models import User


class CreateUserFormModel(ModelForm):

    class Meta:
        model = User
        fields = ['last_channel_id', 'backup_key']