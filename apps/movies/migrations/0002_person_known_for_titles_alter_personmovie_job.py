# Generated by Django 4.2.10 on 2024-05-04 18:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='known_for_titles',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, verbose_name='Known for titles'), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='personmovie',
            name='job',
            field=models.CharField(max_length=255, null=True, verbose_name='Job'),
        ),
    ]