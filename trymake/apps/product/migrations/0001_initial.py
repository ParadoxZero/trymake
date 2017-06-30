# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 18:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=500)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.AttributeName')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=250, unique=True)),
                ('attributes', models.ManyToManyField(to='product.AttributeName')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.Image')),
                ('parent_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Category')),
            ],
        ),
        migrations.CreateModel(
            name='DiscountOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('discount_percent', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=250, unique=True)),
                ('slug', models.CharField(db_index=True, max_length=4, unique=True)),
                ('approximate_weight', models.DecimalField(decimal_places=2, max_digits=6)),
                ('short_description', models.TextField()),
                ('description', models.TextField()),
                ('cover_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cover_image', to='commons.Image')),
                ('images', models.ManyToManyField(related_name='additional_images', to='commons.Image')),
            ],
        ),
        migrations.AddField(
            model_name='discountoffer',
            name='products',
            field=models.ManyToManyField(to='product.Product'),
        ),
        migrations.AddField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(to='product.Product'),
        ),
        migrations.AddField(
            model_name='attributevalues',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product'),
        ),
    ]
