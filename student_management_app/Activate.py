# views.py

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from student_management_app.models import (
 
    Classroom,
    CustomUser,
    Staffs,
    Students,
  
    Parent, 
    SchoolDriver,
   
    SchoolSecurityPerson,
    Cooker,
    SchoolCleaner,
 
)
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect

from django.contrib import messages

def update_user_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            user_id = request.POST.get('user_id')
            is_active = request.POST.get('is_active')
            print(is_active)

            # Retrieve the driver object or return a 404 response if not found
            driver = get_object_or_404(CustomUser, id=user_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                driver.is_active = False
            elif is_active == '0':
                driver.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('manage_driver')

            driver.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    # Redirect back to the driver list page
    return redirect('manage_driver')

def update_cooker_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            user_id = request.POST.get('user_id')
            is_active = request.POST.get('is_active')

            # Retrieve the CustomUser object (Cooker) or return a 404 response if not found
            cooker = get_object_or_404(CustomUser, id=user_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                cooker.is_active = False
            elif is_active == '0':
                cooker.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('manage_cooker')  # Make sure 'manage_cooker' is the name of your cooker list URL

            cooker.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    # Redirect back to the cooker list page
    return redirect('manage_cooker')  # Make sure 'manage_cooker' is the name of your cooker list URL

def update_cleaner_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            user_id = request.POST.get('user_id')
            is_active = request.POST.get('is_active')

            # Retrieve the CustomUser object (Cleaner) or return a 404 response if not found
            cleaner = get_object_or_404(CustomUser, id=user_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                cleaner.is_active = False
            elif is_active == '0':
                cleaner.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('manage_cleaner')  # Make sure 'manage_cleaner' is the name of your cleaner list URL

            cleaner.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    # Redirect back to the cleaner list page
    return redirect('manage_cleaner')  # Make sure 'manage_cleaner' is the name of your cleaner list URL

def update_cleaner_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            user_id = request.POST.get('user_id')
            is_active = request.POST.get('is_active')

            # Retrieve the cleaner object or return a 404 response if not found
            cleaner = get_object_or_404(CustomUser, id=user_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                cleaner.is_active = False
            elif is_active == '0':
                cleaner.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('manage_cleaner')  # Make sure 'manage_cleaner' is the name of your cleaner list URL

            cleaner.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    # Redirect back to the cleaner list page
    return redirect('manage_cleaner')  # Make sure 'manage_cleaner' is the name of your cleaner list URL


def update_security_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            user_id = request.POST.get('user_id')
            is_active = request.POST.get('is_active')

            # Retrieve the security person object or return a 404 response if not found
            security_person = get_object_or_404(CustomUser, id=user_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                security_person.is_active = False
            elif is_active == '0':
                security_person.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('manage_security')  # Make sure 'manage_security' is the name of your security list URL

            security_person.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    # Redirect back to the security person list page
    return redirect('manage_security')  # Make sure 'manage_security' is the name of your security list URL

def update_parent_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            user_id = request.POST.get('user_id')
            is_active = request.POST.get('is_active')

            # Retrieve the parent object or return a 404 response if not found
            parent = get_object_or_404(CustomUser, id=user_id)
            # Toggle the is_active status based on the received value
            if is_active == '1':
                parent.is_active = False
            elif is_active == '0':
                parent.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('manage_parent')  # Make sure 'manage_parents' is the name of your parent list URL

            parent.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    # Redirect back to the parent list page
    return redirect('manage_parent')  # Make sure 'manage_parents' is the name of your parent list URL


def update_staff_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            user_id = request.POST.get('user_id')
            is_active = request.POST.get('is_active')

            # Retrieve the staff object or return a 404 response if not found
            staff = get_object_or_404(CustomUser, id=user_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                staff.is_active = False
            elif is_active == '0':
                staff.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('manage_staff')  # Make sure 'manage_staffs' is the name of your staff list URL

            staff.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    # Redirect back to the staff list page
    return redirect('manage_staff')  # Make sure 'manage_staffs' is the name of your staff list URL

def update_student_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            user_id = request.POST.get('user_id')
            is_active = request.POST.get('is_active')

            # Retrieve the student object or return a 404 response if not found
            student = get_object_or_404(CustomUser, id=user_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                student.is_active = False
            elif is_active == '0':
                student.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('manage_students')  # Make sure 'manage_students' is the name of your student list URL

            student.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    # Redirect back to the student list page
    return redirect('manage_student')  # Make sure 'manage_students' is the name of your student list URL

def update_classroom_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            classroom_id = request.POST.get('user_id')
            is_active = request.POST.get('is_active')

            # Retrieve the classroom object or return a 404 response if not found
            classroom = get_object_or_404(Classroom, id=classroom_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                classroom.is_active = False
            elif is_active == '0':
                classroom.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('manage_classroom')  # Make sure 'manage_classrooms' is the name of your classroom list URL

            classroom.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    # Redirect back to the classroom list page
    return redirect('manage_classroom')  # Make sure 'manage_classrooms' is the name of your classroom list URL