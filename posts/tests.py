from django.test import TestCase
from nose.tools import *
from .models import *


class PostsTest(TestCase):

    def make_a_user(self):
        if not hasattr(self, "user"):
            self.user = User.objects.create_user(
                username='jtest', email='john@example.com', password='top_secret')

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


