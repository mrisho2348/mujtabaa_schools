import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from student_management_app.models import (
    Attendance,
    AttendanceReport,
    CustomUser,
    FeedBackStaff,
    LeaveReportStaffs,
    SessionYearModel,
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
            return render(request, "staff_template/error.html")
    else:
        # Redirect the user to the login page
        return redirect("login")  # Replace "login" with the actual URL name of your login page
    
def staff_take_attendance(request):
    staff = Staffs.objects.get(admin=request.user.id)
    subjects = staff.subjects.all() 
    session_years = SessionYearModel.objects.all()
    return render(request,"staff_template/staff_take_attendance.html",{"subjects":subjects,"session_years":session_years})



@csrf_exempt
def get_students(request):
    subject_id = request.POST.get("subject")
    session_year_id = request.POST.get("session_year")
 
    try:
        subject = Subject.objects.get(id=subject_id)
        session_year = SessionYearModel.objects.get(id=session_year_id)
        print(session_year.session_start_year)
        print(subject.subject_name)
        # Get all students associated with the subject and session year
        students = Students.objects.filter(subjects=subject, session_year=session_year)
        
        list_data = []

        for student in students:
            print(student)
            data_small = {
                "id": student.admin.id,
                "name": student.admin.first_name + " " + student.admin.last_name
            }
            list_data.append(data_small)
            print(list_data)

        return JsonResponse(list_data, safe=False)
    except Subject.DoesNotExist:
        return JsonResponse({"error": "Subject not found."}, status=404)
    except SessionYearModel.DoesNotExist:
        return JsonResponse({"error": "Session year not found."}, status=404)
    
    
    
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
    subjects = staff.subjects.all() 
    session_years = SessionYearModel.objects.all()
    return render(request,"staff_template/staff_update_attendance.html",{"subjects":subjects,"session_years":session_years})

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
    attendance_date_id=Attendance.objects.get(id=attendance_date)
    attendance_data =AttendanceReport.objects.filter(attendance_id=attendance_date_id)   
    
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
    return render(request,"staff_template/staff_feedback.html",{"feedback_data":feedback_data})

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
    return render(request,"staff_template/staff_leave_template.html",{"staff_leave_report":staff_leave_report})



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
    if request.method == 'POST':
        try:
            student_id = request.POST.get('student_id')
            subject_id = request.POST.get('subject')
            exam_type_id = request.POST.get('exam_type_id')
            marks = request.POST.get('marks')
            date_of_exam = request.POST.get('date_of_exam')

            # Retrieve the student's current class
            student = Students.objects.get(id=student_id)
            current_class = student.current_class

            # Check if there is an existing result for this student, subject, and exam type
            existing_result = Result.objects.filter(
                student_id=student_id,
                subject_id=subject_id,
                exam_type_id=exam_type_id,
                current_class=current_class
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
                    current_class=current_class
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
        'exam_types': exam_types
    }

    return render(request, 'staff_template/upload_results.html', context)


def student_details(request, student_id, exam_type_id):
    # Retrieve the exam type and student based on their IDs
    exam_type = get_object_or_404(ExamType, id=exam_type_id)
    student = get_object_or_404(Students, id=student_id)
    
    current_staff = Staffs.objects.get(admin=request.user.id)
    # Retrieve the subjects taught by the currently logged-in staff for this student
    staff_subjects = current_staff.subjects.filter(id__in=student.subjects.all())

    return render(request, 'staff_template/upload_results.html', {
        'student': student,
        'subjects': staff_subjects,
        'exam_type': exam_type,
    })
    
def students_summary_staff(request, exam_type=None):
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

    
    return render(request, 'staff_template/students_summary.html', {
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
    exam_type = get_object_or_404(ExamType, id=exam_type_id)
    students = Students.objects.filter(current_class=current_class)
    return render(request, 'staff_template/form_i_students_template.html', {
        'students': students,
        'current_class': current_class,
        'exam_type': exam_type,
        
    })        
    

@login_required  # Add the login_required decorator to ensure the user is logged in
def subject_wise_results(request, student_id, exam_type_id):
    # Get the student based on the provided student_id
    student = Students.objects.get(id=student_id)  # Replace 'Students' with your actual student model

    # Query the results for the specific student
    results = Result.objects.filter(student=student, exam_type_id=exam_type_id)

    # Retrieve subjects for the logged-in staff (assuming it's stored in staff_subjects)
    staff_subjects = request.user.staffs.subjects.all()  # Replace 'staffs' with the actual related name

    context = {
        'student': student,
        'results': results,
        'staff_subjects': staff_subjects,  # Pass the staff's subjects to the template
        'exam_type_id': exam_type_id,
    }

    return render(request, 'staff_template/subject_wise_results.html', context)   


def update_students_results(request, result_id, student_id, exam_type_id):
    # Retrieve the exam type and student based on their IDs
    exam_type = get_object_or_404(ExamType, id=exam_type_id)
    student = get_object_or_404(Students, id=student_id)

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
        'existing_result': existing_result,  # Pass the existing result to the template
    })
    
def assign_results(request, student_id, exam_type_id):
    # Retrieve the exam type and student based on their IDs
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
        
    })
            