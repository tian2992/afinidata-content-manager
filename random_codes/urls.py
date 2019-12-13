from django.urls import path
from random_codes import views

app_name = 'codes'

urlpatterns = [
    path('', views.CodeListView.as_view(), name='codes'),
    path('<int:code_id>/', views.CodeView.as_view(), name='code'),
    path('generate/', views.GenerateCodesView.as_view(), name='generate'),
    path('use/', views.UseCodeView.as_view(), name='use')
]
