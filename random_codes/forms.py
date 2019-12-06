from django import forms


class CodesForm(forms.Form):
    qty = forms.IntegerField()
