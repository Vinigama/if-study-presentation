# Generated by Django 3.2.9 on 2022-10-30 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0014_alter_perfil_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfildata',
            name='foto',
            field=models.ImageField(blank=True, default='../static/img/semfotoperfil.png', null=True, upload_to='fotoperfil', verbose_name='foto'),
        ),
    ]