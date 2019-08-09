from django.urls import path
from messenger_users.views import new_user, add_attribute, by_username, last_interacted, set_referral

app_name = 'messenger_users'

urlpatterns = [
    path('new/', new_user, name="new"),
    path('<channel_id>/add_attribute/', add_attribute, name="add_attribute"),
    path('by_username/<username>/', by_username, name='by_username'),
    path('last_interaction/user/<id>', last_interacted, name='last_activity'),
    path('set_referral/', set_referral, name='referrals'),

]
