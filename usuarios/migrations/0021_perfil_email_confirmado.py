# Generated by Django 3.2.9 on 2022-11-14 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0020_remove_perfil_silenciado'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='email_confirmado',
            field=models.BooleanField(default=False),
        ),
    ]