# Generated by Django 3.2.9 on 2022-10-12 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0010_rename_profile_picture_perfildata_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfildata',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='fotoperfil', verbose_name='foto'),
        ),
    ]
