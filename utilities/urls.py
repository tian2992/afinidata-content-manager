from django.urls import path
from utilities.views import validates_date, validates_kids_date, fix_date, check_valid_date, change_kids_date

app_name = 'utilities'

urlpatterns = [
    path('validates_date', validates_date, name="validates_date"),
    path('validates_kids_date', validates_kids_date, name="validates_kids_date"),
    path('fix_date', fix_date, name='fix_date'),
    path('check_valid_date', check_valid_date, name='check_valid_date'),
    path('change_kids_date', change_kids_date, name='change_kids_date')
]