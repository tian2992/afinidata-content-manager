from django.forms import ModelForm, Form, CharField, ChoiceField, RadioSelect, Select, IntegerField, BooleanField, Textarea
from posts import models


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
        model = models.Post
        fields = ['name', 'content', 'type', 'min_range', 'max_range', 'area_id', 'preview']


class QuestionForm(ModelForm):

    class Meta:
        model = models.Question
        fields = ('name', 'post', 'replies')


class ReviewCommentForm(ModelForm):

    class Meta:
        model = models.ReviewComment
        fields = ('comment',)


class QuestionResponseForm(ModelForm):

    class Meta:
        model = models.QuestionResponse
        fields = ('response', 'value')
