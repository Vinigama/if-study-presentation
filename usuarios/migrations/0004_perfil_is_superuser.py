# Generated by Django 3.2.9 on 2022-10-09 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
