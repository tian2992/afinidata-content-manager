from django.urls import path
from static import views

app_name = 'static'

urlpatterns = [
    path('', views.IndexView.as_view(), name="home"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('logout/', views.LogoutView.as_view(), name='logout')
]
