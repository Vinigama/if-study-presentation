# Generated by Django 3.2.9 on 2022-07-19 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conteudos', '0003_alter_comentario_resposta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='resposta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='conteudos.comentario'),
        ),
    ]
