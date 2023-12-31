
from datetime import datetime
from time import strptime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from financial_management.models import Income_Payment, Invoice
from student_management_app.models import (
    Attendance,
    AttendanceReport,  
    CustomUser,
    FeedBackStudent,
    LeaveReportStudent,
    Notes,
    Parent,
    Route,
    Students, 
    Subject,
    ExamType,
    Result,
    StudentExamInfo,
    StudentPositionInfo,
    TransportationAttendance,
    TransportationAttendanceReport,
)
from student_management_app.templatetags.custom_filters import strftime


def student_home(request):
    student_object = Students.objects.get(admin=request.user.id)
    attendance_present = AttendanceReport.objects.filter(student_id=student_object, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_object, status=False).count()
    attendance_total = AttendanceReport.objects.filter(student_id=student_object).count()
    
    # Get subject-related data
    subject_data = Subject.objects.filter(students=student_object)  # Assuming students is the related_name of the ManyToManyField
    subject_name = []
    data_present = []
    data_absent = []
    total_subjects_taken = student_object.subjects.count()  # Assuming subjects is the related_name of the ManyToManyField
    
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(
            attendance_id__in=attendance, status=True, student_id=student_object.id
        ).count()
        attendance_absent_count = AttendanceReport.objects.filter(
            attendance_id__in=attendance, status=False, student_id=student_object.id
        ).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)
    
    return render(
        request,
        "student_template/student_home.html",
        {
            "attendance_total": attendance_total,
            "attendance_present": attendance_present,
            "attendance_absent": attendance_absent,
            "subject_name": subject_name,
            "data_present": data_present,
            "data_absent": data_absent,
            "total_subjects_taken": total_subjects_taken,
            "students": student_object,
        },
    )


def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id)
    subjects = student.subjects.all()  # Assuming subjects is the related_name of the ManyToManyField
    return render(request, "student_template/student_view_attendance.html", {"subjects": subjects,"students":student})


def student_view_attendance_post(request):
    subject_id = request.POST.get("subject")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    
    start_date_parse = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_parse = datetime.strptime(end_date, "%Y-%m-%d").date()
    subject_obj = Subject.objects.get(id=subject_id)
    user_obj = CustomUser.objects.get(id = request.user.id)
    student_obj = Students.objects.get(admin=user_obj)
    attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse,end_date_parse),subject_id=subject_obj)
    attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance,student_id = student_obj)
    
    for attendance_report in attendance_reports:
        print("Date: "+str(attendance_report.attendance_id.attendance_date), "status: " + str(attendance_report.status))
        
    return render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports,"students":student_obj}) 




def student_sendfeedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    return render(request,"student_template/student_feedback.html",{"feedback_data":feedback_data,"students":student_obj})

def student_sendfeedback_save(request):
    if request.method!= "POST":
        return HttpResponseRedirect(reverse("student_sendfeedback"))
    
    else:
       feedback_msg = request.POST.get("feedback_msg") 
       student_obj = Students.objects.get(admin=request.user.id)
       try:           
          feedback_report = FeedBackStudent(student_id=student_obj,feedback=feedback_msg,feedback_reply="")
          feedback_report.save()
          messages.success(request,"feedback Successfully  sent")
          return HttpResponseRedirect(reverse("student_sendfeedback"))  
             
       except:
            messages.error(request,"feedback failed to be sent")
            return HttpResponseRedirect(reverse("student_sendfeedback"))

def   student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    student_leave_report =LeaveReportStudent.objects.filter(student_id=student_obj)
    return render(request,"student_template/student_leave_template.html",{"student_leave_report":student_leave_report,"students":student_obj})



def student_apply_leave_save(request):
    if request.method!= "POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")     
        staff_obj = Students.objects.get(admin=request.user.id)
       
        try:            
          leave_report =LeaveReportStudent(student_id=staff_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
          leave_report.save()
          messages.success(request,"Successfully  staff apply leave ")
          return HttpResponseRedirect(reverse("student_apply_leave"))  
             
        except:
            messages.error(request,"failed for staff to apply for leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        
        


def  student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    students = Students.objects.get(admin=user)
    return render(request,"student_template/student_profile.html",{"user":user,"students":students})  

@login_required
def student_profile_save(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        address = request.POST.get("address")

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != "" and password is not None:
                customuser.set_password(password)
            customuser.save()

            students = Students.objects.get(admin=customuser.id)
            students.address = address
            students.save()

            messages.success(request, "Profile has been successfully edited")
        except:
            messages.error(request, "Editing of profile failed")

    return HttpResponseRedirect(reverse("student_profile"))


def student_subject_wise_result(request, exam_type):
    # Get the student based on the provided student_id
    student = Students.objects.get(admin=request.user.id)
    # Replace 'Students' with your actual student mode
    
  
    form_i_students = Students.objects.filter(selected_class=student.selected_class)
    total_students = form_i_students.count()
    # Query the results for the specific student
    exam_type = get_object_or_404(ExamType, name=exam_type)

    results = Result.objects.filter(student=student, exam_type_id=exam_type.id)
    exam_info = StudentExamInfo.objects.filter(
        student=student,
        exam_type=exam_type,
        selected_class=student.selected_class
    ).first()

    # Retrieve the StudentPositionInfo for the specified student, exam type, and current class
    position_info = StudentPositionInfo.objects.filter(
        student=student,
        exam_type=exam_type,
        current_class=student.selected_class
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

    context = {
        'student': student,
        'results': results,
        "students": student,
        'exam_type': exam_type,
        'position': position,  # Add position to the context
        'division': division,  # Add position to the context
        'total_students': total_students,  # Add position to the context
        'total_grade_points': total_grade_points,  # Add total_grade_points to the context
    }

    return render(request, 'student_template/subject_wise_results.html', context)


def single_student_details(request):
    students =Students.objects.get(admin=request.user.id)
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

    return render(request, "student_template/student_details.html", context)

@login_required
def student_invoice_list(request):
    # Retrieve the list of invoices for the logged-in student
    student = Students.objects.get(admin=request.user.id) # Assuming you have a OneToOneField to link User to Students
    invoices = Invoice.objects.filter(student=student)

    context = {'invoices': invoices, "students": student}
    return render(request, 'student_template/invoice_list.html', context)
    
    

 

def student_transport_attendance_post(request):
    route_id = request.POST.get("route")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    
    start_date_parse = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_parse = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    route_obj = Route.objects.get(id=route_id)
    user_obj = CustomUser.objects.get(id=request.user.id)
    student_obj = Students.objects.get(admin=user_obj)
    
    attendance = TransportationAttendance.objects.filter(
        date__range=(start_date_parse, end_date_parse),
        route=route_obj
    )
    
    attendance_reports = TransportationAttendanceReport.objects.filter(
        attendance__in=attendance,
        student=student_obj
    )
    
    for attendance_report in attendance_reports:
        print(
            "Date: " + str(attendance_report.attendance.date),
            "Status: " + str(attendance_report.status)
        )
        
    return render(request, "student_template/student_transport_attendance_data.html", {
        "attendance_reports": attendance_reports,
        "students": student_obj,
    })
    
def student_view_transport_attendance(request):
    student = Students.objects.get(admin=request.user)  # Use request.user directly
    routes = student.routes.all()  # Access the related routes
    return render(request, "student_template/student_view_transport_attendance.html", {"routes": routes, "students": student})

def student_notes(request):
    # Assuming the student is logged in and associated with the request
    logged_in_student = request.user.students
    # Retrieve the class level of the logged-in student
    student_class = logged_in_student.selected_class
    # Fetch all notes related to the student's class
    class_notes = Notes.objects.filter(selected_class=student_class)

    # You can pass the class_notes queryset to your template for rendering
    return render(request, 'student_template/students_view_notes.html', {'class_notes': class_notes})

@login_required
def student_payments_record(request):
    # Get the logged-in student
    student = request.user.students
    # Retrieve payment records for the student
    payments = Income_Payment.objects.filter(student=student)
    # Group payments by service
    grouped_payments = {}
    for payment in payments:
        service_name = payment.service_details.service_name
        if service_name not in grouped_payments:
            grouped_payments[service_name] = []
        grouped_payments[service_name].append(payment)

    return render(request, 'student_template/student_payment_record.html', {'grouped_payments': grouped_payments,'students':student})