# Generated by Django 3.2.9 on 2022-11-02 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0015_alter_perfildata_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfildata',
            name='sobre',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
