# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='published',
            field=models.BooleanField(default=False, verbose_name=b'Publicado'),
        ),
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.BooleanField(default=False, verbose_name=b'Publicado'),
        ),
    ]
