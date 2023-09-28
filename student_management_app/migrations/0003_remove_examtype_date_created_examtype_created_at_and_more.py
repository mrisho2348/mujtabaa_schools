# Generated by Django 4.2.1 on 2023-09-01 06:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0002_examtype_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examtype',
            name='date_created',
        ),
        migrations.AddField(
            model_name='examtype',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examtype',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='result',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]