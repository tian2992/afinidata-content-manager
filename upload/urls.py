from django.urls import path
from upload import views

app_name = 'upload'

urlpatterns = [
    path('', views.UploadView.as_view(), name='upload'),
    path('posts/<str:filename>/', views.UploadPostsView.as_view(), name='posts')
]