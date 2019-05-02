from django.forms import ModelForm, Form, CharField, ChoiceField, RadioSelect, Select, IntegerField, BooleanField, Textarea
from posts.models import Post, Question


class CreatePostForm(Form):

    TYPE_CHOICES = (('embeded', 'Embeded'), ('youtube', 'Youtube'))

    name = CharField(label='Name')
    thumbnail = CharField(label='Thumbnail')
    new = BooleanField(label='New?', required=False)
    type = ChoiceField(widget=Select, choices=TYPE_CHOICES)
    min_range = IntegerField()
    max_range = IntegerField()
    area_id = IntegerField()
    content = CharField(label='Content')
    content_activity = CharField(label='Activity for FB. (Divide sections with | )', widget=Textarea)
    preview = CharField(widget=Textarea)


class UpdatePostFormModel(ModelForm):

    class Meta:
        model = Post
        fields = ['name', 'content', 'type', 'min_range', 'max_range', 'area_id', 'preview']


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ('name', 'post', 'replies')
