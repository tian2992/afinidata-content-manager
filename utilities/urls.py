from django.urls import path
from utilities.views import validates_date, validates_kids_date, parse_date

app_name = 'utilities'

urlpatterns = [
    path('validates_date', validates_date, name="validates_date"),
    path('validates_kids_date', validates_kids_date, name="validates_kids_date"),
    path('parse_date', parse_date, name="parse_date")
]