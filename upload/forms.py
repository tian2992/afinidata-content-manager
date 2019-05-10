from django.core.validators import FileExtensionValidator
from django import forms


class UploadForm(forms.Form):

    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'])])
