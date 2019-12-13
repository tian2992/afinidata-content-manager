from django import forms
from random_codes.models import Code
from messenger_users.models import User


class CodesForm(forms.Form):
    qty = forms.IntegerField()


class UseCodeForm(forms.Form):
    user_id = forms.ModelChoiceField(User.objects.all())
    code = forms.ModelChoiceField(Code.objects.filter(available=True), to_field_name="code")

