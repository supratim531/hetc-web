# Generated by Django 3.2.8 on 2022-05-26 12:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0011_auto_20220526_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 26, 18, 21, 50, 456613)),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='gurdian_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_seen',
            field=models.CharField(blank=True, default='00:00', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='preferred_stream',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='school_college_name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
