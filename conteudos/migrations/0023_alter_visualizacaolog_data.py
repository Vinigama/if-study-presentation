# Generated by Django 3.2.9 on 2022-10-09 04:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conteudos', '0022_auto_20221008_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visualizacaolog',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 8, 1, 13, 9, 96913)),
        ),
    ]
