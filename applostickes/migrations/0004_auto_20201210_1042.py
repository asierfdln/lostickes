# Generated by Django 3.1.3 on 2020-12-10 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applostickes', '0003_auto_20201210_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='user_group',
            field=models.ForeignKey(help_text='Grupo al cual pertenence la transaccion.', on_delete=django.db.models.deletion.CASCADE, to='applostickes.usergroup'),
        ),
    ]