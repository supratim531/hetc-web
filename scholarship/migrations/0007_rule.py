# Generated by Django 3.2.8 on 2022-05-04 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0006_student_student_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='')),
            ],
            options={
                'db_table': 'Rule',
            },
        ),
    ]
