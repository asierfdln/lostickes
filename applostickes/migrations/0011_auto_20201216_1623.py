# Generated by Django 3.1.3 on 2020-12-16 15:23

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('applostickes', '0010_transaction_score_settling_mapping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='score_settling_mapping',
            field=picklefield.fields.PickledObjectField(default=dict, editable=False),
        ),
    ]
