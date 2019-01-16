from django.forms import ModelForm, Form, CharField, TextInput, ChoiceField, RadioSelect
from posts.models import Post


class CreatePostForm(Form):

    TYPE_CHOICES = (('embeded', 'Embeded'), ('video', 'Video'))

    name = CharField(label='Name to post')
    content = CharField(label='Content')
    type = ChoiceField(widget=RadioSelect, choices=TYPE_CHOICES)


class CreatePostFormModel(ModelForm):

    class Meta:
        model = Post
        fields = ['name', 'content', 'type']