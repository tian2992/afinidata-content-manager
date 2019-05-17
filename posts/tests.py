from django.test import TestCase, RequestFactory
from posts import models
from django.contrib.auth.models import User, AnonymousUser
from posts import views
from messenger_users import models as user_models


class PostTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='testuser', password='123456')
        models.Post.objects.create(name='test 01', thumbnail='adsfasdf', new=True, min_range=5, max_range=20,
                            content='adsfadsf', content_activity='asdfasdf', user=user)

    def post_has_created(self):
        post = models.Post.objects.get(name='test 01')
        self.assertEqual(post.new, True)

    def post_has_updated(self):
        post = models.Post.objects.get(name='test 01')
        post.new = False
        post.save()
        self.assertNotEqual(post.new, True)

    def post_has_user(self):
        user = User.objects.get(username='testuser')
        post = models.Post.objects.get(name='test 01')
        self.assertEqual(post.user, user)


class InteractionTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='testuser', password='123456')
        post = models.Post.objects.create(name='test post', thumbnail='adsfasdf', new=True, min_range=5, max_range=20,
                            content='adsfadsf', content_activity='asdfasdf', user=user)
        interaction = models.Interaction.objects.create(post=post, user_id=1, username='user_1', channel_id='12345',
                                                        bot_id=1, type='session', value=1)

    def interaction_has_created(self):
        interaction = models.Interaction.objects.get(id=1)
        self.assertNotEqual(interaction.created_at, None)
        self.assertNotEqual(interaction.updated_at, None)

    def interaction_has_updated(self):
        interaction = models.Interaction.objects.get(id=1)
        interaction.type = 'opened'
        interaction.save()
        self.assertNotEqual(interaction.type, 'session')


class FeedbackTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='testuser', password='123456')
        self.post = models.Post.objects.create(name='test post', thumbnail='adsfasdf', new=True, min_range=5,
                                               max_range=20, content='adsfadsf', content_activity='asdfasdf', user=user)
        self.second_post = models.Post.objects.create(name='test post 02', thumbnail='adsfasdf', new=True, min_range=5,
                                                      max_range=20, content='adsfadsf', content_activity='asdfasdf',
                                                      user=user)

        feedback = models.Feedback.objects.create(post=self.post, user_id=1, username='user_1', channel_id='12345',
                                                  bot_id=1, value=1)
        self.messenger_user = user_models.User.objects.create(username='user_1', channel_id='12345', backup_key='12345',
                                                              last_channel_id='12345', bot_id=1)
        self.factory = RequestFactory()

    def feedback_has_created(self):
        request = self.factory.post('posts/feedback/', dict(username=self.messenger_user.username,
                                                            post_id=self.second_post.pk, bot_id=1, value=5))
        request.user = AnonymousUser()
        response = views.feedback(request)
        new_feedback = models.Feedback.objects.get(id=2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_feedback.value, 5)

    def feedback_has_updated(self):
        request = self.factory.post('posts/feedback/', dict(username=self.messenger_user.username,
                                                            post_id=self.post.pk, bot_id=1, value=2))
        request.user = AnonymousUser()
        response = views.feedback(request)
        feedback = models.Feedback.objects.get(pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(feedback.value, 2)

