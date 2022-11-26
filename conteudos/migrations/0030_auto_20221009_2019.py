# Generated by Django 3.2.9 on 2022-10-09 23:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conteudos', '0029_visualizacaolog_visualizador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visualizacaolog',
            name='conteudo',
            field=models.ForeignKey(limit_choices_to={'ativo': True}, on_delete=django.db.models.deletion.PROTECT, related_name='conteudo', to='conteudos.conteudo'),
        ),
        migrations.AlterField(
            model_name='visualizacaolog',
            name='visualizador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='visualizador', to=settings.AUTH_USER_MODEL),
        ),
    ]