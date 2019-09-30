import unittest.mock
from django.contrib.messages.api import MessageFailure
from nose.tools import *
from posts.models import Post, Interaction
from django.contrib.auth.models import AnonymousUser, User as DjangoUser
from django.test import Client, RequestFactory, TestCase
from posts.views import HomeView, NewPostView, fetch_post


class PostsTest(TestCase):
    def make_a_user(self):
        if not hasattr(self, "user"):
            self.user = DjangoUser(
                  username='itest', password='secret')
            #     username='jtest', channel_id=1, last_channel_id=1, recovery_key='top_secret')
            self.user.save()

    def test_creation_posts(self):
        self.make_a_user()
        post_name = "tester"
        post = Post(name=post_name, status='draft', user=self.user)
        post.save()
        eq_(post_name,post.name)

    def test_update_post(self):
        self.make_a_user()
        post = Post(name="tester", status='draft', user=self.user)
        post.save()
        newval = "test2"
        post.name = newval
        post.save()
        eq_(post.name, newval)

    def test_create_old_interaction(self):
        us_id, us_name = 123, "testuser"
        interact = Interaction(user_id=us_id, username=us_name)
        eq_(interact.user_id, us_id)


class PostsViewsTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.POST_DATA = {"name": 'test',
                          'thumbnail': "http://afinidata.com/logo.png",
                          'min_range': 5,
                          'max_range': 32,
                          'content': "http://sample.afinidata.com",
                          'content_activity': "test test test",
                          'preview': 'previu'
                          }
        self.factory = RequestFactory()
        self.client = Client()
        self.user = DjangoUser.objects.create_user(
            username='jacob', email='jacob@example.com', password='top_secret')

    def save_post(self):
        self.post = Post(user = self.user, **self.POST_DATA)
        self.post_id = self.post.save()
        return self.post_id


    @raises(AttributeError)
    def test_fail_create_post(self):
        datao = self.POST_DATA
        request = self.factory.post('/posts/new', datao)
        response = NewPostView.as_view()(request)
        eq_(response.status_code, 500)


    def test_get_home_view(self):
        request = self.factory.get('/posts/')
        request.user = self.user
        response = HomeView.as_view()(request)
        eq_(response.status_code, 200)


    def test_create_post(self):
        datao = self.POST_DATA
        response = self.client.post('/posts/new/', datao)
        eq_(response.status_code, 302)


    def test_fetch_post(self):
        p_id = self.save_post()
        print(Post.objects.get().id)
        p_id = 1
        response = self.client.get('/posts/{}/'.format(p_id))
        eq_(response.status_code, 200)


    @raises(Post.DoesNotExist)
    def test_fail_fetch_post(self):
        request = self.factory.get('/posts/123/')
        request.user = AnonymousUser()
        response = fetch_post(request, 123)
        eq_(response.status_code, 404)

    #
    # def test_details(self):
    #     # Create an instance of a GET request.
    #     request = self.factory.get('/123/')
    #
    #     request.user = AnonymousUser()
    #
    #     # Test my_view() as if it were deployed at /customer/details
    #     response = fetch_post(request, 123)
    #     # Use this syntax for class-based views.
    #     #response = MyView.as_view()(request)
    #     self.assertEqual(response.status_code, 200)


# from django.test import TestCase
#
# class PostTests(TestCase):
#     #This is the fixture:
#     #-   fields: {"name": 'test', 'thumbnail': "http://afinidata.com/logo.png", 'min_range': 5, 'max_range': 32, 'content': "http://sample.afinidata.com", 'content_activity': "test test test", 'preview': 'previu' }
#     #model: posts.models.Post
#     #pk: 1
#     fixtures = ['Post']
#
#     def testFluffyAnimals(self):
#         s = Post.objects.get(pk=1)
#         self.assertEquals(s.query, 'test')
#         s.query = 'who cares'
#         s.save()