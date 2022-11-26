# Generated by Django 3.2.9 on 2022-10-19 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conteudos', '0037_historico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historico',
            name='conteudo',
            field=models.ForeignKey(limit_choices_to={'ativo': True}, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='conteudos.conteudo'),
        ),
    ]
