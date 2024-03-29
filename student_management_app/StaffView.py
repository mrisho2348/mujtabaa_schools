import json
import os
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.http import FileResponse, HttpResponse, HttpResponseRedirect, JsonResponse,Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from financial_management.models import StaffSalary

from student_management_app.models import (
    Attendance,
    AttendanceReport,
    Class_level,
    CustomUser,
    EmploymentHistory,
    FeedBackStaff,
    LeaveReportStaffs,
    Notes,
    Qualifications,
    References,
    SessionYearModel,
    Skills,
    Staffs, 
    Students, 
    Subject,
    ExamType,
    Result
    )


def staff_home(request):
    if request.user.is_authenticated:
        try:
            staff = Staffs.objects.get(admin=request.user)
            
            subjects = staff.subjects.all()

            students_count = Students.objects.filter(subjects__in=subjects).count()
            attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
            leave_count = LeaveReportStaffs.objects.filter(staff_id=staff.id, leave_status=1).count()
            subject_count = subjects.count()

            subject_list = []
            attendance_list = []
            for subject in subjects:
                attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
                subject_list.append(subject.subject_name)
                attendance_list.append(attendance_count1)

            student_list = []
            student_list_attendance_present = []
            student_list_attendance_absent = []
            student_attendance = Students.objects.filter(subjects__in=subjects)
            for student in student_attendance:
                attendance_present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
                attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
                student_list.append(student.admin.username)
                student_list_attendance_present.append(attendance_present_count)
                student_list_attendance_absent.append(attendance_absent_count)

            return render(request, "staff_template/staff_home.html", {
                "student_count": students_count,
                "attendance_count": attendance_count,
                "leave_count": leave_count,
                "subject_count": subject_count,
                "subject_list": subject_list,
                "attendance_list": attendance_list,
                "student_list": student_list,
                "student_list_attendance_present": student_list_attendance_present,
                "student_list_attendance_absent": student_list_attendance_absent,
                "staff": staff,
            })
        except Staffs.DoesNotExist:
            # Handle the case when the staff doesn't exist for the logged-in user
            # You can redirect them to a page or show an error message
            return render(request, "hod_template/error.html")
    else:
        # Redirect the user to the login page
        return redirect("login")  # Replace "login" with the actual URL name of your login page
    
def staff_take_attendance(request):
    staff = Staffs.objects.get(admin=request.user.id)

    # Assuming that the educational level is a ForeignKey in Staffs model
    educational_level = staff.education_level

    # Retrieve class levels corresponding to the staff's educational level
    class_levels = Class_level.objects.filter(school_level=educational_level)

    subjects = staff.subjects.all() 
    session_years = SessionYearModel.objects.all()

    return render(request, "staff_template/staff_take_attendance.html", {
        "subjects": subjects,
        "session_years": session_years,
        "class_levels": class_levels,
    })



@csrf_exempt
def get_students(request):
    subject_id = request.POST.get("subject")
    session_year_id = request.POST.get("session_year")
    current_class = request.POST.get("current_class")  # Add this line
    form_one_class = Class_level.objects.get(name=current_class)    
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session_year = get_object_or_404(SessionYearModel, id=session_year_id)

        # Get all students associated with the subject, session year, and current class
        students = Students.objects.filter(
            subjects=subject,
            session_year=session_year,
            selected_class=form_one_class  # Filter by the current class
        )

        list_data = []

        for student in students:
            data_small = {
                "id": student.admin.id,
                "name": student.admin.first_name + " " + student.admin.last_name
            }
            list_data.append(data_small)

        return JsonResponse(list_data, safe=False)

    except Http404:
        return JsonResponse({"error": "Subject or session year not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
    
    
@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")

    subject_model=Subject.objects.get(id=subject_id)
    session_model=SessionYearModel.objects.get(id=session_year_id)
    json_sstudent=json.loads(student_ids)
    #print(data[0]['id'])


    try:
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_id=session_model)
        attendance.save()

        for stud in json_sstudent:
             student=Students.objects.get(admin_id=stud['id'])
             attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")
    
    
def staff_update_attendance(request):
    staff = Staffs.objects.get(admin=request.user.id)

    # Assuming that the educational level is a ForeignKey in Staffs model
    educational_level = staff.education_level

    # Retrieve class levels corresponding to the staff's educational level
    class_levels = Class_level.objects.filter(school_level=educational_level)

    subjects = staff.subjects.all() 
    session_years = SessionYearModel.objects.all()

    return render(request, "staff_template/staff_update_attendance.html", {
        "subjects": subjects,
        "session_years": session_years,
        "class_levels": class_levels,
    })

@csrf_exempt
def get_attendance_date(request):
     subject = request.POST.get("subject_id")
     session_year_id = request.POST.get("session_year_id")
  
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
 
@csrf_exempt
def get_student_attendance(request):  
    attendance_date=request.POST.get("attendance_date_id") 
    current_class = request.POST.get("current_class") 
    form_one_class = Class_level.objects.get(name=current_class)
    students = Students.objects.filter(selected_class=form_one_class)
    attendance_date_id=Attendance.objects.get(id=attendance_date)
    attendance_data = AttendanceReport.objects.filter(
            attendance_id=attendance_date_id,
            student_id__in=students
        )
         
    
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)



@csrf_exempt
def save_updateattendance(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")     
    attendance=Attendance.objects.get(id=attendance_date)     
    json_sstudent=json.loads(student_ids)
    #print(data[0]['id'])


    try:
        for stud in json_sstudent:
             student=Students.objects.get(admin_id=stud['id'])
             attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
             attendance_report.status =stud["status"]
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")
    

def staff_sendfeedback(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaff.objects.filter(staff_id=staff_obj)
    staff = Staffs.objects.get(admin=request.user.id)
    return render(request,"staff_template/staff_feedback.html",{"feedback_data":feedback_data,'staff':staff,})

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
    return render(request,"staff_template/staff_leave_template.html",{"staff_leave_report":staff_leave_report, 'staff':staff,})



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
    return render(request,"staff_template/staff_profile.html",{"user":user,"staffs":staffs})  

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
        


def assign_results_save(request):
    staff = Staffs.objects.get(admin=request.user.id)
    
    if request.method == 'POST':
        try:
            student_id = request.POST.get('student_id')
            subject_id = request.POST.get('subject')
            exam_type_id = request.POST.get('exam_type_id')
            marks = request.POST.get('marks')
            date_of_exam = request.POST.get('date_of_exam')

            # Retrieve the student's current class
            student = get_object_or_404(Students, id=student_id)
            selected_class = student.selected_class

            # Check if there is an existing result for this student, subject, and exam type
            existing_result = Result.objects.filter(
                student_id=student_id,
                subject_id=subject_id,
                exam_type_id=exam_type_id,
                selected_class=selected_class
            ).first()

            if existing_result:
                # Update the existing result
                existing_result.marks = marks
                existing_result.date_of_exam = date_of_exam
                existing_result.save()
                messages.success(request, 'Exam results updated successfully.')
                redirect_url = reverse('subject_wise_results', args=[student.id, exam_type_id])
                return redirect(redirect_url)
            else:
                # Create a new result
                result = Result(
                    student_id=student_id,
                    subject_id=subject_id,
                    exam_type_id=exam_type_id,
                    marks=marks,
                    date_of_exam=date_of_exam,
                    selected_class=selected_class
                )
                result.save()
                messages.success(request, 'Exam results assigned successfully.')

        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        
        redirect_url = reverse('assign_results', args=[student.id, exam_type_id])    
        return redirect(redirect_url)  # Redirect to the appropriate page

    students = Students.objects.all()
    exam_types = ExamType.objects.all()

    context = {
        'students': students,
        'exam_types': exam_types,
        'staff': staff,
    }

    return render(request, 'staff_template/upload_results.html', context)


def student_details(request, student_id, exam_type_id):
    # Retrieve the exam type and student based on their IDs
    staff = Staffs.objects.get(admin=request.user.id)
    exam_type = get_object_or_404(ExamType, id=exam_type_id)
    student = get_object_or_404(Students, id=student_id)
    
    current_staff = Staffs.objects.get(admin=request.user.id)
    # Retrieve the subjects taught by the currently logged-in staff for this student
    staff_subjects = current_staff.subjects.filter(id__in=student.subjects.all())

    return render(request, 'staff_template/upload_results.html', {
        'student': student,
        'subjects': staff_subjects,
        'exam_type': exam_type,
        'staff':staff,
    })
    
def students_summary_staff(request, exam_type=None):
    # Fetch secondary students
    staff = Staffs.objects.get(admin=request.user.id)
    exam_type = get_object_or_404(ExamType, name=exam_type)
    form_one_class = Class_level.objects.get(name='FORM ONE')
    form_i_students = Students.objects.filter(selected_class=form_one_class)
    form_two_class = Class_level.objects.get(name='FORM TWO')
    form_ii_students = Students.objects.filter(selected_class=form_two_class)
    form_three_class = Class_level.objects.get(name='FORM THREE')
    form_iii_students = Students.objects.filter(selected_class=form_three_class)
    form_four_class = Class_level.objects.get(name='FORM FOUR')
    form_iv_students = Students.objects.filter(selected_class=form_four_class)
    
       # Fetch primary students
    standard_one_class = Class_level.objects.get(name='STANDARD ONE')   
    std_i_students = Students.objects.filter(selected_class=standard_one_class)
    standard_two_class = Class_level.objects.get(name='STANDARD TWO')   
    std_ii_students = Students.objects.filter(selected_class=standard_two_class)
    standard_three_class = Class_level.objects.get(name='STANDARD THREE') 
    std_iii_students = Students.objects.filter(selected_class=standard_three_class)
    standard_four_class = Class_level.objects.get(name='STANDARD FOUR') 
    std_iv_students = Students.objects.filter(selected_class=standard_four_class)
    standard_five_class = Class_level.objects.get(name='STANDARD FIVE') 
    std_v_students = Students.objects.filter(selected_class=standard_five_class)
    standard_six_class = Class_level.objects.get(name='STANDARD SIX')     
    std_vi_students = Students.objects.filter(selected_class=standard_six_class)
    standard_seven_class = Class_level.objects.get(name='STANDARD SEVEN')         
    std_vii_students = Students.objects.filter(selected_class=standard_seven_class)
    
       # Fetch nursery students
    Baby_class = Class_level.objects.get(name='Baby')      
    baby_students = Students.objects.filter(selected_class=Baby_class)
    KG1_class = Class_level.objects.get(name='KG1')  
    kg1_students = Students.objects.filter(selected_class=KG1_class)
    KG2_class = Class_level.objects.get(name='KG2') 
    kg2_students = Students.objects.filter(selected_class=KG2_class)
    
    
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

    
    return render(request, 'staff_template/students_summary.html', {
         'staff':staff,
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
    

    
def form_i_students(request, exam_type_id, current_class):
    # Fetch Form I students
    staff = Staffs.objects.get(admin=request.user.id)
    exam_type = get_object_or_404(ExamType, id=exam_type_id)
    form_one_class = Class_level.objects.get(name=current_class)
    students = Students.objects.filter(selected_class=form_one_class)
    return render(request, 'staff_template/form_i_students_template.html', {
        'students': students,
        'current_class': current_class,
        'exam_type': exam_type,
        'staff':staff,
        
    })        
    

@login_required  # Add the login_required decorator to ensure the user is logged in
def subject_wise_results(request, student_id, exam_type_id):
    staff = Staffs.objects.get(admin=request.user.id)
    # Get the student based on the provided student_id
    student = Students.objects.get(id=student_id)  # Replace 'Students' with your actual student model

    # Query the results for the specific student
    results = Result.objects.filter(student=student, exam_type_id=exam_type_id)

    # Retrieve subjects for the logged-in staff (assuming it's stored in staff_subjects)
    staff_subjects = request.user.staffs.subjects.all()  # Replace 'staffs' with the actual related name

    context = {
        'student': student,
        'results': results,
         'staff':staff,
        'staff_subjects': staff_subjects,  # Pass the staff's subjects to the template
        'exam_type_id': exam_type_id,
    }

    return render(request, 'staff_template/subject_wise_results.html', context)   


def update_students_results(request, result_id, student_id, exam_type_id):
    # Retrieve the exam type and student based on their IDs
    exam_type = get_object_or_404(ExamType, id=exam_type_id)
    student = get_object_or_404(Students, id=student_id)
    staff = Staffs.objects.get(admin=request.user.id)
    # Retrieve the currently logged-in staff
    current_staff = Staffs.objects.get(admin=request.user.id)

    # Retrieve the subjects taught by the currently logged-in staff for this student
    staff_subjects = current_staff.subjects.filter(id__in=student.subjects.all())

    # Check if there is an existing result for this student and subject
    existing_result = Result.objects.filter(id=result_id, student=student).first()

    return render(request, 'staff_template/upload_results.html', {
        'student': student,
        'subjects': staff_subjects,
        'exam_type': exam_type,
         'staff':staff,
        'existing_result': existing_result,  # Pass the existing result to the template
    })
    
def assign_results(request, student_id, exam_type_id):
    # Retrieve the exam type and student based on their IDs
    staff = Staffs.objects.get(admin=request.user.id)
    exam_type = get_object_or_404(ExamType, id=exam_type_id)
    student = get_object_or_404(Students, id=student_id)

    # Retrieve the currently logged-in staff
    current_staff = Staffs.objects.get(admin=request.user.id)

    # Retrieve the subjects taught by the currently logged-in staff for this student
    staff_subjects = current_staff.subjects.filter(id__in=student.subjects.all())

    # Check if there is an existing result for this student and subject


    return render(request, 'staff_template/upload_results.html', {
        'student': student,
        'subjects': staff_subjects,
        'exam_type': exam_type,
        'staff':staff,
        
    })
            
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

    return render(request, "staff_template/staff_details.html", context)            

def staff_salary(request):
    # Retrieve and display the list of staff salaries for the logged-in staff
    staff = Staffs.objects.get(admin=request.user.id)
    staff_salaries = StaffSalary.objects.filter(staff_member__admin=request.user)
    context = {'staff_salaries': staff_salaries,'staff':staff}
    return render(request, 'staff_template/manage_staff_salary_list.html', context)


def add_notes(request):
    try:
        if request.method == 'POST':
            # Extract data from the form submission
            subject_id = request.POST.get('subject')
            selected_class_id = request.POST.get('selected_class')
            title = request.POST.get('title')
            description = request.POST.get('description')
            file = request.FILES.get('file')

            # Validate file format and size
            if file:
                max_file_size = 5 * 1024 * 1024  # 5 MB
                accepted_formats = ['pdf', 'doc', 'docx']

                if file.size > max_file_size:
                    raise ValidationError("File size should be less than 5 MB.")

                file_extension = file.name.lower().split('.')[-1]
                print(file_extension)
                if file_extension not in accepted_formats:
                    raise ValidationError("Only PDF, DOC, and DOCX file formats are allowed.")

                # Save the file to the database
                fs = FileSystemStorage()
                filename = slugify(file.name)  # Use slugify to create a valid filename
                file_path = fs.save(filename, file)
                file_url = fs.url(file_path)
            else:
                file_url = None

            # Retrieve the logged-in staff
            logged_in_staff = request.user.staffs

            # Create a new Notes instance
            new_note = Notes(
                staff=logged_in_staff,
                subject_id=subject_id,
                selected_class_id=selected_class_id,
                title=title,
                description=description,
                file=file_url,
            )

            # Save the new note
            new_note.save()

            messages.success(request, 'Notes added successfully!')
            return redirect('add_notes')

        else:
            # Retrieve the logged-in staff
            logged_in_staff = request.user.staffs

            # Get subjects and class levels associated with the logged-in staff
            subjects = logged_in_staff.subjects.all()
            class_levels = logged_in_staff.education_level.class_level_set.all()

            # Render the template with the required context data
            return render(request, 'staff_template/add_notes.html', {'subjects': subjects, 'class_levels': class_levels})

    except ValidationError as e:
        messages.error(request, str(e))
        return redirect('add_notes')

    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('add_notes')# Redirect to the appropriate URL after encountering an error
 
def edit_notes(request, note_id):
    try:
        # Retrieve the note to be edited
        note = Notes.objects.get(pk=note_id)

        if request.method == 'POST':
            # Extract data from the form submission
            subject_id = request.POST.get('subject')
            selected_class_id = request.POST.get('selected_class')
            title = request.POST.get('title')
            description = request.POST.get('description')
            file = request.FILES.get('file')

            # Validate file format and size
            if file:
                max_file_size = 5 * 1024 * 1024  # 5 MB
                accepted_formats = ['.pdf', '.doc', '.docx']

                if file.size > max_file_size:
                    raise ValidationError("File size should be less than 5 MB.")

                file_extension = file.name.lower().split('.')[-1]
                if file_extension not in accepted_formats:
                    raise ValidationError("Only PDF, DOC, and DOCX file formats are allowed.")

                # Save the file to the database
                fs = FileSystemStorage()
                filename = slugify(file.name)  # Use slugify to create a valid filename
                file_path = fs.save(filename, file)
                note.file = file_path

            # Update the existing note with the new data
            note.subject_id = subject_id
            note.selected_class_id = selected_class_id
            note.title = title
            note.description = description

            # Save the changes
            note.save()

            messages.success(request, 'Note updated successfully!')
            return redirect('edit_notes', note_id=note_id)

        else:
            # Retrieve the logged-in staff
            logged_in_staff = request.user.staffs

            # Get subjects and class levels associated with the logged-in staff
            subjects = logged_in_staff.subjects.all()
            class_levels = logged_in_staff.education_level.class_level_set.all()

            # Render the template with the required context data
            return render(request, 'staff_template/edit_notes.html', {'subjects': subjects, 'class_levels': class_levels, 'note': note})

    except Notes.DoesNotExist:
        messages.error(request, 'Note not found!')
        return redirect('edit_notes', note_id=note_id)  # Replace 'your_error_redirect_url' with the actual URL for error handling

    except ValidationError as e:
        messages.error(request, str(e))
        return redirect('edit_notes', note_id=note_id)

    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('edit_notes', note_id=note_id)
    




def download_notes(request, note_id):
    note = get_object_or_404(Notes, pk=note_id)
    file_path = note.file.name  # Use the file's name instead of path

    try:
        s3_storage = default_storage  # Use default_storage for S3
        file_data = s3_storage.open(file_path, 'rb').read()

        response = HttpResponse(file_data, content_type="application/octet-stream")
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
        return response
    except FileNotFoundError:
        raise Http404


def manage_notes(request):
    # Retrieve the logged-in staff
    logged_in_staff = request.user.staffs
    # Get notes associated with the logged-in staff
    notes = Notes.objects.filter(staff=logged_in_staff)

    # Render the template with the required context data
    return render(request, 'staff_template/manage_notes.html', {'notes': notes})  