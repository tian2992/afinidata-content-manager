from django.urls import path
from utilities.views import validates_date

app_name = 'utilities'

urlpatterns = [
    path('validates_date', validates_date, name="validates_date")
]