from django.contrib.auth.models import AnonymousUser, User as DjangoUser
from django.test import Client, RequestFactory, TestCase
from messenger_users.views import new_user, add_attribute, last_interacted
from messenger_users.models import User as MUser, Referral, UserActivity
from posts.models import Interaction

from nose.tools import *


class PostsViewsTest(TestCase):

    databases = ['default', 'messenger_users_db']

    def setUp(self):
        # Every test needs access to the request factory.
        self.MU_DAT = {"messenger_user_id": 2,
                       "last_channel_id": 2,
                       "bot_id": 1,
                       'first_name': "tester",
                       'last_name': "testintong",
                       }
        self.factory = RequestFactory()
        self.client = Client()
        # self.make_user()

    def make_user(self, channel_id=1):
        if not hasattr(self, 'user') or channel_id != 1:
            use = user = MUser(last_channel_id=channel_id,
                               channel_id=channel_id,
                               backup_key="backz{}".format(channel_id),
                               username="test{}".format(channel_id))
            use.save()
            if not hasattr(self, 'user'):
                self.user = use
            return use

    def test_create_user(self):
        self.make_user()
        datao = self.MU_DAT
        response = self.client.post('/messenger_users/new/', datao)
        eq_(response.status_code, 200)

    def test_create_user_attr(self):
        self.make_user()
        response = self.client.post('/messenger_users/{}/add_attribute/'.format(self.user.id),
                                    {"data": "key"})
        eq_(response.status_code, 200)

    def test_get_last_interaction(self):
        self.make_user()
        idz = self.user.id
        i = Interaction(post=None, user_id=idz, username=self.user.username, channel_id=1,
                        bot_id=1, type='open', value=2)
        i.save()
        response = self.client.post('/messenger_users/last_interaction/user/{}'.format(idz),
                                    {"interaction_type": "open"})
        eq_(response.status_code, 200)

    def test_get_w_username(self):
        self.make_user()
        response = self.client.get('/messenger_users/by_username/{}/'.format(self.user.username))
        eq_(response.status_code, 200)

    def test_set_ref(self):
        u1 = self.make_user()
        u2 = self.make_user(2)

        response = self.client.post('/messenger_users/set_referral/',
                                    {'username': u1.username,
                                     "ref": "user-{}".format(u2.username)})

        response = self.client.post('/messenger_users/set_referral/',
                                    {'username': u1.username,
                                     "ref": u2.username})
        eq_(Referral.objects.count(), 2)
        response = self.client.get('/messenger_users/get_refs_count/{}'.format(u2.username))
        eq_(response.content, b'{"set_attributes": {"ref_count": 2}, "messages": []}')

    def test_unit_user_with_state_machine(self):
        user = self.make_user()
        ua = UserActivity()
        ua.user = user
        ua.save()
        ua.to_pre_register()
        ua.start_register()
        ua.finish_register()
        eq_(ua.state, ua.ACTIVE_SESSION)
        ua.send_broadcast()

    def test_view_user_state_machine(self):
        user = self.make_user()
        self.client.post(f"/messenger_users/actions/user/{self.user.id}/set/set pre_register")
        self.client.post(f"/messenger_users/actions/user/{self.user.id}/set/start_register")
        self.client.post(f"/messenger_users/actions/user/{self.user.id}/set/finish_register")
        resp = self.client.post(f"/messenger_users/actions/user/{self.user.id}/set/non_exist")
        eq_(resp.status_code, 200) # should have message of error
        resp = self.client.get(f"/messenger_users/status/user/{self.user.id}/")
        eq_(resp.status_code, 200)
