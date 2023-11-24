from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.utils import timezone
from student_management_app.models import Class_level, Students, Subject, Staffs
from django.db import transaction

class Question_DB(models.Model):
    teacher = models.ForeignKey(Staffs, on_delete=models.CASCADE, null=True)
    qno = models.AutoField(primary_key=True)
    question = models.CharField(max_length=255)
    optionA = models.CharField(max_length=255)
    optionB = models.CharField(max_length=255)
    optionC = models.CharField(max_length=255)
    optionD = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f'Question No.{self.qno}: {self.question} \t\t Options: \nA. {self.optionA} \nB.{self.optionB} \nC.{self.optionC} \nD.{self.optionD} '

class Question_Paper(models.Model):
    teacher = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    qPaperTitle = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question_DB)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return f'Question Paper Title: {self.qPaperTitle}'

    def get_question_count(self):
        return self.questions.count()



class Stu_Question(Question_DB):
    teacher = None
    student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True)
    choice = models.CharField(max_length=3, default="E")
    is_correct = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return f"Student: {self.student.username}, Question: {self.question}"

class StuExam_DB(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True)
    examname = models.CharField(max_length=255)
    qpaper = models.ForeignKey(Question_Paper, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField(Stu_Question)
    score = models.IntegerField(default=0)
    completed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    @property
    def is_passed(self):
        pass_mark = 50  # Replace with your desired pass mark
        return self.score >= pass_mark

    def __str__(self):
        return f"{self.student} - {self.examname}"

class StuResults_DB(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True)
    exams = models.ManyToManyField(StuExam_DB)
    total_score = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)
    total_completed_exams = models.PositiveIntegerField(default=0)
    total_passed_exams = models.PositiveIntegerField(default=0)
    is_failed = models.BooleanField(default=False)  # New field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    @property
    def calculate_average_score(self):
        if self.total_completed_exams == 0:
            return 0
        return self.total_score / self.total_completed_exams

    def update_failed_status(self):
        failed_exams = self.exams.filter(score__lt=50)  # Adjust the score threshold if needed
        self.is_failed = failed_exams.exists()
        self.save()

    def __str__(self):
        return str(self.student)

@receiver(post_save, sender=StuExam_DB)
def update_results(sender, instance, **kwargs):
    with transaction.atomic():
        results, created = StuResults_DB.objects.get_or_create(student=instance.student)

        if not created:
            # Update existing results instance
            results.exams.add(instance)
            results.total_score += instance.score
            results.total_completed_exams += 1

            if instance.score >= 50:  # Adjust the pass mark if needed
                results.total_passed_exams += 1

            results.average_score = results.calculate_average_score
            results.update_failed_status()  # Call the new method to update the failed status

            print("Before saving results:", results)  # Print the results object before saving

            results.save()
            print("After saving results:", results)  # Print the results object after saving
        else:
            print("Creating new results instance...")
            StuResults_DB.objects.create(student=instance.student, created_at=timezone.now())
        
        

    
class Exam_Model(models.Model):
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE)  
    name = models.CharField(max_length=255)
    total_marks = models.IntegerField()
    duration = models.IntegerField()
    question_paper = models.ForeignKey(Question_Paper, on_delete=models.CASCADE, related_name='exams')
    selected_class = models.ForeignKey(Class_level, on_delete=models.SET_NULL, null=True, blank=True)   
    subjects = models.ManyToManyField(Subject)  
    start_time = models.DateTimeField(default=timezone.now)  # Change to timezone.now()
    end_time = models.DateTimeField(default=timezone.now)    # Change to timezone.now()
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    @classmethod
    def get_published_count(cls):
        return cls.objects.filter(is_published=True).count()

    def __str__(self):
        return self.name
    
    def is_published_now(self):
        if self.is_published and self.publish_date and self.publish_date >= timezone.now():
            return True
        else:
            return False
   
    
    
