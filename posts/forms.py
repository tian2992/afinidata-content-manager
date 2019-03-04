from django.forms import ModelForm, Form, CharField, ChoiceField, RadioSelect, Select, IntegerField
from posts.models import Post, Question


class CreatePostForm(Form):

    TYPE_CHOICES = (('embeded', 'Embeded'), ('youtube', 'Youtube'))

    name = CharField(label='Name to post')
    content = CharField(label='Content')
    type = ChoiceField(widget=Select, choices=TYPE_CHOICES)
    author = CharField(label='Author')
    min_range = IntegerField()
    max_range = IntegerField()
    area_id = IntegerField()
    preview = CharField()
    thumbnail = CharField(label='Thumbnail')


class UpdatePostFormModel(ModelForm):

    class Meta:
        model = Post
        fields = ['name', 'content', 'type', 'author', 'min_range', 'max_range', 'area_id', 'preview']


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ('name', 'post')
