# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-07 08:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=200)),
                ('doc', models.ImageField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('lesson_type', models.CharField(default=0, max_length=120)),
                ('unit', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('college_number', models.BigIntegerField(primary_key=True, serialize=False)),
                ('social_number', models.CharField(max_length=120)),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('period', models.CharField(max_length=120)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Section')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Subject'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Section'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Subject'),
        ),
        migrations.AddField(
            model_name='document',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Student'),
        ),
    ]