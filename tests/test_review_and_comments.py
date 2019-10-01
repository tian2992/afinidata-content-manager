from unittest.mock import Mock, MagicMock
from django.contrib.messages.api import MessageFailure
from nose.tools import *
from posts.models import Post, Interaction, UserReviewRole, Review
from django.contrib.auth.models import AnonymousUser, User as DjangoUser, Group
from django.test import Client, RequestFactory, TestCase

from posts.views import CreateQuestion, QuestionsView, ChangePostStatusToReviewView
from .test_posts import POST_DATA

class PostsReviewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = DjangoUser.objects.create_superuser('adminz', 'admizn@example.com', 'adminpass')
        # g = Group.objects.get(name="reviser")
        g = Group(name="reviser")
        g.save()
        self.user.groups.add(g)
        self.post = Post(user=self.user, **POST_DATA)
        self.post.save()


    def test_unit_send_to_review(self):
        r = Review(post=self.post, comment="this is clem fandango here, can you hear me?")
        r.save()
        p = UserReviewRole(user=self.user, role='reviser', review=r)
        p.save()

    def test_view_send_to_review(self):
        self.post.status = 'draft'
        self.post.save()
        request = self.factory.post(f'/posts/{self.post.id}/send_to_review/', {"comment": "yeah test"})
        request.user = self.user
        response = ChangePostStatusToReviewView.as_view()(request, id=self.post.id)
        eq_(response.status_code, 302)
        pass

class PostsQuestionTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = DjangoUser.objects.create_superuser('adminz', 'admizn@example.com', 'adminpass')
        self.post = Post(user=self.user, **POST_DATA)
        self.post.save()

    def test_add_question(self):
        data = {"name": "test_q", "post": f"{self.post.id}", "replies": "yes, no , maybe, perhaps, whynot"}
        request = self.factory.post('/posts/questions/new/', data)
        request.user = self.user
        response = CreateQuestion.as_view()(request)
        eq_(response.status_code, 302)

    def test_get_questions(self):
        self.test_add_question()
        request = self.factory.get('/posts/questions/')
        request.user = self.user
        response = QuestionsView.as_view()(request)

    def test_delete_post_question(self):
        request = self.factory.post('/posts/questions//delete/')
        request.user = self.user
        response = CreateQuestion.as_view()(request)
        eq_(response.status_code, 200)