from django.urls import path
from random_codes import views

app_name = 'codes'

urlpatterns = [
    path('', views.CodeListView.as_view(), name='codes'),
    path('generate/', views.GenerateCodesView.as_view(), name='generate')
]