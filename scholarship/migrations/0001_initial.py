# Generated by Django 4.0.3 on 2022-04-22 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(blank=True, max_length=5, null=True)),
                ('month', models.CharField(blank=True, max_length=5, null=True)),
                ('start_time', models.CharField(blank=True, max_length=5, null=True)),
                ('exam_duration', models.CharField(blank=True, max_length=5, null=True)),
                ('total_questions', models.CharField(blank=True, max_length=5, null=True)),
                ('registration_last_date', models.CharField(blank=True, max_length=5, null=True)),
                ('registration_last_month', models.CharField(blank=True, max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('user_id', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_birth', models.CharField(blank=True, max_length=50, null=True)),
                ('gurdian_name', models.CharField(blank=True, max_length=100, null=True)),
                ('contact', models.CharField(blank=True, max_length=11, null=True)),
                ('whatsapp', models.CharField(blank=True, max_length=11, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('school_college_name', models.CharField(blank=True, max_length=50, null=True)),
                ('appearing_passed_12', models.CharField(blank=True, max_length=50, null=True)),
                ('board_name', models.CharField(blank=True, max_length=10, null=True)),
                ('appeared_wbjee_jeeMain', models.CharField(blank=True, max_length=10, null=True)),
                ('created_at', models.DateField()),
            ],
        ),
    ]