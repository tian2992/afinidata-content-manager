from django.urls import path
from messenger_users.views import new_user, add_attribute, by_username, last_interacted, set_referral, get_referrals_count, user_interaction

app_name = 'messenger_users'

urlpatterns = [
    path('new/', new_user, name="new"),
    path('<channel_id>/add_attribute/', add_attribute, name="add_attribute"),
    path('by_username/<username>/', by_username, name='by_username'),
    path('last_interaction/user/<id>', last_interacted, name='last_activity'),
    path('set_referral/', set_referral, name='set_ref'),
    path('get_refs_count/<username>', get_referrals_count, name='get_ref'),
    path('user_interaction/', user_interaction, name='user_interaction'),

]
