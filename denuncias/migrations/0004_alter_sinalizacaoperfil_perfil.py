# Generated by Django 3.2.9 on 2022-11-10 02:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('denuncias', '0003_sinalizacaoperfil_silenciado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sinalizacaoperfil',
            name='perfil',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Conteudo', to=settings.AUTH_USER_MODEL),
        ),
    ]
