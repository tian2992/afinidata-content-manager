from django.contrib import admin
from django.urls import path
from dash.views import index, DashView

app_name = 'dash'

urlpatterns = [
    path('', DashView.as_view(), name="index")
]