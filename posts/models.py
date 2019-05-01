from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES = (
    ('draft', 'draft'),
    ('review', 'review'),
    ('private', 'private'),
    ('published', 'published')
)

REVIEW_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('completed', 'Completed')
)

POST_TYPE_CHOICES = (
    ('embeded', 'embeded'),
    ('youtube', 'youtube')
)


class Post(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(choices=STATUS_CHOICES, max_length=255, default='review')
    pretty_name = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, default='embeded', choices=POST_TYPE_CHOICES)
    content = models.TextField(null=True)
    content_activity = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    min_range = models.IntegerField(null=True, default=0)
    max_range = models.IntegerField(null=True, default=72)
    preview = models.TextField(null=True)
    new = models.BooleanField(default=False, null=True)
    thumbnail = models.TextField(null=True)
    area_id = models.IntegerField(null=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Interaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user_id = models.IntegerField(default=0)
    username = models.CharField(max_length=255, null=True)
    channel_id = models.CharField(default="", max_length=50)
    bot_id = models.IntegerField(default=1)
    type = models.CharField(max_length=255, default='open')
    value = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.channel_id


class Feedback(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user_id = models.IntegerField(default=0)
    username = models.CharField(max_length=255, null=True)
    channel_id = models.CharField(default="", max_length=50)
    bot_id = models.IntegerField(default=1)
    value = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.channel_id


class Label(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=255, unique=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    replies = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    response = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.CharField(choices=REVIEW_STATUS_CHOICES, default='pending', max_length=20)
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, through='UserReviewRole')

    def __str__(self):
        return "%s__%s__%s" % (self.pk, self.status, self.post.pk)


REVIEW_ROLE_CHOICES = (('author', 'author'), ('reviser', 'reviser'))


class UserReviewRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(choices=REVIEW_ROLE_CHOICES, default='author', max_length=20)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


class Approbation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return "%s__%s__%s" % (self.pk, self.user.first_name, self.review.pk)


class Rejection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    comment = models.TextField(null=True)

    def __str__(self):
        return "%s__%s__%s" % (self.pk, self.user.first_name, self.review.pk)
