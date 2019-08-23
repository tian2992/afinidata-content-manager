from django.urls import path, include
from messenger_users.views import new_user, add_attribute, by_username, last_interacted, set_referral,\
    get_referrals_count, user_interaction, UserDataViewSet, ChildDataViewSet, ChildViewSet, UserViewSet, \
    get_last_action, set_user_action, get_user_activity_status, UserDataBulkView
from rest_framework import routers


app_name = 'messenger_users'


api_router = routers.DefaultRouter()
api_router.register(r'userData', UserDataViewSet)
api_router.register(r'childData', ChildDataViewSet)
api_router.register(r'child', ChildViewSet)
api_router.register(r'user', UserViewSet)


urlpatterns = [
    path('new/', new_user, name="new"),
    path('<channel_id>/add_attribute/', add_attribute, name="add_attribute"),
    path('by_username/<username>/', by_username, name='by_username'),
    path('last_interaction/user/<id>', last_interacted, name='last_activity'),
    path('set_referral/', set_referral, name='set_ref'),
    path('get_refs_count/<username>', get_referrals_count, name='get_ref'),
    path('user_interaction/', user_interaction, name='user_interaction'),
    path('api/', include(api_router.urls)),
    path('userData/bulk/create', UserDataBulkView.as_view(), name='create_list_user_data'),

]
