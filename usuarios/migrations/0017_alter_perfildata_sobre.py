# Generated by Django 3.2.9 on 2022-11-06 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0016_perfildata_sobre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfildata',
            name='sobre',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]