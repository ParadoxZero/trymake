# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 15:43
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Format: 9999999999', regex='[0-9]{10}')])),
                ('pincode', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(message='Format: 999999', regex='[0-9]{6}')])),
                ('landmark', models.CharField(blank=True, max_length=500)),
                ('city', models.CharField(max_length=500)),
                ('default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=2, unique=True)),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('phone', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message='Format: 9999999999', regex='[0-9]{10}')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=5, unique=True)),
                ('name', models.CharField(max_length=500)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Country')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.Customer'),
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.State'),
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('default', 'customer')]),
        ),
    ]
