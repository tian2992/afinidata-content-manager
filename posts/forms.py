from django.forms import ModelForm, Form, CharField, ChoiceField, RadioSelect, Select
from posts.models import Post


class CreatePostForm(Form):

    TYPE_CHOICES = (('embeded', 'Embeded'), ('youtube', 'Youtube'))

    name = CharField(label='Name to post')
    content = CharField(label='Content')
    type = ChoiceField(widget=Select, choices=TYPE_CHOICES)
    author = CharField(label='Author')


class CreatePostFormModel(ModelForm):

    class Meta:
        model = Post
        fields = ['name', 'content', 'type', 'author']