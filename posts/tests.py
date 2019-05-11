from django.test import TestCase
from posts.models import Post
from django.contrib.auth.models import User


class PostTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username='testuser', password='123456')
        Post.objects.create(name='test 01', thumbnail='adsfasdf', new=True, min_range=5, max_range=20,
                            content='adsfadsf', content_activity='asdfasdf', user=user)
        Post.objects.create(name='test 02', thumbnail='adsfasdf', new=True,
                            content='adsfadsf', content_activity='asdfasdf', user=user)

    def post_has_created(self):
        post = Post.objects.get(name='test 01')
        second_post = Post.objects.get(name='test 02')
        self.assertEqual(post.new, True)
        #self.assertNotEqual(second_post.new, True)

