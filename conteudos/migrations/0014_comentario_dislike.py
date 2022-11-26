# Generated by Django 3.2.9 on 2022-07-26 00:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conteudos', '0013_alter_comentario_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='dislike',
            field=models.ManyToManyField(blank=True, related_name='dislike', to=settings.AUTH_USER_MODEL),
        ),
    ]
