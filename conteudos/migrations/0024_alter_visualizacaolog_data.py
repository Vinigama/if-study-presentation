# Generated by Django 3.2.9 on 2022-10-09 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conteudos', '0023_alter_visualizacaolog_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visualizacaolog',
            name='data',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
