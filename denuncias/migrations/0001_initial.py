# Generated by Django 3.2.9 on 2022-10-13 01:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conteudos', '0031_auto_20221009_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Denuncias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_requisicao', models.CharField(choices=[('rude', 'Rude')], max_length=255)),
                ('comentario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Comentario', to='conteudos.comentario')),
                ('conteudo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Conteudo', to='conteudos.conteudo')),
                ('criador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
