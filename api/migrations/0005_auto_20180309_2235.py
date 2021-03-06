# Generated by Django 2.0.2 on 2018-03-09 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20180301_0105'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('conf_path', models.CharField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='target',
            name='target_follows',
            field=models.CharField(choices=[('F', 'Followers'), ('L', 'Likers')], max_length=1),
        ),
        migrations.AddField(
            model_name='reset',
            name='bot',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.Bot'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='target',
            name='bot',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.Bot'),
            preserve_default=False,
        ),
    ]
