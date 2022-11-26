from django_quill.forms import QuillFormField
from django import forms

class DivulgarTrilhasForm(forms.Form):
    body = QuillFormField()