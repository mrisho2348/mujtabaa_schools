
from decimal import Decimal
from io import BytesIO
from django.core.mail import EmailMessage
import json
import os

from xhtml2pdf import pisa  # For generating PDFs
from django.template.loader import get_template
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from financial_management.models import Income_Payment, ServiceDetails, StaffSalary,Invoice
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import default_storage
from twilio.rest import Client 
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required


from student_management_app.models import (
    Attendance,
    AttendanceReport,
    Class_level,
    CustomUser,
    EducationLevel,
    EmploymentHistory,
    FeedBackStaff,   
    LeaveReportStaffs,  
    Parent,
    Qualifications,
    References,  
    SessionYearModel,
    Skills, 
    Staffs, 
    Students, 
    Subject,
   
    )

def secretary_home(request):
    if request.user.is_authenticated:
        try:
            staff = Staffs.objects.get(admin=request.user)
            
            subjects = staff.subjects.all()

            student_count = Students.objects.all().count()            
            invoice_count = Invoice.objects.all().count()            
            parent_count = Parent.objects.all().count()            
            leave_count = LeaveReportStaffs.objects.filter(staff_id=staff.id, leave_status=1).count()
            subject_count = subjects.count()

            return render(request, "secretary_template/secretary_home.html", {
                "student_count": student_count,               
                "parent_count": parent_count,
                "leave_count": leave_count,
                "invoice_count": invoice_count,
                "subject_count": subject_count,             
                "staff": staff,
            })
        except Staffs.DoesNotExist:
            # Handle the case when the staff doesn't exist for the logged-in user
            # You can redirect them to a page or show an error message
            return render(request, "secretary_template/error.html")
    else:
        # Redirect the user to the login page
        return redirect("login")  # Replace "login" with the actual URL name of your login page
    
    
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
            education_level_id = request.POST.get('school_segment')
            current_class_ids = request.POST.get('current_class')
            birth_certificate_id = request.POST.get('birth_certificate_id')
            allergies = request.POST.get('allergies')           
            sheia_address = request.POST.get('sheia_address')
            street_address = request.POST.get('street_address')
            house_number = request.POST.get('house_number')
            health_status = request.POST.get('health_status')
            physical_disability = request.POST.get('physical_disability')
            subjects_ids = request.POST.getlist('subjects')
            session_year_id = request.POST.get('session_year')
            birth_certificate_photo = request.FILES.get('birth_certificate_photo')
            student_photo = request.FILES.get('student_photo')

            # Save the student's profile picture
            student_photo_url = None
            if student_photo:
                if student_photo.size > 5242880:  # 5 MB (size in bytes)
                    raise ValidationError("Profile picture size should be less than 5 MB.")
                if not student_photo.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    raise ValidationError("Only JPG, JPEG, and PNG image files are allowed for profile pictures.")
                fs = FileSystemStorage()
                filename = fs.save(student_photo.name, student_photo)
                student_photo_url = fs.url(filename)

            # Save the birth certificate photo
            birth_certificate_photo_url = None
            if birth_certificate_photo:
                if birth_certificate_photo.size > 5242880:  # 5 MB (size in bytes)
                    raise ValidationError("Birth certificate photo size should be less than 5 MB.")
                if not birth_certificate_photo.name.lower().endswith(('.pdf')):
                    raise ValidationError("Only PDF files are allowed for birth certificate photos.")
                fs = FileSystemStorage()
                filename = fs.save(birth_certificate_photo.name, birth_certificate_photo)
                birth_certificate_photo_url = fs.url(filename)

            # Perform validation
            educational_level = EducationLevel.objects.get(id=education_level_id)
            class_level = Class_level.objects.get(id=current_class_ids)    

            if not first_name or not last_name or not date_of_birth:
                messages.error(request, "Please provide all required fields")
                return redirect("add_student")

            # Retrieve or create the CustomUser instance based on the username
            username = first_name.lower() + last_name.lower()
            default_email = first_name.lower() + "@gmail.com"
            password = '1234'  # Set a default password
            user = CustomUser.objects.create_user(username=username, password=password, email=default_email, first_name=first_name, last_name=last_name, user_type=3)

            # Create a new instance of the Student model
            user.students.surname = surname
            user.students.service_type = service_type                
            user.students.date_of_birth = date_of_birth
            user.students.gender = gender
            user.students.phone_number = phone_number
            user.students.education_level = educational_level
            user.students.selected_class = class_level
            user.students.birth_certificate_id = birth_certificate_id
            user.students.allergies = allergies            
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
            user.students.session_year = session_year

            # Save the student record again to include the subjects and session year
            user.students.save()

            messages.success(request, "Successfully added student")
            return redirect("add_student")

        except ValidationError as ve:
            messages.error(request, ve.message)
        except Exception as e:
            messages.error(request, f"Error saving student record: {str(e)}")

    return redirect("add_student")    


def add_student(request):
    all_subjects = Subject.objects.all()
    all_session_years = SessionYearModel.objects.all()
    staff = Staffs.objects.get(admin=request.user)
    # Query all education levels from the EducationLevel model
    all_education_levels = EducationLevel.objects.all()

    context = {
        "staff": staff,
        "all_subjects": all_subjects,
        "all_session_years": all_session_years,
        "all_education_levels": all_education_levels,  # Add education levels to the context
    }

    return render(request, "secretary_template/add_student.html", context)

def single_student_detail(request, student_id):
    students = get_object_or_404(Students, id=student_id)
    parents = Parent.objects.filter(student=students)
    selected_subjects = students.subjects.all()
    staff = Staffs.objects.get(admin=request.user)
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
        'staff': staff,
        'students': students,
        'father': father,
        'mother': mother,
        'male_guardian': male_guardian,
        'female_guardian': female_guardian,
        'male_sponsor': male_sponsor,
        'female_sponsor': female_sponsor,
        'selected_subjects':selected_subjects,
    }

    return render(request, "secretary_template/student_details.html", context)


def single_parent_detail(request, parent_id):
    staff = Staffs.objects.get(admin=request.user)
    parent = get_object_or_404(Parent, id=parent_id)
    students = parent.student.all()  # Get all students associated with the parent
    
    context = {
        'staff': staff,
        'parent': parent,
        'students': students,
    }
    
    return render(request, "secretary_template/parent_details.html", context)


def delete_parent(request, parent_id):
    # Retrieve the parent object or return a 404 if not found
    parent = get_object_or_404(Parent, id=parent_id)
    staff = Staffs.objects.get(admin=request.user)
    if request.method == 'POST':
        # Perform the deletion
        parent.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'student parent deleted successfully.')
        return redirect('manage_parent')  # Replace 'parent_list' with your actual list view name

    return render(request, 'secretary_template/delete_parent_confirm.html', {'parent': parent,"staff":staff})

def delete_student(request, student_id):
    # Retrieve the student object or return a 404 if not found
    student = get_object_or_404(Students, id=student_id)
    staff = Staffs.objects.get(admin=request.user)
    if request.method == 'POST':
        # Perform the deletion
        student.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'student deleted successfully.')
        return redirect('manage_student')  # Replace 'student_list' with your actual list view name

    return render(request, 'secretary_template/delete_student_confirm.html', {'student': student,"staff":staff})

def manage_student(request):
    students = Students.objects.all()    
    staff = Staffs.objects.get(admin=request.user)
    return render(request, "secretary_template/manage_student.html", {"students": students ,"staff":staff})


def manage_parent(request):
    per_page = request.GET.get('per_page', 3)  # Get the number of items to display per page from the request
    parents = Parent.objects.all()
    parents = parents.order_by('id')
    paginator = Paginator(parents, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    staff = Staffs.objects.get(admin=request.user)
    return render(request, "secretary_template/manage_parent.html", {"students": parents, "page_obj": page_obj, "staff":staff})
 
 
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
            staff = Staffs.objects.get(admin=request.user)
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
            'staff': staff,
            'parent': parent,
            'students': Students.objects.all(),
            'selected_student_ids': [student.id for student in parent.student.all()] if hasattr(parent, 'student') else []
        }
        return render(request, 'hod_template/edit_parent.html', context)

    except Parent.DoesNotExist:
        messages.error(request, "Parent not found.")
        return redirect("edit_parents", parent_id=parent_id)
     
def student_list(request):
    search_query = request.GET.get('search', '')
    students = Students.objects.all()
    
    if search_query:
        students = students.filter(registration_number__icontains=search_query)
    
    paginator = Paginator(students, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    staff = Staffs.objects.get(admin=request.user)
    return render(request, "paginator.html", {"students": students, "page_obj": page_obj, "staff":staff})  


def add_parents(request):
    students = Students.objects.all()
    staff = Staffs.objects.get(admin=request.user)
    return render(request, "secretary_template/parent_form.html", {'students': students, "staff":staff})   


def edit_parents(request, parent_id):
    try:
        request.session['parent_id'] = parent_id       
        parent = Parent.objects.get(id=parent_id)
        students = Students.objects.all()
        staff = Staffs.objects.get(admin=request.user)
        # Get the IDs of currently associated students, if any
        associated_student_ids = parent.student.all().values_list('id', flat=True)

        return render(request, "secretary_template/edit_parent.html", {
            "id": parent_id,
            "username": parent.name,
            "staff": staff,
            "parents": parent,
            "students": students,
            "associated_student_ids": associated_student_ids,  # Pass the associated student IDs to the template
        })
    except Parent.DoesNotExist:
        messages.error(request, "Parent not found.")
        return redirect("manage_parent")





def secretary_template_parent(request, parent_id):
    try:
        parent = get_object_or_404(Parent, id=parent_id)
        staff = Staffs.objects.get(admin=request.user)
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
                # secretary_template the parent record
                
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

                messages.success(request, "Parent and associated students have been successfully secretary_templated.")
                return redirect("edit_parents", parent_id=parent_id)

        context = {
            'staff': staff,
            'parent': parent,
            'students': Students.objects.all(),
            'selected_student_ids': [student.id for student in parent.student.all()] if hasattr(parent, 'student') else []
        }
        return render(request, 'secretary_template/edit_parent.html', context)

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
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=8)
           

            user.parent.phone = phone
            user.parent.occupation = occupation
            user.parent.address = sheia
            user.parent.street_address = street
            user.parent.house_number = house
            user.parent.national_id = national_id
            user.parent.status = status
            user.parent.gender = gender
            user.parent.parent_type = parent_type         

            # Associate the parent with the student
            user.parent.student.add(student)
            user.save()
            messages.success(request, "Parent information saved successfully")
            return redirect("add_parents")

        except Exception as e:
            messages.error(request, "Error saving parent information: " + str(e))

    return redirect("add_parents")

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
        school_segment_ids = request.POST.get('school_segment')
        current_class_ids = request.POST.get('current_class')
        birth_certificate_id = request.POST.get('birth_certificate_id')
        allergies = request.POST.get('allergies')
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

        # secretary_template user information
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # secretary_template student information
        student = Students.objects.get(admin=user)
        student.surname = surname
        student.service_type = service_type
        student.date_of_birth = date_of_birth
        student.gender = gender
        student.phone_number = phone_number
        student.birth_certificate_id = birth_certificate_id
        student.allergies = allergies
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
            
        
        educational_level = EducationLevel.objects.get(pk=school_segment_ids)
        student.education_level = educational_level
                    
       
        current_class = Class_level.objects.get(pk=current_class_ids)
        student.selected_class = current_class

        # Add the selected session year to the student's session_year field
        session_year = SessionYearModel.objects.get(pk=session_year_id)
        student.session_year = session_year

        student.save()

        # del request.session['student_id']
        messages.success(request, "Successfully edited student")
        return redirect("add_previous_education", student_id=user.students.id)
        # return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))

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
        education_levels = EducationLevel.objects.all()
        staff = Staffs.objects.get(admin=request.user)
        # Fetch all subjects and session years
        all_subjects = Subject.objects.all()
        all_session_years = SessionYearModel.objects.all()

        # Get the currently selected class level for the student
        selected_class = student.selected_class  # This will give you the selected class object

        # Get the currently selected subjects for the student
        selected_subjects = student.subjects.all()  # This will give you a queryset of selected subject objects

        selected_subject_ids = [subject.id for subject in selected_subjects]  # Get IDs of selected subjects

        selected_session_year = student.session_year
        print(student.selected_class.id)
        return render(request, "secretary_template/edit_student.html", {
            "student_id": student_id,
            "username": student.admin.username,
            "staff": staff,
            "students": student,
            "all_subjects": all_subjects,
            "all_session_years": all_session_years,
            "selected_subjects": selected_subjects,
            "selected_session_year": selected_session_year,
            "all_education_levels": education_levels,
            "selected_class": selected_class,
            "selected_subjects_ids": selected_subject_ids,
        })
    except Students.DoesNotExist:
        messages.error(request, "Student does not exist")
        return HttpResponseRedirect(reverse("manage_studen"))
    
def generate_invoice(request, payment_id):
    try:
        # Retrieve the Income_Payment object
        income_payment = get_object_or_404(Income_Payment, id=payment_id)

        # Create a PDF invoice
        pdf_content_bytes = generate_pdf_invoice(income_payment)
        
        # Convert the PDF content bytes to a string
        # pdf_content = pdf_content_bytes.decode('utf-8')
        
        # Send the PDF invoice via email
        send_invoice_email(income_payment.student.admin.email, pdf_content_bytes)

        # Send a notification via SMS
        send_sms_notification(income_payment.student.phone_number, "Your invoice has been sent.")

        # Save the invoice details (you can customize this part based on your Invoice model)
        # Assuming you have an Invoice model, you can save details here.
        invoice = Invoice(
            student=income_payment.student,
            service=income_payment.service_details,
            amount_paid=income_payment.amount_paid,
            amount_required=income_payment.service_details.amount_required,
            amount_remaining=income_payment.amount_remaining,
        )
        invoice.save()

        # Redirect to the income payments list page or wherever you want
        messages.success(request, 'Invoice generated and sent successfully.')
        return redirect('income_payment_list')
    except Exception as e:
        # Handle any exceptions here and display an error message
        messages.error(request, f'Error generating invoice: {str(e)}')
        return redirect('income_payment_list')  # You can redirect to an appropriate page or handle the error differently




def generate_pdf_invoice(income_payment):
    
    # Create a PDF content using a template (you need to create an invoice template)
    template_path = 'secretary_template/invoice_template.html'  # Replace with your actual template path
    
    context = {'income_payment': income_payment}
    template = get_template(template_path)
    pdf_content = template.render(context)
    
    # Decode the PDF content from bytes to a string
    pdf_content_str = pdf_content.encode('ISO-8859-1')

    # Generate the PDF content
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(pdf_content_str), result)

    if not pdf.err:
        return result.getvalue()
    return None

def send_invoice_email(email, pdf_content):
    # Create and send an email with the PDF attachment
    subject = 'Invoice for Payment'
    message = 'Please find attached the invoice for your payment.'
    from_email = settings.DEFAULT_FROM_EMAIL    
    recipient_list = [email]  
    print(recipient_list)  
    email_message = EmailMessage(subject, message, from_email, recipient_list)
    email_message.attach('invoice.pdf', pdf_content, 'application/pdf')
    email_message.send()

def send_sms_notification(phone_number, message):
    # Send an SMS notification using Twilio (you need to set up a Twilio account and configure it)
    twilio_account_sid = 'AC6c75ccb7e00ed2c529b0821a72335932'
    twilio_auth_token = '0a3ceaba8535b83069296e3a60ff76e8'
    twilio_phone_number = '+15103384231'
    client = Client(twilio_account_sid, twilio_auth_token)
    print(phone_number)
    try:
        message = client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=phone_number
        )
    except Exception as e:
        # Handle any errors while sending SMS
        pass

def invoice_list(request):
    # Retrieve the list of invoices
    invoices = Invoice.objects.all()
    staff = Staffs.objects.get(admin=request.user)
    context = {
        'staff': staff,
        'invoices': invoices
        }
    return render(request, 'secretary_template/invoice_list.html', context)

def income_payment_form(request):
    # Fetch the students and service details from your database
    students = Students.objects.all()
    service_details = ServiceDetails.objects.all()
    staff = Staffs.objects.get(admin=request.user)
    context = {
        'staff': staff,
        'students': students,
        'service_details': service_details,
    }

    return render(request, 'secretary_template/income_payment_form.html', context)

def save_income_payment(request):
    if request.method == 'POST':
        try:
            student_id = request.POST.get('student')
            service_details_id = request.POST.get('service_details')
            amount_paid_str = request.POST.get('amount_paid')  # Get amount_paid as a string

            # Convert amount_paid to Decimal
            amount_paid = Decimal(amount_paid_str)

            # Retrieve the student and service details objects
            student = Students.objects.get(pk=student_id)
            service_details = ServiceDetails.objects.get(pk=service_details_id)
            staff = Staffs.objects.get(admin=request.user)
            # Calculate the amount remaining
            amount_required = service_details.amount_required
            amount_remaining = amount_required - amount_paid  # Now subtract Decimal from Decimal

            # Create and save the Income_Payment instance
            income_payment = Income_Payment(
                student=student,
                service_details=service_details,
                amount_paid=amount_paid,
                amount_remaining=amount_remaining,
            )
            income_payment.save()

            # Add a success message
            messages.success(request, 'Income Payment saved successfully!')

            # Redirect to a success page or another appropriate URL
            return redirect('income_payment_form')

        except Exception as e:
            # Handle any exceptions here
            messages.error(request, f'Error saving Income Payment: {str(e)}')

    # Retrieve the list of student members
    students = Students.objects.all()
    service_details = ServiceDetails.objects.all()
    context = {
        'staff': staff, 
        'students': students, 
        'service_details': service_details
        }
    return render(request, 'secretary_template/income_payment_form.html', context)

def income_payment_list(request):
    # Retrieve and display the list of expenses
    income_payments = Income_Payment.objects.all()
    context = {'income_payments': income_payments}
    return render(request, 'secretary_template/manage_student_payment_list.html', context)


def edit_income_payment(request, income_payment_id):
    # Retrieve the Income_Payment object to edit
    income_payment = get_object_or_404(Income_Payment, id=income_payment_id)

    # Retrieve all ServiceDetails
    all_service_details = ServiceDetails.objects.all()
    staff = Staffs.objects.get(admin=request.user)
    # Retrieve all Students
    all_students = Students.objects.all()

    if request.method == 'POST':
        try:
            # secretary_template Income_Payment fields based on the POST data
            income_payment.amount_paid = request.POST.get('amount_paid')
            income_payment.save()

            messages.success(request, 'Income payment secretary_templated successfully.')
            return redirect('income_payment_list')
        except Exception as e:
            messages.error(request, f'Error updating income payment: {str(e)}')
            # You can log the exception for debugging purposes if needed

    context = {
        'staff': staff,
        'income_payment': income_payment,
        'all_service_details': all_service_details,
        'all_students': all_students,
    }
    
    return render(request, 'secretary_template/edit_income_payment.html', context)


def delete_income_payment(request, payment_id):
    # Fetch the income payment to be deleted
    income_payment = get_object_or_404(Income_Payment, id=payment_id)
    staff = Staffs.objects.get(admin=request.user)
    if request.method == 'POST':
        # delete the income payment
        income_payment.delete()
        # Redirect to the income payments list view
        return redirect('income_payment_list')
    context = {
        'staff': staff,
        'income_payment': income_payment
        }
    return render(request, 'secretary_template/delete_income_payment.html', context)

def staff_sendfeedback(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaff.objects.filter(staff_id=staff_obj)
    staff = Staffs.objects.get(admin=request.user.id)
    
    return render(request,"secretary_template/staff_feedback.html",{"feedback_data":feedback_data,'staff':staff,})

def staff_sendfeedback_save(request):
    if request.method!= "POST":
        return HttpResponseRedirect(reverse("staff_sendfeedback"))
    
    else:
       feedback_msg = request.POST.get("feedback_msg") 
       staff_obj = Staffs.objects.get(admin=request.user.id)
       try:           
          feedback_report = FeedBackStaff(staff_id=staff_obj,feedback=feedback_msg,feedback_reply="")
          feedback_report.save()
          messages.success(request,"feedback Successfully  sent")
          return HttpResponseRedirect(reverse("staff_sendfeedback"))  
             
       except:
            messages.error(request,"feedback failed to be sent")
            return HttpResponseRedirect(reverse("staff_sendfeedback"))

def   staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    staff_leave_report = LeaveReportStaffs.objects.filter(staff_id=staff_obj)
    staff = Staffs.objects.get(admin=request.user.id)
    return render(request,"secretary_template/staff_leave_template.html",{"staff_leave_report":staff_leave_report, 'staff':staff,})



def staff_apply_leave_save(request):
    if request.method!= "POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")     
        staff_obj = Staffs.objects.get(admin=request.user.id)
       
        try:            
          leave_report =LeaveReportStaffs(staff_id=staff_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
          leave_report.save()
          messages.success(request,"Successfully  staff apply leave ")
          return HttpResponseRedirect(reverse("staff_apply_leave"))  
             
        except:
            messages.error(request,"failed for staff to apply for leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        


def  staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staffs = Staffs.objects.get(admin=user)
    return render(request,"secretary_template/staff_profile.html",{"user":user,"staffs":staffs})  

def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    
    else:
       first_name = request.POST.get("first_name")
       last_name = request.POST.get("last_name")
       password = request.POST.get("password")
       address = request.POST.get("address")
       try:           
          customuser = CustomUser.objects.get(id=request.user.id)
          customuser.first_name = first_name
          customuser.last_name = last_name
          if password!= "" and password!=None:
              customuser.set_password(password)     
                         
          customuser.save()
          
          staffs = Staffs.objects.get(admin = customuser.id)
          staffs.address = address
          staffs.save()
          messages.success(request,"profile is successfully edited")
          return HttpResponseRedirect(reverse("staff_profile"))
      
       except:
            messages.error(request,"editing  of profile  failed")
            return HttpResponseRedirect(reverse("staff_profile"))

def staff_detail(request):
    staff = Staffs.objects.get(admin=request.user.id)
    # Fetch additional staff-related data    
    skills = Skills.objects.filter(staff_id=staff).first()
    employment_history = EmploymentHistory.objects.filter(staff_id=staff)  # Use ForeignKey's filter here
    qualifications = Qualifications.objects.filter(staff_id=staff)
    references = References.objects.filter(staff_id=staff)

    context = {
        'staff': staff,
        'skills': skills,
        'employment_history': employment_history,
        'qualifications': qualifications,
        'references': references,
    }

    return render(request, "secretary_template/staff_details.html", context)            

def staff_salary(request):
    # Retrieve and display the list of staff salaries for the logged-in staff
    staff = Staffs.objects.get(admin=request.user.id)
    staff_salaries = StaffSalary.objects.filter(staff_member__admin=request.user)
    context = {'staff_salaries': staff_salaries,'staff':staff}
    return render(request, 'secretary_template/manage_staff_salary_list.html', context)