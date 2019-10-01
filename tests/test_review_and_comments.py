from unittest.mock import Mock, MagicMock, patch
from django.contrib.messages.api import MessageFailure
from nose.tools import *
from posts.models import Post, Interaction, UserReviewRole, Review, Question, QuestionResponse
from django.contrib.auth.models import AnonymousUser, User as DjangoUser, Group
from django.test import Client, RequestFactory, TestCase

import posts.views
from posts.views import CreateQuestion, QuestionsView, ChangePostStatusToReviewView, \
                        RejectionView, AcceptReviewView, ReviewView, DeleteQuestionView, \
                        question_by_post, ChangePostToNeedChangesView, AddReviewCommentView, CreateQuestionResponseView, \
                        EditQuestionResponseView

from .test_posts import POST_DATA


class PostsReviewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = DjangoUser.objects.create_superuser('adminz', 'admizn@example.com', 'adminpass')
        self.user2 = DjangoUser.objects.create_superuser('Xtraadminz', 'xtra@example.com', 'adminpass')

        # g = Group.objects.get(name="reviser")
        g = Group(name="reviser")
        g.save()
        self.user.groups.add(g)
        self.user2.groups.add(g)
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

    @patch("posts.views.messages")
    def test_rejection_view(self, mock_message):
        self.test_view_send_to_review()
        riviu_aidi = Review.objects.first().id
        request = self.factory.get(f'/posts/{riviu_aidi}/reject/')
        request.user = self.user
        response = RejectionView.as_view()(request, review_id=riviu_aidi)

        request = self.factory.post(f'/posts/{riviu_aidi}/reject/', {"comment": "testno"})
        request.user = self.user
        response = RejectionView.as_view()(request, review_id=riviu_aidi)
        ##     messages.success(self.request, 'Post with id: %s has been rejected.' % post.pk)
        eq_(response.status_code, 302)

    @patch("posts.views.messages")
    def test_accept_review_view(self, mock_message):
        self.test_view_send_to_review()
        riviu_aidi = Review.objects.first().id
        request = self.factory.get(f'/posts/{riviu_aidi}/accept/')
        request.user = self.user
        response = AcceptReviewView.as_view()(request, review_id=riviu_aidi)
        eq_(response.status_code, 302)

    @patch("posts.views.messages")
    def test_accept_add_review_comment(self, mock_message):
        self.test_view_send_to_review()
        riviu_aidi = Review.objects.first().id
        request = self.factory.get(f'/posts/{self.post.id}/review/{riviu_aidi}/add_comment/', {'comment': "hey"})
        request.user = self.user
        response = AddReviewCommentView.as_view()(request, review_id=riviu_aidi)
        eq_(response.status_code, 200)

    @patch("posts.views.messages")
    def test_review_view(self, mock_message):
        self.test_view_send_to_review()
        riviu_aidi = Review.objects.first().id
        request = self.factory.get(f'/posts/{self.post.id}/review/{riviu_aidi}/')
        request.user = self.user
        response = ReviewView.as_view()(request, id=self.post.id, review_id=riviu_aidi)
        eq_(response.status_code, 200)

    @patch("posts.views.messages")
    def test_request_changes(self, mock_message):
        self.test_view_send_to_review()
        riviu_aidi = Review.objects.first().id
        request = self.factory.get(f'/posts/{riviu_aidi}/request_changes/')
        request.user = self.user
        response = ChangePostToNeedChangesView.as_view()(request, review_id=riviu_aidi)
        eq_(response.status_code, 302)


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
        ## Should validate on value
        # assert(response.status_code, 302)

    def test_get_questions(self):
        self.test_add_question()
        request = self.factory.get('/posts/questions/')
        request.user = self.user
        response = QuestionsView.as_view()(request)

    def test_get_questions_by_post(self):
        self.test_add_question()
        response = self.client.get(f'/posts/{self.post.id}/questions/')
        eq_(response.status_code, 200)

    def test_delete_post_question(self):
        self.test_add_question()
        q = Question.objects.first()
        request = self.factory.post(f'/posts/questions/{q.id}/delete/')
        request.user = self.user
        response = DeleteQuestionView.as_view()(request, id=q.id)
        eq_(response.status_code, 302)

    def test_get_replies(self):
        self.test_add_question()
        q = Question.objects.first()
        response = self.client.get(f'/posts/questions/{q.id}/replies/')

    @patch("posts.views.messages")
    def test_create_q_response_view(self, mock_message, data=None):
        self.test_add_question()
        q = Question.objects.first()
        if not data:
            data = {"id": q.id, "question": q.id, "response": "yeah!", "value": 0}
        request = self.factory.post(f'/posts/questions/{q.id}/responses/new/', data)
        request.user = self.user
        response = CreateQuestionResponseView.as_view()(request, id=q.id)
        eq_(response.status_code, 302)
        return QuestionResponse.objects.first()

    @patch("posts.views.messages")
    def test_edit_question_response_view(self, mock_message):
        qr = self.test_create_q_response_view()
        q = Question.objects.first()

        # request = self.factory.get(f'/posts/questions/{q.id}/responses/{qr.id}/edit/')
        # request.user = self.user
        # print(request)
        # response = EditQuestionResponseView.as_view()(request, response_id=qr.id)

        data = {"id": q.id, "question": q.id, "response": "yezh!", "value": 2}
        request = self.factory.post(f'/posts/questions/{q.id}/responses/{qr.id}/edit/', data=data)
        request.user = self.user
        response = EditQuestionResponseView.as_view()(request, response_id=qr.id, question_id=q.id)
        eq_(response.status_code, 302)
