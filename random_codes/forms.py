from django import forms
from random_codes.models import Code
from messenger_users.models import User


class CodesForm(forms.Form):
    qty = forms.IntegerField()


class ExchangeForm(forms.Form):
    user_id = forms.ChoiceField(choices=[user.pk for user in User.objects.all()])
    code = forms.ChoiceField(choices=[code.code for code in Code.objects.all()])

