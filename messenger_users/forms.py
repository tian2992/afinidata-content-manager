from django.forms import ModelForm
from messenger_users.models import User, UserData


class CreateUserFormModel(ModelForm):

    class Meta:
        model = User
        fields = ['last_channel_id', 'backup_key']


class CreateUserDataFormModel(ModelForm):

    class Meta:
        model = UserData
        fields = ['data_key', 'data_value', 'user']