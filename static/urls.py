from django.urls import path
from static.views import IndexView, ContactView

app_name = 'static'

urlpatterns = [
    path('', IndexView.as_view(), name="home"),
    path('contact/', ContactView.as_view(), name="contact")
]
