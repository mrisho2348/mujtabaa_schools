# Generated by Django 4.2.1 on 2023-09-01 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0003_remove_examtype_date_created_examtype_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='total_marks',
            field=models.DecimalField(blank=True, decimal_places=2, default=100, max_digits=5, null=True),
        ),
    ]
