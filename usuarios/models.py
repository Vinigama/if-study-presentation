from datetime import timedelta
from django.utils import timezone

from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import conteudos.models as conteudo_models

class LowercaseEmailField(models.EmailField):
    """
    Substituir EmailField para converter emails em minúsculas antes de salvar.
    """
    def to_python(self, value):
        """
        Converte email para lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('O usuário deve ter um e-mail')

        if not username:
            raise ValueError('O usuário deve ter um nome de usuário')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        
        usuario = Perfil.objects.get(id=user.id)
        perfil = PerfilData.objects.create(user=usuario)
        perfil.save()

        return user

    def create_superuser(self, first_name, last_name, email, username, password):        
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin       = True
        user.is_active      = True
        user.is_staff       = True
        user.is_superuser   = True
        user.is_superadmin  = True
        user.save(using=self._db)
        return user

class Perfil(AbstractBaseUser):
    phoneNumberRegex = RegexValidator(regex = r"\([0-9]{2}\) 9?[0-9]{4}-[0-9]{4}")

    username        = models.CharField(max_length=50, unique=True, blank=True, verbose_name='usuário')
    first_name      = models.CharField(max_length=50, verbose_name='nome')
    last_name       = models.CharField(max_length=50, verbose_name='sobrenome')
    email           = LowercaseEmailField(unique=True)
    phone_number    = models.CharField(validators = [phoneNumberRegex], max_length = 15, unique = True, blank=True, null=True, verbose_name='Telefone')
    
    
    # required
    date_joined         = models.DateTimeField(auto_now_add=True)
    last_login          = models.DateTimeField(auto_now_add=True)
    is_superuser        = models.BooleanField(default=False)
    is_admin            = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=False)
    is_superadmin       = models.BooleanField(default=False)
    email_confirmado    = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def nome_completo(self):
        return f'{self.first_name.title()} {self.last_name.title()}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def dados(self):
        return PerfilData.objects.get(user=self.id)

    def time_verbose(self):
        return dict(Perfil.time_mute)[self.silenciado]
    
    def has_abandoned(self):
        DELTA = timezone.now() - timedelta(days=7)
        ultima_visualizacao = conteudo_models.Visualizacao.objects.filter(visualizador=self).order_by("-data").first()
        return ultima_visualizacao.data < DELTA



class PerfilData(models.Model):
    user            = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    foto            = models.ImageField(blank=True, upload_to='fotoperfil', verbose_name="foto", default='../static/img/semfotoperfil.png', null=True)
    sobre           = models.CharField(max_length=255, null=True, default='')

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return self.user.first_name

    def url(self):
        return self.foto.url