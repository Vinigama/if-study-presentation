# Generated by Django 3.2.9 on 2022-11-07 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0019_perfil_silenciado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='silenciado',
        ),
    ]
