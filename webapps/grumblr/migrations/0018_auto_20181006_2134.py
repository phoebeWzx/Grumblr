# Generated by Django 2.1.1 on 2018-10-06 21:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0017_auto_20181006_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(200), django.core.validators.MinValueValidator(0)]),
        ),
    ]
