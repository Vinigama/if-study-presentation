from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from usuarios.models import Perfil, PerfilData

class UsuarioForm(UserCreationForm):
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        e = self.cleaned_data['email']
        if User.objects.filter(email=e).exists():
            raise ValidationError(f'O email {e} já está em uso')

        return e


class PerfilForm(forms.ModelForm):
    email       = forms.EmailField(max_length=100)
    username    = forms.CharField(required=True, max_length=50)

    class Meta:
        model = Perfil
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number')

        error_messages = {
            'phone_number': {
                'max_length': ('Número inválido'),
            }
        }

    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        self.request = kwargs.pop("instance")

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_email(self):
        e = self.cleaned_data['email']
        if Perfil.objects.filter(email=e).exists() and not self.request.email == e:
            raise ValidationError(f"O email {e} já está em uso.")
        return e

    def clean_username(self):
        u = self.cleaned_data['username']
        if Perfil.objects.filter(username=u).exists() and not self.request.username == u:
            raise ValidationError(f"O usuário {u} já está em uso.")
        return u

    def clean_phone_number(self):
        t = self.cleaned_data['phone_number']
        if Perfil.objects.filter(phone_number=t).exists() and not self.request.phone_number == t:
            raise ValidationError(f"O número {t} já está em uso.")
        return t

class PerfilDataForm(forms.ModelForm):
    foto    = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    sobre   = forms.CharField(required=False, max_length=255, widget=forms.Textarea(attrs={'rows':4, 'cols':3, 'placeholder': 'Digite sobre você'}))

    class Meta:
        model   = PerfilData
        fields  = ('foto', 'sobre')

    def __init__(self, *args, **kwargs):
        super(PerfilDataForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


