# Generated by Django 3.2.9 on 2022-10-12 02:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0011_alter_perfildata_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='phone_number',
            field=models.CharField(max_length=16, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='/^\\([0-9]{2}\\) [0-9]?[0-9]{4}-[0-9]{4}$/')], verbose_name='Telefone'),
        ),
    ]
