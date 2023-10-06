from django.shortcuts import render, get_object_or_404, redirect
from student_management_app.models import (
 
    SessionYearModel,
    Staffs,
    Students,
    Subject,
    Parent, 

    SchoolDriver,

    Car,
    SchoolSecurityPerson,
    Cooker,
    SchoolCleaner,
    Classroom,
  
)
from django.contrib import messages

def delete_cleaner(request, cleaner_id):
    # Retrieve the cleaner object or return a 404 if not found
    cleaner = get_object_or_404(SchoolCleaner, id=cleaner_id)

    if request.method == 'POST':
        # Perform the deletion
        cleaner.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'School cleaner deleted successfully.')
        return redirect('manage_cleaner')  # Replace 'cleaner_list' with your actual list view name

    return render(request, 'delete/delete_cleaner_confirm.html', {'cleaner': cleaner})

def delete_car(request, car_id):
    # Retrieve the car object or return a 404 if not found
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        # Perform the deletion
        car.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'School Car deleted successfully.')
        return redirect('car_list')  # Replace 'car_list' with your actual list view name

    return render(request, 'car/delete_car_confirm.html', {'car': car})

def delete_classroom(request, classroom_id):
    # Retrieve the classroom object or return a 404 if not found
    classroom = get_object_or_404(Classroom, id=classroom_id)

    if request.method == 'POST':
        # Perform the deletion
        classroom.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'School Classroom deleted successfully.')
        return redirect('manage_classroom')  # Replace 'classroom_list' with your actual list view name

    return render(request, 'delete/delete_classroom_confirm.html', {'classroom': classroom})

def delete_parent(request, parent_id):
    # Retrieve the parent object or return a 404 if not found
    parent = get_object_or_404(Parent, id=parent_id)

    if request.method == 'POST':
        # Perform the deletion
        parent.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'student parent deleted successfully.')
        return redirect('manage_parent')  # Replace 'parent_list' with your actual list view name

    return render(request, 'delete/delete_parent_confirm.html', {'parent': parent})



def delete_cooker(request, cooker_id):
    # Retrieve the cooker object or return a 404 if not found
    cooker = get_object_or_404(Cooker, id=cooker_id)

    if request.method == 'POST':
        # Perform the deletion
        cooker.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'School Cooker deleted successfully.')
        return redirect('manage_cooker')  # Replace 'cooker_list' with your actual list view name

    return render(request, 'delete/delete_cooker_confirm.html', {'cooker': cooker})


def delete_driver(request, driver_id):
    # Retrieve the driver object or return a 404 if not found
    driver = get_object_or_404(SchoolDriver, id=driver_id)

    if request.method == 'POST':
        # Perform the deletion
        driver.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'School Driver deleted successfully.')
        return redirect('manage_driver')  # Replace 'driver_list' with your actual list view name

    return render(request, 'delete/delete_driver_confirm.html', {'driver': driver})

def delete_security(request, security_id):
    # Retrieve the security person object or return a 404 if not found
    security_person = get_object_or_404(SchoolSecurityPerson, id=security_id)

    if request.method == 'POST':
        # Perform the deletion
        security_person.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'School Security deleted successfully.')
        return redirect('manage_security')  # Replace 'security_person_list' with your actual list view name

    return render(request, 'delete/delete_security_confirm.html', {'security_person': security_person})


def delete_session(request, session_id):
    # Retrieve the session year object or return a 404 if not found
    session_year = get_object_or_404(SessionYearModel, id=session_id)

    if request.method == 'POST':
        # Perform the deletion
        session_year.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'Session deleted successfully.')
        return redirect('manage_session')  # Replace 'session_year_list' with your actual list view name

    return render(request, 'delete/delete_session_confirm.html', {'session_year': session_year})


def delete_staff(request, staff_id):
    # Retrieve the staff object or return a 404 if not found
    staff = get_object_or_404(Staffs, id=staff_id)

    if request.method == 'POST':
        # Perform the deletion
        staff.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'staff deleted successfully.')
        return redirect('manage_staff')  # Replace 'staff_list' with your actual list view name

    return render(request, 'delete/delete_staff_confirm.html', {'staff': staff})


def delete_student(request, student_id):
    # Retrieve the student object or return a 404 if not found
    student = get_object_or_404(Students, id=student_id)

    if request.method == 'POST':
        # Perform the deletion
        student.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'student deleted successfully.')
        return redirect('manage_student')  # Replace 'student_list' with your actual list view name

    return render(request, 'delete/delete_student_confirm.html', {'student': student})

def delete_subject(request, subject_id):
    # Retrieve the subject object or return a 404 if not found
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        # Perform the deletion
        subject.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'subject deleted successfully.')
        return redirect('manage_subject')  # Replace 'subject_list' with your actual list view name

    return render(request, 'delete/delete_subject_confirm.html', {'subject': subject})