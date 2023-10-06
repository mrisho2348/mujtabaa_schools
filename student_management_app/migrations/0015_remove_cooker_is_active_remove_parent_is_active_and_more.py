# Generated by Django 4.2.1 on 2023-10-06 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0014_alter_route_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cooker',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='schoolcleaner',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='schooldriver',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='schoolsecurityperson',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='staffs',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='students',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]