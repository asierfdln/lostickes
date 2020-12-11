# Generated by Django 3.1.3 on 2020-12-11 15:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applostickes', '0006_auto_20201210_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='price',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(limit_value=0, message='Only positive integers allowed')]),
        ),
    ]