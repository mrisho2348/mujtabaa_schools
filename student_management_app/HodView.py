import json
from django.urls import reverse
from datetime import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from student_management_app.forms import  (
    AddSessionYearForm,
    AddStaffForm, 
    AddStudentForm,
    AddSubjectForm,
    EditStaffForm,
    EditStudentForm
)
from student_management_app.models import (
    Attendance,
    AttendanceReport,
    CustomUser,
    FeedBackStaff,
    FeedBackStudent,
    LeaveReportStaffs,
    LeaveReportStudent,
    SessionYearModel,
    Staffs,
    Students,
    Subject,
    Parent,    
    Qualifications,
    Skills,
    EmploymentHistory,
    References,
    SchoolDriver,
    SchoolDriverMedicalInfo,
    SchoolDriverLicenseInfo,
    SchoolDriverContact,
    SchoolDriverEmergencyContact,
    SchoolDriverEmployment,
    SchoolDriverVehicle,
    SchoolDriverLanguage,
    SchoolDriverReference,
    Car,
    SchoolSecurityPerson,
    Cooker,
    SchoolCleaner,
    Classroom,
    ExamType,
    Result,
    StudentExamInfo,
    StudentPositionInfo,
    StaffRoleAssignment,
)
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.db import IntegrityError, DatabaseError
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseBadRequest
from PIL import Image





def admin_home(request):
    staff_count = Staffs.objects.all().count()
    subject_count = Subject.objects.all().count()
    student_count = Students.objects.all().count()

    subject_all = Subject.objects.all()
    subject_list = [subject.subject_name for subject in subject_all]

    staff_all = Staffs.objects.all()
    attendance_absent_staff_list = []
    staff_name_list = []
    for staff in staff_all:
        leaves = LeaveReportStaffs.objects.filter(staff_id=staff.id, leave_status=1).count()
        attendance_absent_staff_list.append(leaves)
        staff_name_list.append(staff.admin.username)

    student_all = Students.objects.all()
    attendance_present_student_list = []
    attendance_absent_student_list = []
    student_name_list = []
    for student in student_all:
        attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
        attendance_present_student_list.append(attendance)
        attendance_absent_student_list.append(leaves + absent)
        student_name_list.append(student.admin.username)

    context = {
        "staff_count": staff_count,
        "subject_count": subject_count,
        "subject_list": subject_list,
        "attendance_absent_staff_list": attendance_absent_staff_list,
        "staff_name_list": staff_name_list,
        "attendance_present_student_list": attendance_present_student_list,
        "attendance_absent_student_list": attendance_absent_student_list,
        "student_count": student_count,
    }

    return render(request, "hod_template/home_content.html", context)


def render_staff_role_assignment_form(request):
    if request.method == 'POST':
        try:
            # Process the submitted form data
            staff_id = request.POST.get('staff')
            role = request.POST.get('role')
            notes = request.POST.get('notes')

            # Validate staff_id (ensure it's a valid staff member)
            try:
                staff_member = Staffs.objects.get(id=staff_id)
            except Staffs.DoesNotExist:
                staff_member = None

            if not staff_member:
                error_message = "Invalid staff member selected."
                return render(request, 'hod_template/add_staff_role_assignment_form.html', {'error_message': error_message})

            # Create a new StaffRoleAssignment instance and save it
            staff_assignment = StaffRoleAssignment(
                staff=staff_member,
                role=role,
                notes=notes,
               
            )
            staff_assignment.save()

            messages.success(request, 'Staff role assignment added successfully.')  # Success message
            return redirect('staff_role_list')  # Redirect to a success page or any desired URL

        except Exception as e:
            messages.error(request, f'Error adding staff role assignment: {str(e)}')  # Error message

    # Retrieve staff members from your database (adjust this query as needed)
    staff_members = Staffs.objects.all()  # Replace 'Staffs' with your actual model

    return render(request, 'hod_template/add_staff_role_assignment_form.html', {'staff_members': staff_members,'action':'add'})

def staff_role_list(request):
    staff_assignments = StaffRoleAssignment.objects.all()
    return render(request, 'hod_template/manage_staff_role_list.html', {'staff_assignments': staff_assignments})

def edit_staff_role(request, assignment_id):
    assignment = get_object_or_404(StaffRoleAssignment, id=assignment_id)

    if request.method == 'POST':
        try:
            # Retrieve the form data from the request
            staff_id = request.POST.get('staff')
            role = request.POST.get('role')
            notes = request.POST.get('notes')

            # Update the assignment with the new data
            assignment.staff_id = staff_id
            assignment.role = role
            assignment.notes = notes
            assignment.save()

            messages.success(request, 'Staff role assignment updated successfully.')  # Success message
            return redirect('staff_role_list')  # Redirect to a success page or any desired URL

        except Exception as e:
            messages.error(request, f'Error updating staff role assignment: {str(e)}')  # Error message

    # Render the template for editing with the assignment data
    return render(request, 'hod_template/add_staff_role_assignment_form.html', {'assignment': assignment, 'action': 'edit'})

def delete_staff_role(request, assignment_id):
    assignment = get_object_or_404(StaffRoleAssignment, id=assignment_id)

    if request.method == 'POST':
        # Handle the deletion here
        assignment.delete()
        return redirect('staff_role_list')  # Redirect to a success page or any desired URL after deletion

    return redirect('staff_role_list') 

def get_class_choices(request):
    segment = request.GET.get('segment')

    SCHOOL_SEGMENT_CHOICES = (
        ("Nursery", "Nursery Level"),
        ("Primary", "Primary Level"),
        ("Secondary", "Secondary Level"),
    )

    NURSERY_CLASS_CHOICES = [
        ("Baby", "Baby"),
        ("KG1", "KG1"),
        ("KG2", "KG2")
    ]

    PRIMARY_CLASS_CHOICES = [
        ("I", "I"),
        ("II", "II"),
        ("III", "III"),
        ("IV", "IV"),
        ("V", "V"),
        ("VI", "VI")
    ]

    SECONDARY_CLASS_CHOICES = [
        ("Form I", "Form I"),
        ("Form II", "Form II"),
        ("Form III", "Form III"),
        ("Form IV", "Form IV")
    ]

    if segment == "Nursery":
        choices = NURSERY_CLASS_CHOICES
    elif segment == "Primary":
        choices = PRIMARY_CLASS_CHOICES
    elif segment == "Secondary":
        choices = SECONDARY_CLASS_CHOICES
    else:
        choices = []

    return JsonResponse({'choices': choices})


def driver_form_view(request):
    return render(request, 'hod_template/add_driver_form.html')
def add_security_person(request):
    return render(request, 'hod_template/add_security_person_form.html')
def add_cooker(request):
    return render(request, 'hod_template/add_cooker_form.html')
def add_schoolcleaner(request):
    return render(request, 'hod_template/add_schoolcleaner_form.html')
def add_schoolclassroom(request):
    return render(request, 'hod_template/add_school_classroom.html')
def add_schoolcar_view(request):
    return render(request, 'hod_template/add_school_car.html')


def add_driver_info_save(request):
    if request.method == 'POST':
        try:
            # Extract form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')  # Be sure to hash the password securely
            license_number = request.POST.get('license_number')
            contact_number = request.POST.get('contact_number')
            address = request.POST.get('address')
            date_of_birth_str = request.POST.get('date_of_birth')
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            gender = request.POST.get('gender')
            profile_pic = request.FILES.get('profile_pic', None)
            driving_license_photo = request.FILES.get('driving_license_photo', None)

            # Perform validation
            if not all([first_name, last_name, date_of_birth]):
                messages.error(request, "Please provide all required fields")
                return redirect("add_driver_info")

            # Define accepted image formats
            accepted_image_formats = ['image/jpeg', 'image/jpg', 'image/png']
            accepted_pdf_format = 'application/pdf'

            # Define maximum file size in bytes (5MB)
            max_file_size = 5 * 1024 * 1024

            # Function to validate file format and size
            def validate_file(file, accepted_formats, max_size):
                if file.content_type not in accepted_formats:
                    raise ValueError(f"Invalid file format. Accepted formats: {', '.join(accepted_formats)}")

                if file.size > max_size:
                    raise ValueError(f"File size exceeds the limit. Maximum allowed size: {max_size} bytes")

            # Save the driver information to the database
            try:
                # Save the profile picture
                profile_pic_url = None
                if profile_pic:
                    validate_file(profile_pic, accepted_image_formats, max_file_size)

                    fs = FileSystemStorage()
                    filename = fs.save(profile_pic.name, profile_pic)
                    profile_pic_url = fs.url(filename)

                # Save the driving license photo
                driving_license_photo_url = None
                if driving_license_photo:
                    validate_file(driving_license_photo, [accepted_pdf_format], max_file_size)

                    fs = FileSystemStorage()
                    filename = fs.save(driving_license_photo.name, driving_license_photo)
                    driving_license_photo_url = fs.url(filename)

                # Check if the admin user already exists in SchoolDriver model
                user, created = CustomUser.objects.get_or_create(
                    username=username,
                    defaults={
                        'password': password,
                        'email': email,
                        'first_name': first_name,
                        'last_name': last_name,
                        'user_type': 4,  # SchoolDriver user type
                    }
                )

                if not created:
                    # Update existing user fields if the user already exists
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.user_type = 4  # SchoolDriver user type
                    user.set_password(password)  # Update password securely

                    # Save the user instance
                    user.save()

                # Create or update the corresponding SchoolDriver instance
                driver, driver_created = SchoolDriver.objects.get_or_create(admin=user)
                driver.license_number = license_number
                driver.contact_number = contact_number
                driver.address = address
                driver.date_of_birth = date_of_birth
                driver.gender = gender
                driver.profile_pic = profile_pic_url
                driver.driving_license_photo = driving_license_photo_url

                # Save the SchoolDriver record
                driver.save()

                messages.success(request, "Driver information saved successfully.")
                # Redirect to the next view with driver_id as a parameter
                if 'continue_filling' in request.POST:
                    return redirect(reverse('add_driver_medical_info', kwargs={'driver_id': driver.id}))
                else:
                    return redirect("driver_form")

            except Exception as e:
                messages.error(request, f"Error saving driver information: {str(e)}")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect("driver_form")

def updating_driver_info_save(request, driver_id=None):
    driver = None
    if driver_id:
        driver = get_object_or_404(SchoolDriver, id=driver_id)

    if request.method == 'POST':
        try:
            # Extract form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            license_number = request.POST.get('license_number')
            contact_number = request.POST.get('contact_number')
            address = request.POST.get('address')
            date_of_birth_str = request.POST.get('date_of_birth')
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            gender = request.POST.get('gender')
            profile_pic = request.FILES.get('profile_pic', None)
            driving_license_photo = request.FILES.get('driving_license_photo', None)

            # Perform validation
            if not all([first_name, last_name, date_of_birth]):
                messages.error(request, "Please provide all required fields")
                return redirect("add_driver_info")

            # Define accepted image formats
            accepted_image_formats = ['image/jpeg', 'image/jpg', 'image/png']
            accepted_pdf_format = 'application/pdf'

            # Define maximum file size in bytes (5MB)
            max_file_size = 5 * 1024 * 1024

            # Function to validate file format and size
            def validate_file(file, accepted_formats, max_size):
                if file.content_type not in accepted_formats:
                    raise ValueError(f"Invalid file format. Accepted formats: {', '.join(accepted_formats)}")

                if file.size > max_size:
                    raise ValueError(f"File size exceeds the limit. Maximum allowed size: {max_size} bytes")

            # Update the driver information in the database
            try:
                # Update the profile picture if provided
                if profile_pic:
                    validate_file(profile_pic, accepted_image_formats, max_file_size)

                    fs = FileSystemStorage()
                    filename = fs.save(profile_pic.name, profile_pic)
                    driver.profile_pic = fs.url(filename)

                # Update the driving license photo if provided
                if driving_license_photo:
                    validate_file(driving_license_photo, [accepted_pdf_format], max_file_size)

                    fs = FileSystemStorage()
                    filename = fs.save(driving_license_photo.name, driving_license_photo)
                    driver.driving_license_photo = fs.url(filename)

                # Update the driver record
                driver.admin.first_name = first_name
                driver.admin.last_name = last_name
                driver.license_number = license_number
                driver.contact_number = contact_number
                driver.address = address
                driver.date_of_birth = date_of_birth
                driver.gender = gender

                # Save the updated driver instance
                driver.admin.save()
                driver.save()

                messages.success(request, "Driver information updated successfully.")
                # Redirect to the next view with driver_id as a parameter
                if 'continue_filling' in request.POST:
                    return redirect(reverse('add_driver_medical_info', kwargs={'driver_id': driver.id}))
                else:
                    return redirect("driver_form")

            except Exception as e:
                messages.error(request, f"Error updating driver information: {str(e)}")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect("driver_form")


def add_driver_medical_info(request, driver_id):
    driver = get_object_or_404(SchoolDriver, id=driver_id)
    medical_info, created = SchoolDriverMedicalInfo.objects.get_or_create(driver=driver)

    if request.method == 'POST':
        try:
            # Extract form data
            blood_group = request.POST.get('blood_group')
            medical_conditions = request.POST.get('medical_conditions')
            health_condition = request.POST.get('health_condition')

            # Save the medical information to the database
            medical_info.blood_group = blood_group
            medical_info.medical_conditions = medical_conditions
            medical_info.health_condition = health_condition
            medical_info.save()

            messages.success(request, "Medical information saved successfully.")

            # Redirect to the next view or home page based on user's choice
            if 'continue_filling' in request.POST:
                # If the user wants to continue filling other forms, redirect to the next form view
                return redirect(reverse('add_driver_license_info', kwargs={'driver_id': driver_id}))
            else:
                # If the user wants to return to the home page, redirect to the home page view
                return redirect("home_page")

        except Exception as e:
            messages.error(request, f"Error saving medical information: {str(e)}")

    # Pass the existing medical_info to the template for pre-filling the form
    return render(request, 'hod_template/add_drivermedicalinfor.html', {'driver_id': driver_id, 'medical_info': medical_info})

def add_driver_license_info(request, driver_id):
    driver = get_object_or_404(SchoolDriver, id=driver_id)
    license_info, created = SchoolDriverLicenseInfo.objects.get_or_create(driver=driver)

    if request.method == 'POST':
        try:
            # Extract form data
            license_type = request.POST.get('license_type')
            drivers_license_expiry_reminder_str = request.POST.get('drivers_license_expiry_reminder')
            drivers_license_expiry_reminder = datetime.strptime(drivers_license_expiry_reminder_str, '%Y-%m-%d').date()
            additional_licenses = request.POST.get('additional_licenses')
            certification = request.POST.get('certification')
            driver_training_certifications = request.POST.get('driver_training_certifications')
            experience_in_transportation = request.POST.get('experience_in_transportation')

            # Save the license information to the database
            license_info.license_type = license_type
            license_info.drivers_license_expiry_reminder = drivers_license_expiry_reminder
            license_info.additional_licenses = additional_licenses
            license_info.certification = certification
            license_info.driver_training_certifications = driver_training_certifications
            license_info.experience_in_transportation = experience_in_transportation
            license_info.save()

            messages.success(request, "License information saved successfully.")

            # Redirect to the next view or home page based on user's choice
            if 'continue_filling' in request.POST:
                # If the user wants to continue filling other forms, redirect to the next form view
                return redirect(reverse('add_driver_contact_info', kwargs={'driver_id': driver_id}))
            else:
                # If the user wants to return to the home page, redirect to the home page view
                return redirect("home_page")

        except Exception as e:
            messages.error(request, f"Error saving license information: {str(e)}")

    # Pass the existing license_info to the template for pre-filling the form
    return render(request, 'hod_template/add_driverlicenceinfo.html', {'driver_id': driver_id, 'license_info': license_info})
def add_driver_contact_info(request, driver_id):
    driver = get_object_or_404(SchoolDriver, id=driver_id)
    contact_info, created = SchoolDriverContact.objects.get_or_create(driver=driver)

    if request.method == 'POST':
        try:
            # Extract form data
            alternate_contact_number = request.POST.get('alternate_contact_number')
            email = request.POST.get('email')

            # Save the contact information to the database
            contact_info.alternate_contact_number = alternate_contact_number
            contact_info.email = email
            contact_info.save()

            messages.success(request, "Contact information saved successfully.")

            # Redirect to the next view or home page based on user's choice
            if 'continue_filling' in request.POST:
                # If the user wants to continue filling other forms, redirect to the next form view
                return redirect(reverse('add_driver_emergency_contact_info', kwargs={'driver_id': driver_id}))
            else:
                # If the user wants to return to the home page, redirect to the home page view
                return redirect("driver_form")

        except Exception as e:
            messages.error(request, f"Error saving contact information: {str(e)}")

    # Pass the existing contact_info to the template for pre-filling the form
    return render(request, 'hod_template/add_drivercontactinfo.html', {'driver_id': driver_id, 'contact_info': contact_info})

def add_driver_emergency_contact_info(request, driver_id):
    driver = get_object_or_404(SchoolDriver, id=driver_id)
    emergency_contact_info, created = SchoolDriverEmergencyContact.objects.get_or_create(driver=driver)

    if request.method == 'POST':
        try:
            # Extract form data
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_number = request.POST.get('emergency_contact_number')
            emergency_contact_relationship = request.POST.get('emergency_contact_relationship')

            # Save the emergency contact information to the database
            emergency_contact_info.emergency_contact_name = emergency_contact_name
            emergency_contact_info.emergency_contact_number = emergency_contact_number
            emergency_contact_info.emergency_contact_relationship = emergency_contact_relationship
            emergency_contact_info.save()

            messages.success(request, "Emergency contact information saved successfully.")

            # Redirect to the next view or home page based on user's choice
            if 'continue_filling' in request.POST:
                # If the user wants to continue filling other forms, redirect to the next form view
                return redirect(reverse('add_driver_employment_info', kwargs={'driver_id': driver_id}))
            else:
                # If the user wants to return to the home page, redirect to the home page view
                return redirect("driver_form")

        except Exception as e:
            messages.error(request, f"Error saving emergency contact information: {str(e)}")

    # Pass the existing emergency_contact_info to the template for pre-filling the form
    return render(request, 'hod_template/add_driveremergencyinfo.html', {'driver_id': driver_id, 'emergency_contact_info': emergency_contact_info})


def add_driver_employment_info(request, driver_id):
    driver = get_object_or_404(SchoolDriver, id=driver_id)
    employment_info, created = SchoolDriverEmployment.objects.get_or_create(driver=driver)

    if request.method == 'POST':
        try:
            # Extract form data
            date_of_joining_str = request.POST.get('date_of_joining')
            date_of_joining = datetime.strptime(date_of_joining_str, '%Y-%m-%d').date()
            employment_start_date_str = request.POST.get('employment_start_date')
            employment_start_date = datetime.strptime(employment_start_date_str, '%Y-%m-%d').date()
            employment_end_date_str = request.POST.get('employment_end_date')
            employment_end_date = datetime.strptime(employment_end_date_str, '%Y-%m-%d').date()
            salary = request.POST.get('salary')
            salary_information = request.POST.get('salary_information')
            performance_ratings = request.POST.get('performance_ratings')
            shift_schedule = request.POST.get('shift_schedule')
            driving_hours = request.POST.get('driving_hours')
            uniform_size = request.POST.get('uniform_size')
            uniform_issued_date_str = request.POST.get('uniform_issued_date')
            uniform_issued_date = datetime.strptime(uniform_issued_date_str, '%Y-%m-%d').date()
            uniform_return_date_str = request.POST.get('uniform_return_date')
            uniform_return_date = datetime.strptime(uniform_return_date_str, '%Y-%m-%d').date()

            # Save the employment information to the database
            employment_info.date_of_joining = date_of_joining
            employment_info.employment_start_date = employment_start_date
            employment_info.employment_end_date = employment_end_date
            employment_info.salary = salary
            employment_info.salary_information = salary_information
            employment_info.performance_ratings = performance_ratings
            employment_info.shift_schedule = shift_schedule
            employment_info.driving_hours = driving_hours
            employment_info.uniform_size = uniform_size
            employment_info.uniform_issued_date = uniform_issued_date
            employment_info.uniform_return_date = uniform_return_date
            employment_info.save()

            messages.success(request, "Employment information saved successfully.")

            # Redirect to the next view or home page based on user's choice
            if 'continue_filling' in request.POST:
                # If the user wants to continue filling other forms, redirect to the next form view
                return redirect(reverse('add_driver_vehicle_info', kwargs={'driver_id': driver_id}))
            else:
                # If the user wants to return to the home page, redirect to home page view
                return redirect("driver_form")

        except Exception as e:
            messages.error(request, f"Error saving employment information: {str(e)}")

    # Pass the existing employment_info to the template for pre-filling the form
    return render(request, 'hod_template/add_driveremploymentinfo.html', {'driver_id': driver_id, 'employment_info': employment_info})


def add_driver_vehicle_info(request, driver_id):
    driver = get_object_or_404(SchoolDriver, id=driver_id)
    vehicle_info, created = SchoolDriverVehicle.objects.get_or_create(driver=driver)

    if request.method == 'POST':
        try:
            # Extract form data
            vehicle_assigned_id = request.POST.get('vehicle_assigned')
            vehicle_assigned = Car.objects.get(id=vehicle_assigned_id) if vehicle_assigned_id else None
            personal_vehicle_information = request.POST.get('personal_vehicle_information')
            vehicle_registration_number = request.POST.get('vehicle_registration_number')
            vehicle_maintenance_records = request.POST.get('vehicle_maintenance_records')

            # Save the vehicle information to the database
            vehicle_info.vehicle_assigned = vehicle_assigned
            vehicle_info.personal_vehicle_information = personal_vehicle_information
            vehicle_info.vehicle_registration_number = vehicle_registration_number
            vehicle_info.vehicle_maintenance_records = vehicle_maintenance_records
            vehicle_info.save()

            messages.success(request, "Vehicle information saved successfully.")

            # Redirect to the next view or home page based on user's choice
            if 'continue_filling' in request.POST:
                # If the user wants to continue filling other forms, redirect to the next form view
                return redirect(reverse('add_driver_languages', kwargs={'driver_id': driver_id}))
            else:
                # If the user wants to return to the home page, redirect to home page view
                return redirect("driver_form")

        except Exception as e:
            messages.error(request, f"Error saving vehicle information: {str(e)}")

    # Pass the existing vehicle_info to the template for pre-filling the form
    return render(request, 'hod_template/add_drivervehicleinfo.html', {'cars': Car.objects.all(), 'driver_id': driver_id, 'vehicle_info': vehicle_info})



def add_driver_languages(request, driver_id):
    driver = get_object_or_404(SchoolDriver, id=driver_id)
    spoken_languages = SchoolDriverLanguage.objects.filter(driver=driver)

    if request.method == 'POST':
        try:
            # Extract form data
            spoken_languages = request.POST.getlist('spoken_languages')

            # Save the spoken languages to the database
            # Clear existing spoken languages and add the new ones
            SchoolDriverLanguage.objects.filter(driver=driver).delete()
            for language in spoken_languages:
                SchoolDriverLanguage.objects.create(driver=driver, language=language)

            messages.success(request, "Spoken languages saved successfully.")

            # Redirect to the next view or home page based on user's choice
            if 'continue_filling' in request.POST:
                # If the user wants to continue filling other forms, redirect to the next form view
                return redirect(reverse('add_driver_references', kwargs={'driver_id': driver_id}))
            else:
                # If the user wants to return to the home page, redirect to home page view
                return redirect("driver_form")

        except Exception as e:
            messages.error(request, f"Error saving spoken languages: {str(e)}")

    # Pass the existing spoken_languages to the template for pre-filling the form
    return render(request, 'hod_template/add_driverlanguageinfo.html', {'driver_id': driver_id, 'spoken_languages': spoken_languages})


def add_driver_references(request, driver_id):
    driver = get_object_or_404(SchoolDriver, id=driver_id)
    references = SchoolDriverReference.objects.filter(driver=driver)

    if request.method == 'POST':
        try:
            # Extract form data
            reference_names = request.POST.getlist('reference_name')
            reference_contacts = request.POST.getlist('reference_contact')

            # Save the references to the database
            # Clear existing references and add the new ones
            SchoolDriverReference.objects.filter(driver=driver).delete()
            for name, contact in zip(reference_names, reference_contacts):
                SchoolDriverReference.objects.create(driver=driver, reference_name=name, reference_contact=contact)

            messages.success(request, "References saved successfully.")

            # Redirect to home page view as this is the last form
            return redirect("driver_form")

        except Exception as e:
            messages.error(request, f"Error saving references: {str(e)}")

    # Pass the existing references to the template for pre-filling the form
    return render(request, 'hod_template/add_driverreference.html', {'references': references})


def manage_driver(request):
    # Retrieve all Securitys from the database
    drivers = SchoolDriver.objects.all()

    return render(request, 'hod_template/manage_schooldriver.html', {'drivers': drivers})

def view_driver_info(request, driver_id):
    driver = get_object_or_404(SchoolDriver.objects.select_related(
        'admin', 'medical_info', 'license_info', 'contact_info',
        'employment_info', 'vehicle_info'
    ).prefetch_related('languages_spoken', 'references'), id=driver_id)
    
    context = {'driver': driver}
    return render(request, 'hod_template/details_schooldriver.html', context)

def update_driver_info(request, driver_id):
    driver = get_object_or_404(SchoolDriver, id=driver_id)
    context = {'driver': driver}
    return render(request, 'hod_template/edit_schooldriver.html', context)



def add_security_person_info_save(request):
    if request.method == 'POST':
        try:
            # Extract form data
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            contact_number = request.POST.get('contact_number')
            address = request.POST.get('address')
            date_of_birth_str = request.POST.get('date_of_birth')
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            gender = request.POST.get('gender')
            profile_pic = request.FILES.get('profile_pic', None)
            security_clearance_expiry_str = request.POST.get('security_clearance_expiry')
            security_clearance_expiry = datetime.strptime(security_clearance_expiry_str, '%Y-%m-%d').date()
            patrol_area = request.POST.get('patrol_area')
            security_training_courses = request.POST.get('security_training_courses')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_number = request.POST.get('emergency_contact_number')
            shift_start_time_str = request.POST.get('shift_start_time')
            shift_start_time = datetime.strptime(shift_start_time_str, '%H:%M').time()
            shift_end_time_str = request.POST.get('shift_end_time')
            shift_end_time = datetime.strptime(shift_end_time_str, '%H:%M').time()
            years_of_experience = request.POST.get('years_of_experience')
            uniform_size = request.POST.get('uniform_size')
            vehicle_assigned_id = request.POST.get('vehicle_assigned')
            vehicle_assigned = None
            if vehicle_assigned_id:
                try:
                    vehicle_assigned_id = int(vehicle_assigned_id)
                    vehicle_assigned = get_object_or_404(Car, pk=vehicle_assigned_id)
                except ValueError:
                    # Invalid vehicle_assigned_id, handle the error accordingly
                    messages.error(request, "Invalid vehicle_assigned_id")
                    return redirect("add_security_person")
            # Perform validation for required fields
            required_fields = [username, email, first_name, last_name, password, contact_number, address, date_of_birth]
            if not all(required_fields):
                messages.error(request, "Please provide all required fields")
                return redirect("add_security_person")

            # Validate email uniqueness
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists. Please use a different email.")
                return redirect("add_security_person")

            # Validate username uniqueness
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please use a different username.")
                return redirect("add_security_person")

            # Define accepted image formats
            accepted_image_formats = ['image/jpeg', 'image/jpg', 'image/png']

            # Define maximum file size in bytes (5MB)
            max_file_size = 5 * 1024 * 1024

            # Function to validate file format and size
            def validate_file(file, accepted_formats, max_size):
                if file.content_type not in accepted_formats:
                    raise ValidationError(f"Invalid file format. Accepted formats: {', '.join(accepted_formats)}")

                if file.size > max_size:
                    raise ValidationError(f"File size exceeds the limit. Maximum allowed size: {max_size} bytes")

            # Save the Security information to the database
            try:
                # Save the profile picture
                profile_pic_url = None
                if profile_pic:
                    validate_file(profile_pic, accepted_image_formats, max_file_size)

                    fs = FileSystemStorage()
                    filename = fs.save(profile_pic.name, profile_pic)
                    profile_pic_url = fs.url(filename)

                # Create the User instance (Django built-in User model)
                user = CustomUser.objects.create_user(username=username, email=email, password=password,
                                                      first_name=first_name, last_name=last_name,
                                                      user_type=5)  # Security user type

                # Create or update the corresponding Security instance
                security_person, security_created = SchoolSecurityPerson.objects.get_or_create(admin=user)
                security_person.contact_number = contact_number
                security_person.address = address
                security_person.date_of_birth = date_of_birth
                security_person.gender = gender
                security_person.security_clearance_expiry = security_clearance_expiry
                security_person.uniform_size = uniform_size
                security_person.patrol_area = patrol_area
                security_person.emergency_contact_number = emergency_contact_number
                security_person.emergency_contact_name = emergency_contact_name
                security_person.years_of_experience = years_of_experience
                security_person.security_training_courses = security_training_courses
                security_person.shift_start_time = shift_start_time
                security_person.shift_end_time = shift_end_time
                security_person.vehicle_assigned = vehicle_assigned
                security_person.profile_pic = profile_pic_url

                # Save the Security record
                security_person.save()

                messages.success(request, "Security information saved successfully.")
                # Redirect to the next view with Security_id as a parameter
                # Modify the URL pattern accordingly              
                return redirect("add_security_person")

            except Exception as e:
                messages.error(request, f"Error saving security information: {str(e)}")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect("add_security_person")


def manage_security(request):
    # Retrieve all Securitys from the database
    securitys = SchoolSecurityPerson.objects.all()

    return render(request, 'hod_template/manage_schoolsecurity.html', {'securitys': securitys})

def view_security_info(request, security_id):
    security = get_object_or_404(SchoolSecurityPerson, id=security_id)
    context = {'security': security}
    return render(request, 'hod_template/details_schoolsecurity.html', context)

def update_security_info(request, security_id):
    security = get_object_or_404(SchoolSecurityPerson, id=security_id)
    context = {'security': security}
    return render(request, 'hod_template/edit_schoolsecurity.html', context)



def update_security_info_save(request, security_id=None):
    if request.method == 'POST':
        try:
            # Extract form data
            # Extract form data        
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')            
            contact_number = request.POST.get('contact_number')
            address = request.POST.get('address')
            date_of_birth_str = request.POST.get('date_of_birth')
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            gender = request.POST.get('gender')
            profile_pic = request.FILES.get('profile_pic', None)
            security_clearance_expiry_str = request.POST.get('security_clearance_expiry')
            security_clearance_expiry = datetime.strptime(security_clearance_expiry_str, '%Y-%m-%d').date()
            patrol_area = request.POST.get('patrol_area')
            security_training_courses = request.POST.get('security_training_courses')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_number = request.POST.get('emergency_contact_number')
            shift_start_time_str = request.POST.get('shift_start_time')
            shift_start_time = datetime.strptime(shift_start_time_str, '%H:%M').time()
            shift_end_time_str = request.POST.get('shift_end_time')
            shift_end_time = datetime.strptime(shift_end_time_str, '%H:%M').time()
            years_of_experience = request.POST.get('years_of_experience')
            uniform_size = request.POST.get('uniform_size')
            vehicle_assigned_id = request.POST.get('vehicle_assigned')
            
            
            vehicle_assigned = None
            if vehicle_assigned_id:
                try:
                    vehicle_assigned_id = int(vehicle_assigned_id)
                    vehicle_assigned = get_object_or_404(Car, pk=vehicle_assigned_id)
                except ValueError:
                    # Invalid vehicle_assigned_id, handle the error accordingly
                    messages.error(request, "Invalid vehicle_assigned_id")
                    return redirect("add_security_person")

            # Perform validation for required fields
            required_fields = [first_name, last_name, contact_number, address, date_of_birth]
            if not all(required_fields):
                messages.error(request, "Please provide all required fields")
                return redirect("update_security_info", security_id=security_id)

            # Check if cooker_id is provided for updating the record
            if security_id:
                try:
                    security_person = SchoolSecurityPerson.objects.get(pk=security_id)
                except SchoolSecurityPerson.DoesNotExist:
                    messages.error(request, "Security does not exist.")
                    return redirect("update_security_info", security_id=security_id)
            else:
                security_person = SchoolSecurityPerson()

            # Save the cooker information to the database
            security_person.admin.first_name = first_name
            security_person.admin.last_name = last_name
            security_person.contact_number = contact_number
            security_person.address = address
            security_person.date_of_birth = date_of_birth
            security_person.gender = gender
            security_person.security_clearance_expiry = security_clearance_expiry
            security_person.uniform_size = uniform_size
            security_person.patrol_area = patrol_area
            security_person.emergency_contact_name = emergency_contact_name
            security_person.emergency_contact_number = emergency_contact_number
            security_person.shift_start_time = shift_start_time
            security_person.shift_end_time = shift_end_time
            security_person.years_of_experience = years_of_experience
            security_person.security_training_courses = security_training_courses
            security_person.vehicle_assigned = vehicle_assigned

            # Save the profile picture
            profile_pic = request.FILES.get('profile_pic', None)
            if profile_pic:
                accepted_image_formats = ['image/jpeg', 'image/jpg', 'image/png']
                max_file_size = 5 * 1024 * 1024  # 5MB

                if profile_pic.content_type not in accepted_image_formats:
                    messages.error(request, "Invalid file format. Accepted formats: JPG, JPEG, PNG")
                    return redirect(reverse('update_security_info', kwargs={'security_id': security_person.id}))

                if profile_pic.size > max_file_size:
                    messages.error(request, "File size exceeds the limit. Maximum allowed size: 5MB")
                    return redirect(reverse('update_security_info', kwargs={'security_id': security_person.id}))

                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
                security_person.profile_pic = profile_pic_url

            # Save the security record
            security_person.save()

            messages.success(request, "security information updated successfully.")
            # Redirect to the next view with security_id as a parameter
            # Modify the URL pattern accordingly
           
            return redirect(reverse('update_security_info', kwargs={'security_id': security_person.id}))

        except Exception as e:
            messages.error(request, f"Error on updating security information: {str(e)}")

    return redirect(reverse('update_security_info', kwargs={'security_id': security_id}))




def add_cooker_info_save(request):
    if request.method == 'POST':
        try:
            # Extract form data
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            contact_number = request.POST.get('contact_number')
            address = request.POST.get('address')
            date_of_birth_str = request.POST.get('date_of_birth')
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            gender = request.POST.get('gender')
            cooking_shift_hours = request.POST.get('cooking_shift_hours')
            uniform_size = request.POST.get('uniform_size')
            special_dietary_requirements = request.POST.get('special_dietary_requirements')
            emergency_contact_number = request.POST.get('emergency_contact_number')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            years_of_experience = request.POST.get('years_of_experience')
            performance_ratings = request.POST.get('performance_ratings')
            profile_pic = request.FILES.get('profile_pic', None)

            # Perform validation for required fields
            required_fields = [username, email, first_name, last_name, password, contact_number, address, date_of_birth]
            if not all(required_fields):
                messages.error(request, "Please provide all required fields")
                return redirect("add_cooker_info")

            # Validate email uniqueness
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists. Please use a different email.")
                return redirect("add_cooker_info")

            # Validate username uniqueness
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please use a different username.")
                return redirect("add_cooker_info")

            # Define accepted image formats
            accepted_image_formats = ['image/jpeg', 'image/jpg', 'image/png']

            # Define maximum file size in bytes (5MB)
            max_file_size = 5 * 1024 * 1024

            # Function to validate file format and size
            def validate_file(file, accepted_formats, max_size):
                if file.content_type not in accepted_formats:
                    raise ValidationError(f"Invalid file format. Accepted formats: {', '.join(accepted_formats)}")

                if file.size > max_size:
                    raise ValidationError(f"File size exceeds the limit. Maximum allowed size: {max_size} bytes")

            # Save the cooker information to the database
            try:
                # Save the profile picture
                profile_pic_url = None
                if profile_pic:
                    validate_file(profile_pic, accepted_image_formats, max_file_size)

                    fs = FileSystemStorage()
                    filename = fs.save(profile_pic.name, profile_pic)
                    profile_pic_url = fs.url(filename)

                # Create the User instance (Django built-in User model)
                user = CustomUser.objects.create_user(username=username, email=email, password=password,
                                                      first_name=first_name, last_name=last_name,
                                                      user_type=6)  # Cooker user type

                # Create or update the corresponding Cooker instance
                cooker, cooker_created = Cooker.objects.get_or_create(admin=user)
                cooker.contact_number = contact_number
                cooker.address = address
                cooker.date_of_birth = date_of_birth
                cooker.gender = gender
                cooker.cooking_shift_hours = cooking_shift_hours
                cooker.uniform_size = uniform_size
                cooker.special_dietary_requirements = special_dietary_requirements
                cooker.emergency_contact_number = emergency_contact_number
                cooker.emergency_contact_name = emergency_contact_name
                cooker.years_of_experience = years_of_experience
                cooker.performance_ratings = performance_ratings
                cooker.profile_pic = profile_pic_url

                # Save the Cooker record
                cooker.save()

                messages.success(request, "Cooker information saved successfully.")
                # Redirect to the next view with cooker_id as a parameter
                # Modify the URL pattern accordingly              
                return redirect("add_cooker")

            except Exception as e:
                messages.error(request, f"Error saving cooker information: {str(e)}")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect("add_cooker")

def manage_cooker(request):
    # Retrieve all cookers from the database
    cookers = Cooker.objects.all()

    return render(request, 'hod_template/manage_schoolcooker.html', {'cookers': cookers})

def view_cooker_info(request, cooker_id):
    cooker = get_object_or_404(Cooker, id=cooker_id)
    context = {'cooker': cooker}
    return render(request, 'hod_template/details_schoolcooker.html', context)

def update_cooker_info(request, cooker_id):
    cooker = get_object_or_404(Cooker, id=cooker_id)
    context = {'cooker': cooker}
    return render(request, 'hod_template/edit_schoolcooker.html', context)

def update_cooker_info_save(request, cooker_id=None):
    if request.method == 'POST':
        try:
            # Extract form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            contact_number = request.POST.get('contact_number')
            address = request.POST.get('address')
            date_of_birth_str = request.POST.get('date_of_birth')
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            gender = request.POST.get('gender')
            cooking_shift_hours = request.POST.get('cooking_shift_hours')
            uniform_size = request.POST.get('uniform_size')
            special_dietary_requirements = request.POST.get('special_dietary_requirements')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_number = request.POST.get('emergency_contact_number')
            years_of_experience = request.POST.get('years_of_experience')
            performance_ratings = request.POST.get('performance_ratings')

            # Perform validation for required fields
            required_fields = [first_name, last_name, contact_number, address, date_of_birth]
            if not all(required_fields):
                messages.error(request, "Please provide all required fields")
                return redirect("update_cooker_info", cooker_id=cooker_id)

            # Check if cooker_id is provided for updating the record
            if cooker_id:
                try:
                    cooker = Cooker.objects.get(pk=cooker_id)
                except Cooker.DoesNotExist:
                    messages.error(request, "Cooker does not exist.")
                    return redirect("update_cooker_info", cooker_id=cooker_id)
            else:
                cooker = Cooker()

            # Save the cooker information to the database
            cooker.admin.first_name = first_name
            cooker.admin.last_name = last_name
            cooker.contact_number = contact_number
            cooker.address = address
            cooker.date_of_birth = date_of_birth
            cooker.gender = gender
            cooker.cooking_shift_hours = cooking_shift_hours
            cooker.uniform_size = uniform_size
            cooker.special_dietary_requirements = special_dietary_requirements
            cooker.emergency_contact_name = emergency_contact_name
            cooker.emergency_contact_number = emergency_contact_number
            cooker.years_of_experience = years_of_experience
            cooker.performance_ratings = performance_ratings

            # Save the profile picture
            profile_pic = request.FILES.get('profile_pic', None)
            if profile_pic:
                accepted_image_formats = ['image/jpeg', 'image/jpg', 'image/png']
                max_file_size = 5 * 1024 * 1024  # 5MB

                if profile_pic.content_type not in accepted_image_formats:
                    messages.error(request, "Invalid file format. Accepted formats: JPG, JPEG, PNG")
                    return redirect(reverse('update_cooker_info', kwargs={'cooker_id': cooker.id}))

                if profile_pic.size > max_file_size:
                    messages.error(request, "File size exceeds the limit. Maximum allowed size: 5MB")
                    return redirect(reverse('update_cooker_info', kwargs={'cooker_id': cooker.id}))

                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
                cooker.profile_pic = profile_pic_url

            # Save the Cooker record
            cooker.save()

            messages.success(request, "Cooker information updated successfully.")
            # Redirect to the next view with cooker_id as a parameter
            # Modify the URL pattern accordingly
           
            return redirect(reverse('update_cooker_info', kwargs={'cooker_id': cooker.id}))

        except Exception as e:
            messages.error(request, f"Error on updating cooker information: {str(e)}")

    return redirect(reverse('update_cooker_info', kwargs={'cooker_id': cooker.id}))



def add_schoolcleaner_info_save(request):
    if request.method == 'POST':
        try:
            # Extract form data
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            cleaning_duties = request.POST.get('cleaning_duties')
            contact_number = request.POST.get('contact_number')
            address = request.POST.get('address')
            date_of_birth_str = request.POST.get('date_of_birth')
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            gender = request.POST.get('gender')
            cooking_shift_hours = request.POST.get('cooking_shift_hours')
            uniform_size = request.POST.get('uniform_size')
            
            emergency_contact_number = request.POST.get('emergency_contact_number')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            years_of_experience = request.POST.get('years_of_experience')
            performance_ratings = request.POST.get('performance_ratings')
            profile_pic = request.FILES.get('profile_pic', None)

            # Perform validation for required fields
            required_fields = [username, email, first_name, last_name, password, contact_number, address, date_of_birth]
            if not all(required_fields):
                messages.error(request, "Please provide all required fields")
                return redirect("add_schoolcleaner")

            # Validate email uniqueness
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists. Please use a different email.")
                return redirect("add_schoolcleaner")

            # Validate username uniqueness
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please use a different username.")
                return redirect("add_schoolcleaner")

            # Define accepted image formats
            accepted_image_formats = ['image/jpeg', 'image/jpg', 'image/png']

            # Define maximum file size in bytes (5MB)
            max_file_size = 5 * 1024 * 1024

            # Function to validate file format and size
            def validate_file(file, accepted_formats, max_size):
                if file.content_type not in accepted_formats:
                    raise ValidationError(f"Invalid file format. Accepted formats: {', '.join(accepted_formats)}")

                if file.size > max_size:
                    raise ValidationError(f"File size exceeds the limit. Maximum allowed size: {max_size} bytes")

            # Save the cooker information to the database
            try:
                # Save the profile picture
                profile_pic_url = None
                if profile_pic:
                    validate_file(profile_pic, accepted_image_formats, max_file_size)

                    fs = FileSystemStorage()
                    filename = fs.save(profile_pic.name, profile_pic)
                    profile_pic_url = fs.url(filename)

                # Create the User instance (Django built-in User model)
                user = CustomUser.objects.create_user(username=username, email=email, password=password,
                                                      first_name=first_name, last_name=last_name,
                                                      user_type=7)  # Cooker user type

                # Create or update the corresponding Cooker instance
                cleaner, cleaner_created = SchoolCleaner.objects.get_or_create(admin=user)
                cleaner.contact_number = contact_number
                cleaner.address = address
                cleaner.date_of_birth = date_of_birth
                cleaner.gender = gender
                cleaner.cleaning_shift_hours = cooking_shift_hours
                cleaner.uniform_size = uniform_size
                cleaner.cleaning_duties = cleaning_duties
                cleaner.emergency_contact_number = emergency_contact_number
                cleaner.emergency_contact_name = emergency_contact_name
                cleaner.years_of_experience = years_of_experience
                cleaner.performance_ratings = performance_ratings
                cleaner.profile_pic = profile_pic_url

                # Save the Cooker record
                cleaner.save()

                messages.success(request, "cleaner information saved successfully.")
                # Redirect to the next view with cooker_id as a parameter
                # Modify the URL pattern accordingly              
                return redirect("add_schoolcleaner")

            except Exception as e:
                messages.error(request, f"Error saving cleaner information: {str(e)}")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect("add_schoolcleaner")


def manage_cleaner(request):
    # Retrieve all cookers from the database
    cleaners = SchoolCleaner.objects.all()
    return render(request, 'hod_template/manage_schoolcleaner.html', {'cleaners': cleaners})

def view_cleaner_info(request, cleaner_id):
    cleaner = get_object_or_404(SchoolCleaner, id=cleaner_id)
    context = {'cleaner': cleaner}
    return render(request, 'hod_template/details_schoolcleaner.html', context)

def update_cleaner_info(request, cleaner_id):
    cleaner = get_object_or_404(SchoolCleaner, id=cleaner_id)
    context = {'cleaner': cleaner}
    return render(request, 'hod_template/edit_schoolcleaner.html', context)

def update_cleaner_info_save(request, cleaner_id=None):
    if request.method == 'POST':
        try:
            # Extract form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            contact_number = request.POST.get('contact_number')
            cleaning_duties = request.POST.get('cleaning_duties')
            address = request.POST.get('address')
            date_of_birth_str = request.POST.get('date_of_birth')
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            gender = request.POST.get('gender')
            cooking_shift_hours = request.POST.get('cooking_shift_hours')
            uniform_size = request.POST.get('uniform_size')            
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_number = request.POST.get('emergency_contact_number')
            years_of_experience = request.POST.get('years_of_experience')
            performance_ratings = request.POST.get('performance_ratings')

            # Perform validation for required fields
            required_fields = [first_name, last_name, contact_number, address, date_of_birth]
            if not all(required_fields):
                messages.error(request, "Please provide all required fields")
                return redirect("update_cooker_info", cooker_id=cleaner_id)

            # Check if cooker_id is provided for updating the record
            if cleaner_id:
                try:
                    cleaner = SchoolCleaner.objects.get(pk=cleaner_id)
                except SchoolCleaner.DoesNotExist:
                    messages.error(request, "Cooker does not exist.")
                    return redirect("update_cooker_info", cleaner_id=cleaner_id)
            else:
                cleaner = SchoolCleaner()

            # Save the cooker information to the database
            cleaner.admin.first_name = first_name
            cleaner.admin.last_name = last_name
            cleaner.contact_number = contact_number
            cleaner.address = address
            cleaner.date_of_birth = date_of_birth
            cleaner.gender = gender
            cleaner.cleaning_shift_hours = cooking_shift_hours
            cleaner.uniform_size = uniform_size
            cleaner.cleaning_duties = cleaning_duties
            cleaner.emergency_contact_name = emergency_contact_name
            cleaner.emergency_contact_number = emergency_contact_number
            cleaner.years_of_experience = years_of_experience
            cleaner.performance_ratings = performance_ratings

            # Save the profile picture
            profile_pic = request.FILES.get('profile_pic', None)
            if profile_pic:
                accepted_image_formats = ['image/jpeg', 'image/jpg', 'image/png']
                max_file_size = 5 * 1024 * 1024  # 5MB

                if profile_pic.content_type not in accepted_image_formats:
                    messages.error(request, "Invalid file format. Accepted formats: JPG, JPEG, PNG")
                    return redirect(reverse('update_cleaner_info', kwargs={'cleaner_id': cleaner.id}))

                if profile_pic.size > max_file_size:
                    messages.error(request, "File size exceeds the limit. Maximum allowed size: 5MB")
                    return redirect(reverse('update_cleaner_info', kwargs={'cleaner_id': cleaner.id}))

                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
                cleaner.profile_pic = profile_pic_url

            # Save the Cooker record
            cleaner.save()

            messages.success(request, "cleaner information updated successfully.")
            # Redirect to the next view with cooker_id as a parameter
            # Modify the URL pattern accordingly
           
            return redirect(reverse('update_cleaner_info', kwargs={'cleaner_id': cleaner.id}))

        except Exception as e:
            messages.error(request, f"Error on updating cleaner information: {str(e)}")

    return redirect(reverse('update_cleaner_info', kwargs={'cleaner_id': cleaner.id}))






def add_car_save(request):
    if request.method == 'POST':
        # Retrieve the data from the request.POST dictionary
        make = request.POST.get('make')
        model = request.POST.get('model')
        year = request.POST.get('year')
        license_plate = request.POST.get('license_plate')
        color = request.POST.get('color')
        owner_id = request.POST.get('owner')

        # Check if the owner_id is valid and exists in the SchoolDriver model
        try:
            owner = SchoolDriver.objects.get(id=owner_id)
        except SchoolDriver.DoesNotExist:
            owner = None

        try:
            # Create a new Car instance and save it to the database
            car = Car(make=make, model=model, year=year, license_plate=license_plate, color=color, owner=owner)
            car.save()

            # Add a success message
            messages.success(request, "Car information saved successfully.")

            # Redirect to a success page or any other page as per your requirement
            return redirect('add_schoolcar_view')

        except Exception as e:
            # Add an error message with the exception message
            messages.error(request, f"Error saving car information: {str(e)}")

    # If it's a GET request or if there was an error in saving the car information
    # Render the template with an empty form instance
    return redirect('add_schoolcar_view')


def add_classroom_save(request):
    if request.method == 'POST':
        # Retrieve the data from the request.POST dictionary
        name = request.POST.get('name')
        grade_level = request.POST.get('grade_level')
        capacity = request.POST.get('capacity')
        room_number = request.POST.get('room_number')
        building = request.POST.get('building')
        description = request.POST.get('description')
        
        class_rules = request.POST.get('class_rules')
        class_events = request.POST.get('class_events')
        additional_notes = request.POST.get('additional_notes')

        try:
            # Create a new Classroom instance and save it to the database
            classroom = Classroom(
                name=name,
                grade_level=grade_level,
                capacity=capacity,
                room_number=room_number,
                building=building,
                description=description,
                
                class_rules=class_rules,
                class_events=class_events,
                additional_notes=additional_notes,
            )
            classroom.save()

            # Add a success message
            messages.success(request, "Classroom information saved successfully.")

            # Redirect to a success page or any other page as per your requirement
            return redirect('add_schoolclassroom')

        except Exception as e:
            # Add an error message with the exception message
            messages.error(request, f"Error saving classroom information: {str(e)}")

    # If it's a GET request or if there was an error in saving the classroom information
    # Render the template with an empty form instance
    return redirect('add_schoolclassroom')

def manage_classroom(request):
    classrooms = Classroom.objects.all()
    return render(request, 'hod_template/manage_classroom.html', {'courses': classrooms})

def delete_classroom(request, classroom_id):
    # Get the classroom object from the database
    classroom = get_object_or_404(Classroom, pk=classroom_id)

    if request.method == 'POST':
        # Handle the deletion of the classroom here
        classroom.delete()
        return redirect('manage_classroom')  # Redirect to a page after successful deletion

    # Render a confirmation template if using a separate confirmation page
    return redirect('manage_classroom')


def classroom_detail(request, classroom_id):
    # Get the classroom object from the database
    classroom = get_object_or_404(Classroom, pk=classroom_id)

    return render(request, 'hod_template/details_schoolclassroom.html', {'classroom': classroom})


def update_classroom(request, classroom_id):
    # Assuming 'classroom_id' is the primary key of the classroom to be updated
    classroom = Classroom.objects.get(pk=classroom_id)
    context = {'classroom': classroom}
    return render(request, 'hod_template/edit_schoolclassroom.html', context)

def update_classroom_save(request, classroom_id=None):
    if classroom_id:
        # If 'classroom_id' is provided, fetch the classroom instance for updating
        try:
            classroom = Classroom.objects.get(pk=classroom_id)
        except Classroom.DoesNotExist:
            messages.error(request, 'Classroom does not exist.')
            return redirect(reverse('update_classroom', kwargs={'classroom_id':classroom_id})) # Replace 'error_page' with your desired URL name for showing error messages

    else:
        # If no 'classroom_id', create a new Classroom instance for adding
        classroom = Classroom()

    if request.method == 'POST':
        # If the form is submitted, process the data
        classroom.name = request.POST.get('name', '')
        classroom.grade_level = request.POST.get('grade_level', '')
        classroom.capacity = request.POST.get('capacity', None)
        classroom.room_number = request.POST.get('room_number', '')
        classroom.building = request.POST.get('building', '')
        classroom.description = request.POST.get('description', '')
        classroom.class_rules = request.POST.get('class_rules', '')
        classroom.class_events = request.POST.get('class_events', '')
        classroom.additional_notes = request.POST.get('additional_notes', '')

        try:
            classroom.save()
            messages.success(request, 'Classroom information updated successfully.')
            return redirect(reverse('update_classroom', kwargs={'classroom_id':classroom_id})) # Replace 'success_page' with your desired URL name for showing success messages
        except Exception as e:
            messages.error(request, f'Error updating classroom information: {str(e)}')
            return redirect(reverse('update_classroom', kwargs={'classroom_id':classroom_id}))  # Replace 'error_page' with your desired URL name for showing error messages

    # If it's a GET request, render the template with the classroom data (if updating)
    return render(request, 'hod_template/edit_schoolclassroom.html', {'classroom': classroom})




def update_classroom_status(request, classroom_id):
    if request.method == 'POST':
        # Get the classroom object from the database
        classroom = get_object_or_404(Classroom, pk=classroom_id)

        # Get the new status from the request data
        is_active = request.POST.get('is_active', False)
        print(is_active)
        # Update the classroom status
        classroom.is_active = is_active
        classroom.save()

        # Return the updated classroom status as JSON response
        return JsonResponse({'status': 'success', 'is_active': classroom.is_active})

    # If the request method is not POST, return a JSON response with an error message
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



def add_staff(request):  
    forms = AddStaffForm()  
    all_subjects = Subject.objects.all()
    return render(request,"hod_template/add_staff.html",{"forms":forms,"all_subjects":all_subjects})

def primery_table(request):     
    return render(request,"hod_template/primery_table.html")

def secondary_timetable(request):     
    return render(request,"hod_template/secondary_timetable.html")



def add_staff_save(request):
    if request.method == "POST":
        try:
            # Extract form data
            first_name = request.POST.get('first_name')
            email = request.POST.get('email')
            username = request.POST.get('username')            
            surname = request.POST.get('surname')            
            background_check = request.POST.get('background_check')            
            availability = request.POST.get('availability')            
            preferred_grade_level = request.POST.get('preferred_grade_level')            
            salary_expectations = request.POST.get('salary_expectations')            
            personal_statement = request.POST.get('personal_statement')            
            national_identity_number = request.POST.get('national_identity_number')            
            personal_statement = request.POST.get('personal_statement')            
            subjects = request.POST.getlist('subjects')  # Use getlist to retrieve multiple selected values           
            password = request.POST.get('password')            
            last_name = request.POST.get('last_name')
            date_of_birth_str = request.POST.get('date_of_birth')
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            gender = request.POST.get('gender')            
            phone_number = request.POST.get('contact_number')          
            sheia_address = request.POST.get('sheia_address')
            street_address = request.POST.get('street_address')
            house_number = request.POST.get('house_number')

            # Perform validation
            if not first_name or not last_name or not date_of_birth:
                messages.error(request, "Please provide all required fields")
                return redirect("addstaff")

            # Define accepted file formats
            accepted_image_formats = ['image/jpeg', 'image/jpg', 'image/png']
            accepted_pdf_format = 'application/pdf'

            # Define maximum file size in bytes (5MB)
            max_file_size = 5 * 1024 * 1024

            # Function to validate file format and size
            def validate_file(file: InMemoryUploadedFile, accepted_formats, max_size):
                if file.content_type not in accepted_formats:
                    raise ValueError(f"Invalid file format. Accepted formats: {', '.join(accepted_formats)}")

                if file.size > max_size:
                    raise ValueError(f"File size exceeds the limit. Maximum allowed size: {max_size} bytes")

            # Save the form data to the database
            try:
                # Save the staff's profile picture
                staff_photo_url = None
                staff_photo = request.FILES.get('staff_photo')
                if staff_photo:
                    validate_file(staff_photo, accepted_image_formats, max_file_size)

                    fs = FileSystemStorage()
                    filename = fs.save(staff_photo.name, staff_photo)
                    staff_photo_url = fs.url(filename)

                # Save the birth certificate photo
                birth_certificate_photo_url = None
                birth_certificate_photo = request.FILES.get('birth_certificate_photo')
                if birth_certificate_photo:
                    validate_file(birth_certificate_photo, accepted_image_formats + [accepted_pdf_format], max_file_size)

                    fs = FileSystemStorage()
                    filename = fs.save(birth_certificate_photo.name, birth_certificate_photo)
                    birth_certificate_photo_url = fs.url(filename)

                # Save the national ID photo
                national_id_photo_url = None
                national_id_photo = request.FILES.get('national_id_photo')
                if national_id_photo:
                    validate_file(national_id_photo, accepted_image_formats + [accepted_pdf_format], max_file_size)

                    fs = FileSystemStorage()
                    filename = fs.save(national_id_photo.name, national_id_photo)
                    national_id_photo_url = fs.url(filename)

                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
                
                # Create a new instance of the Staff model           
                staff = user.staffs
                staff.background_check = background_check
                staff.availability = availability
                staff.preferred_grade_level = preferred_grade_level
                staff.salary_expectations = salary_expectations
                staff.personal_statement = personal_statement
                staff.national_identity_number = national_identity_number
                staff.date_of_birth = date_of_birth
                staff.gender = gender
                staff.surname = surname                
                staff.contact_number = phone_number          
                staff.address = sheia_address
                staff.street_address = street_address
                staff.house_number = house_number
                staff.profile_pic = staff_photo_url
                staff.national_id_photo = national_id_photo_url
                staff.birth_certificate_photo = birth_certificate_photo_url

                # Save the staff record
                staff.save()
                
                # Assign subjects to the staff
                staff.subjects.set(subjects)

                messages.success(request, "Successfully added staff")
                return redirect(reverse('qualification_form', kwargs={'staff_id': user.staffs.id}))
            except Exception as e:
                messages.error(request, f"Error saving staff record: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect("addstaff")


def qualifications_form(request, staff_id):
    if request.method == 'POST':
        # Retrieve form data
        teaching_experience = request.POST.get('teaching_experience')
        educational_qualification = request.POST.get('educational_qualification')
        certification = request.POST.get('certification')
        cv = request.FILES.get('cv')
        other_certificates = request.FILES.get('other_certificates')

        try:
            # Validate the CV and other certificate formats
            if cv and not cv.name.endswith('.pdf'):
                raise ValueError('Invalid CV format. Only PDF files are allowed.')

            if other_certificates and not other_certificates.name.endswith('.pdf'):
                raise ValueError('Invalid other certificate format. Only PDF files are allowed.')

            # Save the CV and other certificate files
            cv_url = None
            if cv:
                fs = FileSystemStorage()
                filename = fs.save(cv.name, cv)
                cv_url = fs.url(filename)

            other_certificates_url = None
            if other_certificates:
                fs = FileSystemStorage()
                filename = fs.save(other_certificates.name, other_certificates)
                other_certificates_url = fs.url(filename)

            # Save the form data to the database
            qualifications = Qualifications.objects.create(
                staff_id=staff_id,
                teaching_experience=teaching_experience,
                educational_qualification=educational_qualification,
                certification=certification,
                cv=cv_url,
                other_certificates=other_certificates_url,
            )

            messages.success(request, "Qualifications successfully added.")
            return redirect(reverse('skills_form', kwargs={'staff_id': staff_id}))
        except Exception as e:
            messages.error(request, f"Error saving qualifications: {str(e)}")

    return render(request, 'hod_template/add_qualification.html', {'staff_id': staff_id})


def edit_staff_qualification(request, staff_id):
    try:
        staff = Staffs.objects.get(id=staff_id)
    except ObjectDoesNotExist:
        messages.error(request, "Staff not found")
        return redirect("manage_staff")

    qualification, created = Qualifications.objects.get_or_create(staff=staff)

    if request.method == "POST":
        try:
            teaching_experience = request.POST.get('teaching_experience')
            educational_qualification = request.POST.get('educational_qualification')
            certification = request.POST.get('certification')
            cv = request.FILES.get('cv')
            other_certificates = request.FILES.get('other_certificates')

            qualification.teaching_experience = teaching_experience
            qualification.educational_qualification = educational_qualification
            qualification.certification = certification

            fs = FileSystemStorage()

            # Process and validate CV
            if cv:
                if not validate_file_format(cv.name, ['.pdf', '.docx']):
                    messages.error(request, "Invalid CV format. Accepted formats: PDF, DOCX.")
                    return redirect("edit_staff_qualification", staff_id=staff_id)

                if cv.size > 10485760:  # 10MB in bytes
                    messages.error(request, "CV size exceeds the limit of 10MB.")
                    return redirect("edit_staff_qualification", staff_id=staff_id)

                filename = fs.save(cv.name, cv)
                qualification.cv = fs.url(filename)

            # Process and validate other certificates
            if other_certificates:
                if not validate_file_format(other_certificates.name, ['.pdf', '.docx']):
                    messages.error(request, "Invalid certificate format. Accepted formats: PDF, DOCX.")
                    return redirect("edit_staff_qualification", staff_id=staff_id)

                if other_certificates.size > 10485760:  # 10MB in bytes
                    messages.error(request, "Certificate size exceeds the limit of 10MB.")
                    return redirect("edit_staff_qualification", staff_id=staff_id)

                filename = fs.save(other_certificates.name, other_certificates)
                qualification.other_certificates = fs.url(filename)

            qualification.save()

            messages.success(request, "Staff qualification details updated successfully.")
            return redirect("edit_staff_skill", staff_id=staff_id)
        except Exception as e:
            messages.error(request, f"Error updating staff qualification details: {str(e)}")

    return render(request, "hod_template/edit_qualification.html", {"staff": staff, "staff_id": staff_id, "qualification": qualification})


def skills_form(request, staff_id):
    staff = get_object_or_404(Staffs, id=staff_id)

    if request.method == 'POST':
        # Retrieve form data
        subject_expertise = request.POST.get('subject_expertise')
        teaching_methods = request.POST.get('teaching_methods')
        professional_development = request.POST.get('professional_development')
        language_proficiency = request.POST.get('language_proficiency')
        technology_skills = request.POST.get('technology_skills')
        special_skills = request.POST.get('special_skills')
        certificate = request.FILES.get('certificate')

        try:
            # Validate the certificate format
            if certificate:
                if not certificate.name.endswith('.pdf'):
                    raise ValueError('Invalid certificate format. Only PDF files are allowed.')

                # Save the certificate file
                fs = FileSystemStorage()
                filename = fs.save(certificate.name, certificate)
                certificate_url = fs.url(filename)
            else:
                certificate_url = None

            # Save the form data to the database
            skills = Skills.objects.create(
                staff_id=staff,
                subject_expertise=subject_expertise,
                teaching_methods=teaching_methods,
                professional_development=professional_development,
                language_proficiency=language_proficiency,
                technology_skills=technology_skills,
                special_skills=special_skills,
                certificate_url=certificate_url
            )

            messages.success(request, "Skills successfully added.")
            return redirect(reverse('employment_history_form', kwargs={'staff_id': staff_id}))
        except Exception as e:
            messages.error(request, f"Error saving skills: {str(e)}")
            return render(request, 'hod_template/add_skills.html', {'staff_id': staff_id})

    return render(request, 'hod_template/add_skills.html', {'staff_id': staff_id})

def edit_staff_skill(request, staff_id):
    staff = get_object_or_404(Staffs, id=staff_id)
    try:
        skills = Skills.objects.get(staff_id=staff)
    except Skills.DoesNotExist:
        skills = None

    if request.method == 'POST':
        # Retrieve form data
        subject_expertise = request.POST.get('subject_expertise')
        teaching_methods = request.POST.get('teaching_methods')
        professional_development = request.POST.get('professional_development')
        language_proficiency = request.POST.get('language_proficiency')
        technology_skills = request.POST.get('technology_skills')
        special_skills = request.POST.get('special_skills')
        certificate = request.FILES.get('certificate')

        try:
            # Validate the certificate format and size
            if certificate:
                if not certificate.name.endswith('.pdf'):
                    raise ValueError('Invalid certificate format. Only PDF files are allowed.')

                if certificate.size > 10485760:  # 10MB in bytes
                    raise ValueError('Certificate size exceeds the limit of 10MB.')

                # Save the certificate file
                fs = FileSystemStorage()
                filename = fs.save(certificate.name, certificate)
                certificate_url = fs.url(filename)
            else:
                certificate_url = None

            # Save the form data to the database
            if skills:
                skills.subject_expertise = subject_expertise
                skills.teaching_methods = teaching_methods
                skills.professional_development = professional_development
                skills.language_proficiency = language_proficiency
                skills.technology_skills = technology_skills
                skills.special_skills = special_skills
                skills.certificate_url = certificate_url
                skills.save()
            else:
                Skills.objects.create(
                    staff_id=staff,
                    subject_expertise=subject_expertise,
                    teaching_methods=teaching_methods,
                    professional_development=professional_development,
                    language_proficiency=language_proficiency,
                    technology_skills=technology_skills,
                    special_skills=special_skills,
                    certificate_url=certificate_url
                )

            messages.success(request, "Skills successfully updated.")
            return redirect(reverse('edit_staff_employment_history', kwargs={'staff_id': staff_id}))
        except Exception as e:
            messages.error(request, f"Error saving skills: {str(e)}")
            return render(request, 'hod_template/edit_skills.html', {'staff': staff, 'skills': skills})

    return render(request, 'hod_template/edit_skills.html', {'staff': staff, 'skills': skills})

def employment_history_form(request, staff_id):
    if request.method == 'POST':
        # Retrieve form data
        employment_history = request.POST.get('employment_history')
        company_name = request.POST.get('company_name')
        company_address = request.POST.get('company_address')
        position = request.POST.get('position')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        # Convert date strings to datetime objects
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        except ValueError as e:
            messages.error(request, f"Invalid date format: {str(e)}. Please use the format 'YYYY-MM-DD'.")
            return render(request, 'hod_template/add_employment_history.html', {'staff_id': staff_id})

        try:
            # Fetch the Staffs instance
            staff = get_object_or_404(Staffs, id=staff_id)

            # Save form data to the database
            employment_history_obj = EmploymentHistory.objects.create(
                staff_id=staff,
                employment_history=employment_history,
                company_name=company_name,
                company_address=company_address,
                position=position,
                start_date=start_date,
                end_date=end_date
            )

            messages.success(request, "Employment history successfully added.")
            return redirect(reverse('references_form', kwargs={'staff_id': staff_id}))
        except Exception as e:
            messages.error(request, f"Error saving employment history: {str(e)}")
            return render(request, 'hod_template/add_employment_history.html', {'staff_id': staff_id})

    return render(request, 'hod_template/add_employment_history.html', {'staff_id': staff_id})


def edit_staff_employment_history(request, staff_id):
    staff = get_object_or_404(Staffs, id=staff_id)
    try:
        employment_history_obj = EmploymentHistory.objects.get(staff_id=staff)
    except EmploymentHistory.DoesNotExist:
        employment_history_obj = None

    if request.method == 'POST':
        # Retrieve form data
        employment_history = request.POST.get('employment_history')
        company_name = request.POST.get('company_name')
        company_address = request.POST.get('company_address')
        position = request.POST.get('position')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        # Convert date strings to datetime objects
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        except ValueError as e:
            messages.error(request, f"Invalid date format: {str(e)}. Please use the format 'YYYY-MM-DD'.")
            return render(request, 'hod_template/edit_employment_history.html', {'staff': staff, 'employment_history_obj': employment_history_obj})

        try:
            # Save form data to the database
            if employment_history_obj:
                employment_history_obj.employment_history = employment_history
                employment_history_obj.company_name = company_name
                employment_history_obj.company_address = company_address
                employment_history_obj.position = position
                employment_history_obj.start_date = start_date
                employment_history_obj.end_date = end_date
                employment_history_obj.save()
            else:
                EmploymentHistory.objects.create(
                    staff_id=staff,
                    employment_history=employment_history,
                    company_name=company_name,
                    company_address=company_address,
                    position=position,
                    start_date=start_date,
                    end_date=end_date
                )

            messages.success(request, "Employment history successfully updated.")
            return redirect(reverse('edit_staff_reference', kwargs={'staff_id': staff_id}))
        except Exception as e:
            messages.error(request, f"Error saving employment history: {str(e)}")
            return render(request, 'hod_template/edit_employment_history.html', {'staff': staff, 'employment_history_obj': employment_history_obj})

    return render(request, 'hod_template/edit_employment_history.html', {'staff': staff, 'employment_history_obj': employment_history_obj})



def references_form(request, staff_id):
    if request.method == 'POST':
        # Retrieve form data
        staff_position = request.POST.get('staff_position')
        company_name = request.POST.get('company_name')
        company_address = request.POST.get('company_address')
        company_contact_person = request.POST.get('company_contact_person')
        company_contact_email = request.POST.get('company_contact_email')
        company_contact_phone = request.POST.get('company_contact_phone')

        try:
            # Save form data to the database
            references = References.objects.create(
                staff_id=staff_id,
                staff_position=staff_position,
                company_name=company_name,
                company_address=company_address,
                company_contact_person=company_contact_person,
                company_contact_email=company_contact_email,
                company_contact_phone=company_contact_phone
            )

            messages.success(request, "References successfully added.")
        except Exception as e:
            messages.error(request, f"Error saving references: {str(e)}")

    return render(request, 'hod_template/add_reference.html',{'staff_id': staff_id})


def edit_staff_reference(request, staff_id):
    staff = get_object_or_404(Staffs, id=staff_id)
    try:
        reference = References.objects.get(staff_id=staff)
    except References.DoesNotExist:
        reference = None

    if request.method == 'POST':
        # Retrieve form data
        staff_position = request.POST.get('staff_position')
        company_name = request.POST.get('company_name')
        company_address = request.POST.get('company_address')
        company_contact_person = request.POST.get('company_contact_person')
        company_contact_email = request.POST.get('company_contact_email')
        company_contact_phone = request.POST.get('company_contact_phone')

        try:
            # Save form data to the database
            if reference:
                reference.staff_position = staff_position
                reference.company_name = company_name
                reference.company_address = company_address
                reference.company_contact_person = company_contact_person
                reference.company_contact_email = company_contact_email
                reference.company_contact_phone = company_contact_phone
                reference.save()
            else:
                References.objects.create(
                    staff_id=staff,
                    staff_position=staff_position,
                    company_name=company_name,
                    company_address=company_address,
                    company_contact_person=company_contact_person,
                    company_contact_email=company_contact_email,
                    company_contact_phone=company_contact_phone
                )

            messages.success(request, "References successfully updated.")
            return redirect(reverse('other_editing_form', kwargs={'staff_id': staff_id}))
        except Exception as e:
            messages.error(request, f"Error saving references: {str(e)}")
            return render(request, 'hod_template/edit_reference.html', {'staff': staff, 'reference': reference})

    return render(request, 'hod_template/edit_reference.html', {'staff': staff, 'reference': reference})


 
def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    
    else:        
        form = AddSubjectForm(request.POST)
        if form.is_valid():
            subject_name = form.cleaned_data["subject_name"]
            school_segment = form.cleaned_data["school_segment"]
            
            try:
                subject = Subject(subject_name=subject_name, school_segment=school_segment)
                subject.save()
                
                messages.success(request, "Subject successfully added")
                return HttpResponseRedirect(reverse("addsubject"))  
            
            except Exception as e:
                messages.error(request, f"Failed to add subject. Error: {str(e)}")
                return HttpResponseRedirect(reverse("addsubject"))
            
        else:
            messages.error(request, "Invalid form submission. Please check the form fields.")
            return HttpResponseRedirect(reverse("addsubject"))
            

def add_subject(request):
    forms = AddSubjectForm()
    return render(request,"hod_template/add_subject.html",{"forms":forms})    

def add_parents(request):
    students = Students.objects.all()
    return render(request, "hod_template/parent_form.html", {'students': students})   


def edit_parents(request, parent_id):
    try:
        request.session['parent_id'] = parent_id       
        parent = Parent.objects.get(id=parent_id)
        students = Students.objects.all()

        # Get the IDs of currently associated students, if any
        associated_student_ids = parent.student.all().values_list('id', flat=True)

        return render(request, "hod_template/edit_parent.html", {
            "id": parent_id,
            "username": parent.name,
            "parents": parent,
            "students": students,
            "associated_student_ids": associated_student_ids,  # Pass the associated student IDs to the template
        })
    except Parent.DoesNotExist:
        messages.error(request, "Parent not found.")
        return redirect("manage_parent")





def update_parent(request, parent_id):
    try:
        parent = get_object_or_404(Parent, id=parent_id)

        if request.method == 'POST':
            # Retrieve form field values from the request
            
            phone = request.POST.get('phone')
            occupation = request.POST.get('occupation')
            address = request.POST.get('sheia')
            street_address = request.POST.get('street')
            house_number = request.POST.get('house')
            national_id = request.POST.get('nationalid')
            status = request.POST.get('status')
            gender = request.POST.get('gender')
            parent_type = request.POST.get('type')

            # Perform form field validation
            if not phone:
                messages.error(request, "phone field is required.")         
            elif not occupation:
                messages.error(request, "Occupation field is required.")
            elif not address:
                messages.error(request, "Sheia Address field is required.")
            elif not street_address:
                messages.error(request, "Street Address field is required.")
            elif not house_number:
                messages.error(request, "House Number field is required.")
            elif not national_id:
                messages.error(request, "National ID field is required.")
            elif not status:
                messages.error(request, "Status field is required.")
            elif not gender:
                messages.error(request, "Gender field is required.")
            elif not parent_type:
                messages.error(request, "Relation field is required.")
            else:
                # Update the parent record
                
                parent.phone = phone
                parent.occupation = occupation
                parent.address = address
                parent.street_address = street_address
                parent.house_number = house_number
                parent.national_id = national_id
                parent.status = status
                parent.gender = gender
                parent.parent_type = parent_type

                # Get the selected students (assuming 'students' is a list of student IDs from the form)
                selected_student_ids = request.POST.getlist('student_id')

                # Clear existing relationships and add the selected students
                parent.student.clear()  # Clear all existing relationships
                for student_id in selected_student_ids:
                    student = get_object_or_404(Students, id=student_id)
                    parent.student.add(student)  # Add selected students to the relationship

                parent.save()

                messages.success(request, "Parent and associated students have been successfully updated.")
                return redirect("edit_parents", parent_id=parent_id)

        context = {
            'parent': parent,
            'students': Students.objects.all(),
            'selected_student_ids': [student.id for student in parent.student.all()] if hasattr(parent, 'student') else []
        }
        return render(request, 'admin_template/edit_parent.html', context)

    except Parent.DoesNotExist:
        messages.error(request, "Parent not found.")
        return redirect("edit_parents", parent_id=parent_id)
    
    
def save_parent(request):
    if request.method == "POST":
        try:
            student_id = request.POST.get('student_id')
            phone = request.POST.get('phone')
            occupation = request.POST.get('occupation')
            sheia = request.POST.get('sheia')
            street = request.POST.get('street')
            house = request.POST.get('house')
            national_id = request.POST.get('nationalid')
            status = request.POST.get('status')
            gender = request.POST.get('gender')
            parent_type = request.POST.get('type')

            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not all([student_id, phone, username, first_name, last_name, email, password]):
                messages.error(request, "Please provide all required fields")
                return redirect("add_parents")

            student = Students.objects.get(id=student_id)

            # Create or update the CustomUser
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'user_type': 3,
                }
            )

            if not created:
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.user_type = 3
                user.password = password
                user.save()

            # Create or update the Parent
            parent, created = Parent.objects.get_or_create(
                admin=user,  # Set the admin field to the user
                defaults={
                    'phone': phone,
                    'occupation': occupation,
                    'address': sheia,
                    'street_address': street,
                    'house_number': house,
                    'national_id': national_id,
                    'status': status,
                    'gender': gender,
                    'parent_type': parent_type,
                }
            )

            if not created:
                parent.phone = phone
                parent.occupation = occupation
                parent.address = sheia
                parent.street_address = street
                parent.house_number = house
                parent.national_id = national_id
                parent.status = status
                parent.gender = gender
                parent.parent_type = parent_type
                parent.save()

            # Associate the parent with the student
            student.parent.add(parent)

            messages.success(request, "Parent information saved successfully")
            return redirect("add_parents")

        except Exception as e:
            messages.error(request, "Error saving parent information: " + str(e))

    return redirect("add_parents")
          

def add_student_save(request):
    if request.method == "POST":
        try:
            # Extract form data
            first_name = request.POST.get('first_name')
            surname = request.POST.get('surname')
            service_type = request.POST.get('service_type')
            last_name = request.POST.get('last_name')
            date_of_birth_str = request.POST.get('date_of_birth')
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            gender = request.POST.get('gender')
            phone_number = request.POST.get('phone_number')
            school_segment = request.POST.get('school_segment')
            current_class = request.POST.get('current_class')
            birth_certificate_id = request.POST.get('birth_certificate_id')
            allergies = request.POST.get('allergies')
            current_year = request.POST.get('current_year')
            is_finished = request.POST.get('is_finished')
            sheia_address = request.POST.get('sheia_address')
            street_address = request.POST.get('street_address')
            house_number = request.POST.get('house_number')
            health_status = request.POST.get('health_status')
            physical_disability = request.POST.get('physical_disability')
            subjects_ids = request.POST.getlist('subjects')
            session_year_id = request.POST.get('session_year')

            # Perform validation
            if not first_name or not last_name or not date_of_birth:
                messages.error(request, "Please provide all required fields")
                return redirect("add_student")

            # Save the form data to the database
            try:
                # Save the student's profile picture
                student_photo_url = None
                student_photo = request.FILES.get('student_photo')
                if student_photo:
                    if student_photo.size > 5242880:  # 10 MB (size in bytes)
                        raise ValidationError("Profile picture size should be less than 5 MB.")
                    if not student_photo.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                        raise ValidationError("Only JPG, JPEG, and PNG image files are allowed for profile pictures.")
                    fs = FileSystemStorage()
                    filename = fs.save(student_photo.name, student_photo)
                    student_photo_url = fs.url(filename)

                # Save the birth certificate photo
                birth_certificate_photo_url = None
                birth_certificate_photo = request.FILES.get('birth_certificate_photo')
                if birth_certificate_photo:
                    if birth_certificate_photo.size > 5242880:  # 10 MB (size in bytes)
                        raise ValidationError("Birth certificate photo size should be less than 5 MB.")
                    if not birth_certificate_photo.name.lower().endswith(('.pdf')):
                        raise ValidationError("Only PDF image files are allowed for birth certificate photos.")
                    fs = FileSystemStorage()
                    filename = fs.save(birth_certificate_photo.name, birth_certificate_photo)
                    birth_certificate_photo_url = fs.url(filename)

                # Retrieve or create the CustomUser instance based on the username
                username = first_name.lower() + last_name.lower()
                default_email = first_name.lower() + "@gmail.com"
                password = '1234'  # Set a default password
                
                user= CustomUser.objects.create_user(username=username,password=password,email=default_email,first_name=first_name,last_name=last_name,user_type=3)

                # Create a new instance of the Student model
               
                user.students.surname = surname
                user.students.service_type = service_type
                user.students.last_name = last_name
                user.students.date_of_birth = date_of_birth
                user.students.gender = gender
                user.students.phone_number = phone_number
                user.students.school_segment = school_segment
                user.students.current_class = current_class
                user.students.birth_certificate_id = birth_certificate_id
                user.students.allergies = allergies
                user.students.current_year = current_year
                user.students.is_finished = is_finished
                user.students.address = sheia_address
                user.students.street_address = street_address
                user.students.house_number = house_number
                user.students.health_status = health_status
                user.students.physical_disability = physical_disability
                user.students.profile_pic = student_photo_url
                user.students.birth_certificate_photo = birth_certificate_photo_url

                # Save the student record
                user.save()

                # Add the selected subjects to the student's subjects field
                for subject_id in subjects_ids:
                    subject = Subject.objects.get(pk=subject_id)
                    user.students.subjects.add(subject)

                # Add the selected session year to the student's session_id field
                session_year = SessionYearModel.objects.get(pk=session_year_id)
                user.students.session_id = session_year

                # Save the student record again to include the subjects and session year
                user.students.save()

                messages.success(request, "Successfully added student")
                return redirect("add_student")
            except ValidationError as ve:
                messages.error(request, ve.message)
            except Exception as e:
                messages.error(request, f"Error saving student record: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect("add_student")

        

def add_student(request):
    all_subjects = Subject.objects.all()
    all_session_years = SessionYearModel.objects.all()

    context = {
        "all_subjects": all_subjects,
        "all_session_years": all_session_years,
    }

    return render(request, "hod_template/add_student.html", context)

def single_student_detail(request, student_id):
    students = get_object_or_404(Students, id=student_id)
    parents = Parent.objects.filter(student=students)
    selected_subjects = students.subjects.all()
    father = None
    mother = None
    male_guardian = None
    female_guardian = None
    male_sponsor = None
    female_sponsor = None

    for parent in parents:
        if parent.parent_type == 'parent':
            if parent.gender == 'male':
                father = parent
            elif parent.gender == 'female':
                mother = parent
        elif parent.parent_type == 'guardian':
            if parent.gender == 'male':
                male_guardian = parent
            elif parent.gender == 'female':
                female_guardian = parent
        elif parent.parent_type == 'sponsor':
            if parent.gender == 'male':
                male_sponsor = parent
            elif parent.gender == 'female':
                female_sponsor = parent

    context = {
        'students': students,
        'father': father,
        'mother': mother,
        'male_guardian': male_guardian,
        'female_guardian': female_guardian,
        'male_sponsor': male_sponsor,
        'female_sponsor': female_sponsor,
        'selected_subjects':selected_subjects,
    }

    return render(request, "hod_template/student_details.html", context)



def single_staff_detail(request, staff_id):
    staff = get_object_or_404(Staffs, id=staff_id)
    # Fetch additional staff-related data    
    skills = Skills.objects.filter(staff_id=staff_id).first()
    employment_history = EmploymentHistory.objects.filter(staff_id=staff_id)  # Use ForeignKey's filter here
    qualifications = Qualifications.objects.filter(staff_id=staff_id)
    references = References.objects.filter(staff_id=staff_id)

    context = {
        'staff': staff,
        'skills': skills,
        'employment_history': employment_history,
        'qualifications': qualifications,
        'references': references,
    }

    return render(request, "hod_template/staff_details.html", context)

def single_parent_detail(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    students = parent.student.all()  # Get all students associated with the parent
    
    context = {
        'parent': parent,
        'students': students,
    }
    
    return render(request, "hod_template/parent_details.html", context)


  
def manage_student(request):
    per_page = request.GET.get('per_page', 3)
    current_class = request.GET.get('current_class')  # Get the selected class from the request
    students = Students.objects.all()
    
    if current_class:  # Filter students by class if it is selected
        students = students.filter(current_class=current_class)
    students = students.order_by('id')
    paginator = Paginator(students, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "hod_template/manage_student.html", {"students": students, "page_obj": page_obj})


def manage_parent(request):
    per_page = request.GET.get('per_page', 3)  # Get the number of items to display per page from the request
    parents = Parent.objects.all()
    parents = parents.order_by('id')
    paginator = Paginator(parents, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "hod_template/manage_parent.html", {"students": parents, "page_obj": page_obj})
 
def student_list(request):
    search_query = request.GET.get('search', '')
    students = Students.objects.all()
    
    if search_query:
        students = students.filter(registration_number__icontains=search_query)
    
    paginator = Paginator(students, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "paginator.html", {"students": students, "page_obj": page_obj})  
  

  
def manage_staff(request):       
    per_page = request.GET.get('per_page', 3)  # Get the number of items to display per page from the request
    staffs=Staffs.objects.all()
    staffs = staffs.order_by('id') 
    paginator = Paginator(staffs, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"hod_template/manage_staff.html",{"staffs":staffs,"page_obj":page_obj})  


def manage_subject(request):
    per_page = request.GET.get('per_page', 3)
    search_query = request.GET.get('search', '')

    subjects = Subject.objects.filter(
        Q(subject_name__icontains=search_query) | Q(school_segment__icontains=search_query)
    )
    subjects = subjects.order_by('id')
    paginator = Paginator(subjects, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "hod_template/manage_subject.html", {
        "subjects": subjects,
        "page_obj": page_obj,
        "search_query": search_query,
    })
    

def edit_subject(request,subject_id):
    # If you want to populate the form fields with an existing Subject object
    subject = Subject.objects.get(pk=subject_id)  # Replace subject_id with the ID of the Subject you want to edit
    return render(request, 'hod_template/edit_subject.html', {'subject': subject}) 
   

def create_or_edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)

    if request.method == 'POST':
        school_segment = request.POST.get('school_segment')
        subject_name = request.POST.get('subject_name')

        # Perform basic validation
        if not school_segment or not subject_name:
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('edit_subject', subject_id=subject_id)

        # Update the Subject object with the form data
        subject.school_segment = school_segment
        subject.subject_name = subject_name

        # Save the Subject object to the database
        subject.save()

        messages.success(request, 'Subject details successfully updated.')
        return redirect('edit_subject', subject_id=subject_id)  # Provide the subject_id as an argument

    return render(request, 'edit_subject.html', {'subject': subject})

def subject_details(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    return render(request, 'hod_template/subject_detail.html', {'subject': subject})
    
def edit_staff(request, staff_id):
    # Check if the staff with the given ID exists, or return a 404 page
    staff = get_object_or_404(Staffs, id=staff_id)

    # Get all available subjects (Modify this line according to your model and queryset)
    all_subjects = Subject.objects.all()  # Replace 'Subject' with your actual Subject model

    # If staff exists, proceed with the rest of the view
    request.session['staff_id'] = staff_id
    return render(request, "hod_template/edit_staff.html", {"id": staff_id, "username": staff.admin.username, "staff": staff, "all_subjects": all_subjects})   


def edit_staff_save(request):
    if request.method == "POST":
        try:
            # Retrieve the staff ID from the session
            staff_id = request.session.get('staff_id')
            if staff_id is None:
                messages.error(request, "Staff ID not found")
                return redirect("manage_staff")

            # Retrieve the staff instance from the database
            try:
                staff = Staffs.objects.get(id=staff_id)
            except ObjectDoesNotExist:
                messages.error(request, "Staff not found")
                return redirect("manage_staff")

            # Extract the form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            surname = request.POST.get('surname')
            email = request.POST.get('email')
            address = request.POST.get('address')
            street_address = request.POST.get('street_address')
            house_number = request.POST.get('house_number')
            date_of_birth = request.POST.get('date_of_birth')
            contact_number = request.POST.get('contact_number')
            gender = request.POST.get('gender')
            background_check = request.POST.get('background_check')
            availability = request.POST.get('availability')
            preferred_grade_level = request.POST.get('preferred_grade_level')
            salary_expectations = request.POST.get('salary_expectations')
            personal_statement = request.POST.get('personal_statement')
            national_identity_number = request.POST.get('national_identity_number')
            subjects = request.POST.getlist('subjects')

            # Save the staff details
            staff.admin.first_name = first_name
            staff.admin.last_name = last_name
            staff.admin.email = email
            staff.surname = surname
            staff.address = address
            staff.street_address = street_address
            staff.house_number = house_number
            staff.date_of_birth = date_of_birth
            staff.contact_number = contact_number
            staff.gender = gender
            staff.background_check = background_check
            staff.availability = availability
            staff.preferred_grade_level = preferred_grade_level
            staff.salary_expectations = salary_expectations
            staff.personal_statement = personal_statement
            staff.national_identity_number = national_identity_number

            # Save the staff subjects
            staff.subjects.set(subjects)

            # Process and validate uploaded files
            fs = FileSystemStorage()

            # Process the profile picture
            profile_picture = request.FILES.get('staff_photo')
            if profile_picture:
                if not validate_file_format(profile_picture.name, ['.jpg', '.jpeg', '.png']):
                    messages.error(request, "Invalid profile picture format. Accepted formats: JPG, JPEG, PNG.")
                    return redirect("edit_staff",staff_id=staff_id)

                if profile_picture.size > 5242880:  # 5MB in bytes
                    messages.error(request, "Profile picture size exceeds the limit of 5MB.")
                    return redirect("edit_staff",staff_id=staff_id)

                # Save the profile picture
                filename = fs.save(profile_picture.name, profile_picture)
                staff.profile_pic = fs.url(filename)

            # Process and validate uploaded files for national ID photo and birth certificate photo
            national_id_photo = request.FILES.get('national_id_photo')
            if national_id_photo:
                if not validate_file_format(national_id_photo.name, ['.pdf']):
                    messages.error(request, "Invalid national ID photo format. Accepted format: PDF.")
                    return redirect("edit_staff",staff_id=staff_id)

                if national_id_photo.size > 5242880:  # 5MB in bytes
                    messages.error(request, "National ID photo size exceeds the limit of 5MB.")
                    return redirect("edit_staff",staff_id=staff_id)

                # Save the national ID photo
                filename = fs.save(national_id_photo.name, national_id_photo)
                staff.national_id_photo = fs.url(filename)

            birth_certificate_photo = request.FILES.get('birth_certificate_photo')
            if birth_certificate_photo:
                if not validate_file_format(birth_certificate_photo.name, ['.pdf']):
                    messages.error(request, "Invalid birth certificate format. Accepted format: PDF.")
                    return redirect("edit_staff",staff_id=staff_id)

                if birth_certificate_photo.size > 5242880:  # 5MB in bytes
                    messages.error(request, "Birth certificate size exceeds the limit of 5MB.")
                    return redirect("edit_staff",staff_id=staff_id)

                # Save the birth certificate photo
                filename = fs.save(birth_certificate_photo.name, birth_certificate_photo)
                staff.birth_certificate_photo = fs.url(filename)

            # Save the staff instance to the database
            staff.save()

            # Assuming the URL name for the next editing form is "qualification_form"
            messages.success(request, "Staff details updated successfully.")
            return redirect("qualification_form", staff_id=staff_id)
        except Exception as e:
            messages.error(request, f"Error updating staff details: {str(e)}")

    return redirect("edit_staff",staff_id=staff_id)

def validate_file_format(filename, allowed_formats):
    return any(filename.lower().endswith(format) for format in allowed_formats)



def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")

    print("Session data:", request.session.items())
    student_id = request.session.get("student_id")
    print("Student ID:", student_id)
    if not student_id:
        return HttpResponseRedirect(reverse("manage_student"))

    try:
        user = CustomUser.objects.get(id=student_id)

        # Get the form data
        first_name = request.POST.get('first_name')
        surname = request.POST.get('surname')
        service_type = request.POST.get('service_type')
        last_name = request.POST.get('last_name')
        date_of_birth_str = request.POST.get('date_of_birth')
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        school_segment = request.POST.get('school_segment')
        current_class = request.POST.get('current_class')
        birth_certificate_id = request.POST.get('birth_certificate_id')
        allergies = request.POST.get('allergies')
        current_year = request.POST.get('current_year')
        is_finished = request.POST.get('is_finished')
        sheia_address = request.POST.get('sheia_address')
        street_address = request.POST.get('street_address')
        house_number = request.POST.get('house_number')
        health_status = request.POST.get('health_status')
        physical_disability = request.POST.get('physical_disability')

        # Get the selected subjects and session year
        subjects_ids = request.POST.getlist('subjects')
        session_year_id = request.POST.get('session_year')

        # Perform validation
        if not all([first_name, last_name, date_of_birth]):
            messages.error(request, "Please provide all required fields")
            return redirect("add_student")

        # Update user information
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Update student information
        student = Students.objects.get(admin=user)
        student.surname = surname
        student.service_type = service_type
        student.date_of_birth = date_of_birth
        student.gender = gender
        student.phone_number = phone_number
        student.school_segment = school_segment
        student.current_class = current_class
        student.birth_certificate_id = birth_certificate_id
        student.allergies = allergies
        student.current_year = current_year
        student.is_finished = is_finished
        student.address = sheia_address
        student.street_address = street_address
        student.house_number = house_number
        student.health_status = health_status
        student.physical_disability = physical_disability

        # Validate and save the profile picture
        student_photo = request.FILES.get('student_photo')
        if student_photo:
            if student_photo.size > 5242880:  # 5 MB limit
                raise ValidationError("Profile picture size should not exceed 5 MB.")
            if not student_photo.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError("Invalid file format. Only PNG, JPG, and JPEG files are allowed.")
            fs = FileSystemStorage()
            filename = fs.save(student_photo.name, student_photo)
            student.profile_pic = fs.url(filename)

        # Validate and save the birth certificate photo
        birth_certificate_photo = request.FILES.get('birth_certificate_photo')
        if birth_certificate_photo:
            if birth_certificate_photo.size > 5242880:  # 5 MB limit
                raise ValidationError("Birth certificate photo size should not exceed 5 MB.")
            if not birth_certificate_photo.name.lower().endswith('.pdf'):
                raise ValidationError("Invalid file format. Only PDF files are allowed.")
            fs = FileSystemStorage()
            filename = fs.save(birth_certificate_photo.name, birth_certificate_photo)
            student.birth_certificate_photo = fs.url(filename)

        student.save()

        # Clear existing subjects and add the selected subjects to the student's subjects field
        student.subjects.clear()
        for subject_id in subjects_ids:
            subject = Subject.objects.get(pk=subject_id)
            student.subjects.add(subject)

        # Add the selected session year to the student's session_year field
        session_year = SessionYearModel.objects.get(pk=session_year_id)
        student.session_year = session_year

        student.save()

        # del request.session['student_id']
        messages.success(request, "Successfully edited student")
        return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))

    except CustomUser.DoesNotExist:
        messages.error(request, "User does not exist")
        return HttpResponseRedirect(reverse("edit_student"))

    except Students.DoesNotExist:
        messages.error(request, "Student does not exist")
        return HttpResponseRedirect(reverse("edit_student"))

    except IntegrityError:
        messages.error(request, "Failed to edit student due to a database error")
        return HttpResponseRedirect(reverse("edit_student"))




   
def edit_student(request, student_id):
    try:
        # Get the student record based on the student_id
        student = Students.objects.get(admin__id=student_id)
        request.session['student_id'] = student_id
        # Fetch all subjects and session years
        all_subjects = Subject.objects.all()
        all_session_years = SessionYearModel.objects.all()

        # Get the currently selected subjects and session year for the student
        selected_subjects = student.subjects.all()
        selected_session_year = student.session_year

        return render(request, "hod_template/edit_student.html", {
            "student_id": student_id,
            "username": student.admin.username,
            "students": student,
            "all_subjects": all_subjects,
            "all_session_years": all_session_years,
            "selected_subjects": selected_subjects,
            "selected_session_year": selected_session_year,
        })

    except Students.DoesNotExist:
        messages.error(request, "Student does not exist")
        return HttpResponseRedirect(reverse("manage_studen"))
    
      



    




def add_session(request):    
    return render(request,"hod_template/add_session.html")

def edit_session(request, session_id):
    session = get_object_or_404(SessionYearModel, id=session_id)
    return render(request, "hod_template/edit_session.html", {"session": session})


def edit_session_save(request, session_id):
    session = get_object_or_404(SessionYearModel, id=session_id)

    if request.method == 'POST':
        # Get the data from the form submission
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        # Update the session with the new data
        session.session_start_year = session_start_year
        session.session_end_year = session_end_year
        session.save()

        # Display a success message
        messages.success(request, 'Session updated successfully.')

        # Redirect to the list of sessions after successful editing
        return redirect('manage_session')
    else:
        # Display an error message for invalid form submission
        messages.error(request, 'Failed to update session. Please check the form data.')

    return render(request, 'hod_template/edit_session.html', {'session': session})


def manage_session(request):
    sessions = SessionYearModel.objects.all()
    return render(request, 'hod_template/manage_session.html', {'sessions': sessions})

def delete_session(request, session_id):
    try:
        session = SessionYearModel.objects.get(id=session_id)
        session.delete()
        messages.success(request, "Session deleted successfully.")
    except SessionYearModel.DoesNotExist:
        messages.error(request, "Session not found.")
    return redirect('manage_session')


def add_session_save(request):
    if request.method == 'POST':
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        if session_start_year and session_end_year:
            SessionYearModel.objects.create(
                session_start_year=session_start_year,
                session_end_year=session_end_year
            )
            # Display a success message after successfully creating the session
            messages.success(request, 'Session added successfully.')
            return redirect('add_session')  # Replace 'list_sessions' with the URL name of a page that displays all sessions.
        else:
            # Display an error message if any of the fields are missing
            messages.error(request, 'Failed to add session. Please fill in all the fields.')
    
    return render(request, 'hod_template/ad_session.html')

        
            
@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_object = CustomUser.objects.filter(email=email).exists()
    if user_object:
        return HttpResponse(True)
    
    else:
        return HttpResponse(False)
    
    
@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_object = CustomUser.objects.filter(username=username).exists()
    if user_object:
        return HttpResponse(True)
    
    else:
        return HttpResponse(False)


def  student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    return render(request,"hod_template/student_feedback_message.html",{"feedbacks":feedbacks})

def staff_feedback_message(request):
    feedbacks = FeedBackStaff.objects.all()
    return render(request,"hod_template/staff_feedback_message.html",{"feedbacks":feedbacks})


@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:    
      feedback = FeedBackStudent.objects.get(id=feedback_id)
      feedback.feedback_reply = feedback_message
      feedback.save() 
      return HttpResponse(True)
    except:
       return HttpResponse(False)  
   
            
@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:    
      feedback = FeedBackStaff.objects.get(id=feedback_id)
      feedback.feedback_reply = feedback_message
      feedback.save() 
      return HttpResponse(True)
    except:
       return HttpResponse(False)           
   
def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    return render(request,"hod_template/student_leave_view.html",{"leaves":leaves})



def student_approve_leave(request,leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def student_disapprove_leave(request,leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_leave_view(request):
    leaves = LeaveReportStaffs.objects.all()
    return render(request,"hod_template/staff_leave_view.html",{"leaves":leaves})

def staff_approve_leave(request,leave_id):
    leave = LeaveReportStaffs.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def staff_disapprove_leave(request,leave_id):
    leave = LeaveReportStaffs.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def admin_view_attendance(request):
    subjects = Subject.objects.all()   
    session_years = SessionYearModel.objects.all()
    return render(request,"hod_template/admin_view_attendance.html",{"subjects":subjects,"session_years":session_years})

@csrf_exempt
def admin_get_student_attendance(request):
    attendance_date=request.POST.get("attendance_date_id")     
    attendance_date_id=Attendance.objects.get(id=attendance_date)
    attendance_data =AttendanceReport.objects.filter(attendance_id=attendance_date_id)   
    
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def admin_get_attendance_date(request):
     subject = request.POST.get("subject_id")
     session_year_id = request.POST.get("session_year_id")
     print(subject)
     print(session_year_id)
     subject_obj = Subject.objects.get(id=subject)
     session_year_obj = SessionYearModel.objects.get(id=session_year_id)
     attendance = Attendance.objects.filter(subject_id=subject_obj,session_id=session_year_obj)
     attendance_obj = []
     
     for attendance_single in attendance:
         data = {
             "id":attendance_single.id,
             "attendance_date":str(attendance_single.attendance_date),
             "session_year_id":attendance_single.session_id.id
             }
         attendance_obj.append(data)
         
     return JsonResponse(json.dumps(attendance_obj),content_type="application/json",safe=False) 
 
 
def admin_save_updateattendance(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")     
    attendance=Attendance.objects.get(id=attendance_date)     
    json_sstudent=json.loads(student_ids)



    try:
        for stud in json_sstudent:
             student=Students.objects.get(admin_id=stud['id'])
             attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
             attendance_report.status =stud["status"]
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")
    
    

def  admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})  

def edit_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    
    else:
       first_name = request.POST.get("first_name")
       last_name = request.POST.get("last_name")
       password = request.POST.get("password")
       try:           
          customuser = CustomUser.objects.get(id=request.user.id)
          customuser.first_name = first_name
          customuser.last_name = last_name
          if password!= "" and password!=None:
              customuser.set_password(password)     
                         
          customuser.save()
          messages.success(request,"profile is successfully edited")
          return HttpResponseRedirect(reverse("admin_profile"))
      
       except:
            messages.error(request,"editing  of profile  failed")
            return HttpResponseRedirect(reverse("admin_profile"))
        
    
def exam_type_form(request, exam_type_id=None):
    if request.method == 'POST':
        try:
            # Get the data from the POST request
            name = request.POST.get('name')
            description = request.POST.get('description')

            # Create or update the ExamType instance
            if exam_type_id:
                # It's an update operation
                exam_type = ExamType.objects.get(pk=exam_type_id)
                exam_type.name = name
                exam_type.description = description
                exam_type.save()
                messages.success(request, 'Exam type updated successfully.')
            else:
                # It's a create operation
                exam_type = ExamType.objects.create(name=name, description=description)
                messages.success(request, 'Exam type created successfully.')

            return redirect('exam_type_list')  # Redirect to a list view or another appropriate URL.
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    else:
        # It's a GET request, render the form
        if exam_type_id:
            # It's an edit operation, retrieve the exam type
            exam_type = ExamType.objects.get(pk=exam_type_id)
        else:
            # It's a create operation
            exam_type = None

    return render(request, 'hod_template/add_exam_type.html', {'exam_type': exam_type})

def exam_type_list(request):
    exam_types = ExamType.objects.all()
    return render(request, 'hod_template/manage_exam_type.html', {'exam_types': exam_types})


       

def student_results(request, exam_type_id,current_class):
    # Retrieve the list of students
    
    students = Students.objects.filter(current_class=current_class)  # Replace 'Students' with your actual student model

    # Create a list to store student information
    student_info = []

    # Define the exam type for which you want to calculate positions
    exam_type = get_object_or_404(ExamType, id=exam_type_id)  # Adjust this based on your actual ExamType model

    for student in students:
        # Retrieve the StudentExamInfo for the specified student, exam type, and current class
        exam_info = StudentExamInfo.objects.filter(
            student=student,
            exam_type=exam_type,
            current_class=current_class
        ).first()

        # Retrieve the StudentPositionInfo for the specified student, exam type, and current class
        position_info = StudentPositionInfo.objects.filter(
            student=student,
            exam_type=exam_type,
            current_class=current_class
        ).first()

        if exam_info:
            division = exam_info.division
            total_grade_points = exam_info.total_grade_points
        else:
            division = "Division Not Available"
            total_grade_points = "Total Grade Points Not Available"

        if position_info:
            position = position_info.position
        else:
            position = "Position Not Available"

        # Create a dictionary for each student's information
        student_data = {
            'student': student,
            'division': division,
            'position': position,
            'total_grade_points': total_grade_points,
        }

        student_info.append(student_data)

    context = {
        'student_info': student_info,
        'exam_type': exam_type,
        'current_class': current_class,
    }

    return render(request, 'hod_template/student_results.html', context)



def subject_wise_result(request, student_id,exam_type_id):
    # Get the student based on the provided student_id
    student = Students.objects.get(id=student_id)  # Replace 'Students' with your actual student model

    # Query the results for the specific student
    exam_type = get_object_or_404(ExamType, id=exam_type_id)
    results = Result.objects.filter(student=student, exam_type_id=exam_type_id)

    context = {
        'student': student,
        'results': results,
        'exam_type': exam_type,
    }

    return render(request, 'hod_template/subject_wise_results.html', context) 


def students_summary(request, exam_type=None):
    # Fetch secondary students
    exam_type = get_object_or_404(ExamType, name=exam_type)
    form_i_students = Students.objects.filter(current_class='Form I')
    form_ii_students = Students.objects.filter(current_class='Form II')
    form_iii_students = Students.objects.filter(current_class='Form III')
    form_iv_students = Students.objects.filter(current_class='Form IV')
    
       # Fetch primary students
    std_i_students = Students.objects.filter(current_class='STD I')
    std_ii_students = Students.objects.filter(current_class='STD II')
    std_iii_students = Students.objects.filter(current_class='STD III')
    std_iv_students = Students.objects.filter(current_class='STD IV')
    std_v_students = Students.objects.filter(current_class='STD V')
    std_vi_students = Students.objects.filter(current_class='STD VI')
    std_vii_students = Students.objects.filter(current_class='STD VII')
    
       # Fetch nursery students
    baby_students = Students.objects.filter(current_class='Baby')
    kg1_students = Students.objects.filter(current_class='KG1')
    kg2_students = Students.objects.filter(current_class='KG2')
    
    
    # Calculate the total number of secondary  students
    total_form_i_students = form_i_students.count()
    total_form_2_students = form_ii_students.count()
    total_form_3_students = form_iii_students.count()
    total_form_4_students = form_iv_students.count()
    
     # Calculate the total number of primary  students
    total_std_i_students = std_i_students.count()
    total_std_ii_students = std_ii_students.count()
    total_std_iii_students = std_iii_students.count()
    total_std_iv_students = std_iv_students.count()
    total_std_v_students = std_v_students.count()
    total_std_vi_students = std_vi_students.count()
    total_std_vii_tudents = std_vii_students.count()
    
     # Calculate the total number of nursery  students
    total_baby_students = baby_students.count()
    total_kg1_students = kg1_students.count()
    total_kg2_students = kg2_students.count()
    
    
    # Calculate the number of boys and girls in secodary school
    total_boys_form_i_count = form_i_students.filter(gender='Male').count()
    total_girls_form_i_count = form_i_students.filter(gender='Female').count()
    total_boys_form_ii_count = form_ii_students.filter(gender='Male').count()
    total_girls_form_ii_count = form_ii_students.filter(gender='Female').count()
    total_boys_form_iii_count = form_iii_students.filter(gender='Male').count()
    total_girls_form_iii_count = form_iii_students.filter(gender='Female').count()
    total_boys_form_iv_count = form_iv_students.filter(gender='Male').count()
    total_girls_form_iv_count = form_iv_students.filter(gender='Female').count()
    
      # Calculate the number of boys and girls in primary school
    total_boys_std_i_count = std_i_students.filter(gender='Male').count()
    total_girls_std_i_count = std_i_students.filter(gender='Female').count()
    total_boys_std_ii_count = std_ii_students.filter(gender='Male').count()
    total_girls_std_ii_count = std_ii_students.filter(gender='Female').count()
    total_boys_std_iii_count = std_iii_students.filter(gender='Male').count()
    total_girls_std_iii_count = std_iii_students.filter(gender='Female').count()
    total_boys_std_iv_count = std_iv_students.filter(gender='Male').count()
    total_girls_std_iv_count = std_iv_students.filter(gender='Female').count()
    total_boys_std_v_count = std_v_students.filter(gender='Male').count()
    total_girls_std_v_count = std_v_students.filter(gender='Female').count()
    total_boys_std_vi_count = std_vi_students.filter(gender='Male').count()
    total_girls_std_vi_count = std_vi_students.filter(gender='Female').count()
    total_boys_std_vii_count = std_vii_students.filter(gender='Male').count()
    total_girls_std_vii_count = std_vii_students.filter(gender='Female').count()
    
      # Calculate the number of boys and girls in nursery school
    total_boys_baby_count = baby_students.filter(gender='Male').count()
    total_girls_baby_count = baby_students.filter(gender='Female').count()
    total_boys_kg1_count = kg1_students.filter(gender='Male').count()
    total_girls_kg1_count = kg1_students.filter(gender='Female').count()
    total_boys_kg2_count = kg2_students.filter(gender='Male').count()
    total_girls_kg2_count = kg2_students.filter(gender='Female').count()

    
    return render(request, 'hod_template/students_summary.html', {
        'total_form_i_students': total_form_i_students,
        'total_form_2_students': total_form_2_students,
        'total_form_3_students': total_form_3_students,
        'total_form_4_students': total_form_4_students,
        'total_std_i_students': total_std_i_students,
        'total_std_ii_students': total_std_ii_students,
        'total_std_iii_students': total_std_iii_students,
        'total_std_iv_students': total_std_iv_students,
        'total_std_v_students': total_std_v_students,
        'total_std_vi_students': total_std_vi_students,
        'total_std_vii_tudents': total_std_vii_tudents,
        'total_baby_students': total_baby_students,
        'total_kg1_students': total_kg1_students,
        'total_kg2_students': total_kg2_students,
        'total_boys_form_i_count': total_boys_form_i_count,
        'total_girls_form_i_count': total_girls_form_i_count,
        'total_boys_form_ii_count': total_boys_form_ii_count,
        'total_girls_form_ii_count': total_girls_form_ii_count,
        'total_boys_form_iii_count': total_boys_form_iii_count,
        'total_girls_form_iii_count': total_girls_form_iii_count,
        'total_boys_form_iv_count': total_boys_form_iv_count,
        'total_girls_form_iv_count': total_girls_form_iv_count,
        'total_boys_std_i_count': total_boys_std_i_count,
        'total_girls_std_i_count': total_girls_std_i_count,
        'total_boys_std_ii_count': total_boys_std_ii_count,
        'total_girls_std_ii_count': total_girls_std_ii_count,
        'total_boys_std_iii_count': total_boys_std_iii_count,
        'total_girls_std_iii_count': total_girls_std_iii_count,
        'total_boys_std_iv_count': total_boys_std_iv_count,
        'total_girls_std_iv_count': total_girls_std_iv_count,
        'total_boys_std_v_count': total_boys_std_v_count,
        'total_boys_std_v_count': total_boys_std_v_count,
        'total_girls_std_v_count': total_girls_std_v_count,
        'total_boys_std_vi_count': total_boys_std_vi_count,
        'total_girls_std_vi_count': total_girls_std_vi_count,
        'total_boys_std_vii_count': total_boys_std_vii_count,
        'total_girls_std_vii_count': total_girls_std_vii_count,
        'total_boys_baby_count': total_boys_baby_count,
        'total_girls_baby_count': total_girls_baby_count,
        'total_boys_kg1_count': total_boys_kg1_count,
        'total_girls_kg1_count': total_girls_kg1_count,
        'total_boys_kg2_count': total_boys_kg2_count,
        'total_girls_kg2_count': total_girls_kg2_count,
        'exam_type': exam_type,
    })
    