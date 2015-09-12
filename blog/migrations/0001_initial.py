# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'T\xc3\xadtulo')),
                ('published', models.BooleanField(default=False, verbose_name=b'Publicado')),
            ],
            options={
                'verbose_name': 'categoria',
                'verbose_name_plural': 'categorias',
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'T\xc3\xadtulo do site')),
                ('status', models.BooleanField(default=False, verbose_name=b'Ativo')),
            ],
            options={
                'verbose_name': 'configura\xe7\xe3o',
                'verbose_name_plural': 'configura\xe7\xf5es',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name=b'Data')),
                ('title', models.CharField(max_length=200, verbose_name=b'T\xc3\xadtulo')),
                ('slug', models.SlugField(verbose_name=b'Slug')),
            ],
            options={
                'verbose_name': 'galeria',
                'verbose_name_plural': 'galerias',
            },
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'', verbose_name=b'Imagem')),
                ('gallery', models.ForeignKey(related_name='imagens', verbose_name=b'Galeria', to='blog.Gallery')),
            ],
            options={
                'verbose_name': 'imagem',
                'verbose_name_plural': 'imagens',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name=b'Data')),
                ('title', models.CharField(max_length=200, verbose_name=b'T\xc3\xadtulo')),
                ('pages', models.IntegerField(verbose_name=b'Quantidade de p\xc3\xa1ginas')),
                ('author', models.CharField(max_length=200, verbose_name=b'Tradutor', blank=True)),
                ('image', models.ImageField(upload_to=b'', verbose_name=b'Imagem Destaque')),
                ('categories', models.ManyToManyField(to='blog.Category', verbose_name=b'Categorias')),
                ('gallery', models.ForeignKey(verbose_name=b'Galeria', to='blog.Gallery')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
            },
        ),
    ]
