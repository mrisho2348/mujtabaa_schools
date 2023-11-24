# Generated by Django 4.2.1 on 2023-11-12 00:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student_management_app', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question_DB',
            fields=[
                ('qno', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=255)),
                ('optionA', models.CharField(max_length=255)),
                ('optionB', models.CharField(max_length=255)),
                ('optionC', models.CharField(max_length=255)),
                ('optionD', models.CharField(max_length=255)),
                ('answer', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='Question_Paper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qPaperTitle', models.CharField(max_length=255)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('questions', models.ManyToManyField(to='exams.question_db')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='StuExam_DB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examname', models.CharField(max_length=255)),
                ('score', models.IntegerField(default=0)),
                ('completed', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('qpaper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exams.question_paper')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='Stu_Question',
            fields=[
                ('question_db_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='exams.question_db')),
                ('choice', models.CharField(default='E', max_length=3)),
                ('is_correct', models.BooleanField(default=False)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
            ],
            bases=('exams.question_db',),
        ),
        migrations.CreateModel(
            name='StuResults_DB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_score', models.IntegerField(default=0)),
                ('average_score', models.FloatField(default=0)),
                ('total_completed_exams', models.PositiveIntegerField(default=0)),
                ('total_passed_exams', models.PositiveIntegerField(default=0)),
                ('is_failed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exams', models.ManyToManyField(to='exams.stuexam_db')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('students', models.ManyToManyField(related_name='groups', to='student_management_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='Exam_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('total_marks', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_published', models.BooleanField(default=False)),
                ('publish_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exams.group')),
                ('question_paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='exams.question_paper')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs')),
                ('subjects', models.ManyToManyField(to='student_management_app.subject')),
            ],
        ),
        migrations.AddField(
            model_name='stuexam_db',
            name='questions',
            field=models.ManyToManyField(to='exams.stu_question'),
        ),
    ]
