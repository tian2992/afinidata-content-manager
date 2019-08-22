import uuid
from django.db import models
from transitions import Machine
from django.db.models.signals import post_init
from django.dispatch import receiver


class User(models.Model):
    last_channel_id = models.CharField(max_length=50, unique=True)
    channel_id = models.CharField(max_length=50, null=True, unique=True)
    backup_key = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bot_id = models.IntegerField(default=1)
    username = models.CharField(max_length=100, null=True, unique=True)

    def __str__(self):
        return "User {} with m_id: {}; username = {}".format(self.pk, self.last_channel_id, self.username)

    class Meta:
        app_label = 'messenger_users'


class UserData(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    data_key = models.CharField(max_length=30)
    data_value = models.TextField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.data_value

    class Meta:
        app_label = 'messenger_users'


class Child(models.Model):
    parent_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    dob = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'messenger_users'


class ChildData(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    data_key = models.CharField(max_length=50)
    data_value = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'messenger_users'


class Referral(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_shared = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='shared_ref')
    user_opened = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='opened_ref', null=True)
    ref_type = models.CharField(choices=[("link", "link"), ("ref","ref")], default="link", max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'messenger_users'

    def __str__(self):
        return "User '{}' referred '{}'".format(self.user_shared, self.user_opened)


class UserActivity(models.Model):

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        app_label = 'messenger_users'

    WAIT = 'wait'
    USER_QUERY = 'user_query'
    BROADCAST_START= 'broadcast_start'
    TIMED_START = 'timed_start'
    ACTIVE_SESSION = 'active_session'
    DISPATCHED = 'dispatched'
    OPENED = 'opened'
    FOLLOW_UP = 'follow_up'

    STATE_TYPES = [
        (WAIT, WAIT),
        (USER_QUERY, USER_QUERY),
        (BROADCAST_START, BROADCAST_START),
        (TIMED_START, TIMED_START),
        (ACTIVE_SESSION, ACTIVE_SESSION),
        (DISPATCHED, DISPATCHED),
        (OPENED, OPENED),
        (FOLLOW_UP, FOLLOW_UP),
    ]

    state = models.CharField(
        "state",
        max_length=100,
        choices=STATE_TYPES,
        default=WAIT,
        help_text='stado',
    )


@receiver(post_init, sender=UserActivity)
def init_state_machine(instance, **kwargs):
    states = [state for state, _ in instance.STATE_TYPES]
    machine = instance.machine = Machine(model=instance, states=states, initial=instance.WAIT, \
                                         ignore_invalid_triggers=True)
    machine.add_transition('receive_user_message', instance.WAIT, instance.USER_QUERY)
    machine.add_transition('send_broadcast', instance.WAIT, instance.BROADCAST_START)
    machine.add_transition('awaited_enough', instance.WAIT, instance.TIMED_START)
    machine.add_transition('want_activity', instance.USER_QUERY, instance.ACTIVE_SESSION)
    machine.add_transition('want_activity', instance.BROADCAST_START, instance.ACTIVE_SESSION)
    machine.add_transition('want_activity', instance.TIMED_START, instance.ACTIVE_SESSION)
    machine.add_transition('get_post', instance.ACTIVE_SESSION, instance.DISPATCHED)
    machine.add_transition('open_post', instance.DISPATCHED, instance.OPENED)
    machine.add_transition('give_feedback', instance.OPENED, instance.FOLLOW_UP)
    machine.add_transition('give_feedback', instance.FOLLOW_UP, instance.FOLLOW_UP)
    machine.add_transition('end_feedback', instance.FOLLOW_UP, instance.WAIT)
    machine.add_transition('no_feedback', instance.OPENED, instance.WAIT)
