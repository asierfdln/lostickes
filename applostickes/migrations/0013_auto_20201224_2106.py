# Generated by Django 3.1.3 on 2020-12-24 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applostickes', '0012_auto_20201224_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=55),
        ),
    ]
