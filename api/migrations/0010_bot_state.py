# Generated by Django 2.0.2 on 2018-03-11 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20180310_0632'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='state',
            field=models.IntegerField(default=-1),
        ),
    ]
