# Generated by Django 2.0.2 on 2018-03-10 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20180310_0628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='username',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
