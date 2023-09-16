# student_management_app/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from exams.models import Group
from .models import Students

@receiver(pre_save, sender=Students)
def update_student_group_name(sender, instance, **kwargs):
    if instance.pk:
        original_student = Students.objects.get(pk=instance.pk)
        if original_student.current_class != instance.current_class:
            group, created = Group.objects.get_or_create(name=instance.current_class)
            group.students.add(instance)
            # Remove the student from the old group
            old_group = Group.objects.get(name=original_student.current_class)
            old_group.students.remove(instance)

@receiver(post_save, sender=Students)
def create_or_update_group(sender, instance, **kwargs):
    # Get or create the Group based on current_class
    group_name = instance.current_class
    group, created = Group.objects.get_or_create(name=group_name)
    
    # Add the student to the group
    group.students.add(instance)
