# Generated by Django 3.1.3 on 2020-12-16 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applostickes', '0008_auto_20201211_1629'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='element',
            options={'ordering': ['name', 'price']},
        ),
    ]
