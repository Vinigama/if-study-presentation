# Generated by Django 3.2.9 on 2022-11-13 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('denuncias', '0006_alter_historicosinalizacaoperfil_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicosinalizacaoperfil',
            name='perfil',
            field=models.CharField(max_length=100, verbose_name='Perfil Sinalizado'),
        ),
    ]
