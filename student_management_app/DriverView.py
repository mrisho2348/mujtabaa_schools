import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Count, Case, When, F,IntegerField
from django.db.models.functions import Coalesce
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import JsonResponse
from django.db.models import DateField
from django.db.models.functions import Cast
from django.contrib.auth.decorators import login_required
from datetime import date

from financial_management.models import DriverSalary  # Import date from datetime module

from .models import (  
    CustomUser,
    Route, 
  
    Students, 
    SchoolDriver,
    LeaveReportSchoolDriver,
    FeedbackSchoolDriver,
    TransportationAttendance,
    TransportationAttendanceReport,
   
    )

@login_required
def driver_home(request):
    if request.user.is_authenticated:
        try:
            driver = SchoolDriver.objects.get(admin=request.user)

            # Fetch the number of attendances taken by the driver
            attendance_count = TransportationAttendance.objects.filter(driver=driver).count()

            # Fetch the number of students present in each route
            route_student_counts = Route.objects.annotate(
                total_students=Count('students')
            ).values('name', 'total_students')

            # Fetch the number of students present and absent in each route
            route_attendance_counts = TransportationAttendance.objects.filter(
                driver=driver,
                date=date.today()
            ).values('route__name').annotate(
                total_present=Coalesce(
                    Count(
                        Case(
                            When(
                                transportationattendancereport__status=True,
                                then=1
                            ),
                            output_field=IntegerField()
                        )
                    ),
                    0
                ),
                total_absent=Coalesce(
                    Count(
                        Case(
                            When(
                                transportationattendancereport__status=False,
                                then=1
                            ),
                            output_field=IntegerField()
                        )
                    ),
                    0
                )
            )

            # Fetch the total number of routes
            total_routes = Route.objects.count()

            return render(request, "driver_template/driver_home.html", {
                "driver": driver,
                "attendance_count": attendance_count,
                "route_student_counts": route_student_counts,
                "route_attendance_counts": route_attendance_counts,
                "total_routes": total_routes,  # Pass the total number of routes to the template
                "total_present": sum(item['total_present'] for item in route_attendance_counts),
                "total_absent": sum(item['total_absent'] for item in route_attendance_counts),
            })
        except SchoolDriver.DoesNotExist:
            # Handle the case when the driver doesn't exist for the logged-in user
            # You can redirect them to a page or show an error message
            return render(request, "hod_template/error.html")
        except Exception as e:
            # Handle any other exceptions that might occur
            return render(request, "hod_template/error.html", {"error_message": str(e)})
    else:
        # Redirect the user to the login page
        return redirect("login")  # Replace "login" with the actual URL name of your login page view
    
@login_required    
def driver_sendfeedback(request):
    driver_obj = SchoolDriver.objects.get(admin=request.user.id)
    feedback_data = FeedbackSchoolDriver.objects.filter(driver_id=driver_obj)    
    return render(request,"driver_template/driver_feedback.html",{"feedback_data":feedback_data,"driver":driver_obj})


@login_required
def driver_sendfeedback_save(request):
    if request.method!= "POST":
        return HttpResponseRedirect(reverse("driver_sendfeedback"))
    
    else:
       feedback_msg = request.POST.get("feedback_msg")        
       driver_obj = SchoolDriver.objects.get(admin=request.user.id)
       try:           
          feedback_report = FeedbackSchoolDriver(driver_id=driver_obj,feedback=feedback_msg,feedback_reply="")
          feedback_report.save()
          messages.success(request,"feedback Successfully  sent")
          return HttpResponseRedirect(reverse("driver_sendfeedback"))  
             
       except:
            messages.error(request,"feedback failed to be sent")
            return HttpResponseRedirect(reverse("driver_sendfeedback"))
        
        
@login_required
def   driver_apply_leave(request):
    driver_obj = SchoolDriver.objects.get(admin=request.user.id)    
    driver_leave_report =LeaveReportSchoolDriver.objects.filter(driver_id=driver_obj)    
    return render(request,"driver_template/driver_leave_template.html",{"driver_leave_report":driver_leave_report,"driver":driver_obj})


@login_required
def driver_apply_leave_save(request):
    if request.method!= "POST":
        return HttpResponseRedirect(reverse("driver_apply_leave"))
    
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")   
         
        driver_obj = SchoolDriver.objects.get(admin=request.user.id)
       
        try:            
          leave_report =LeaveReportSchoolDriver(driver_id=driver_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
          leave_report.save()
          messages.success(request,"Successfully  driver apply leave ")
          return HttpResponseRedirect(reverse("driver_apply_leave"))  
             
        except:
            messages.error(request,"failed for driver to apply for leave")
            return HttpResponseRedirect(reverse("driver_apply_leave"))
        
        

@login_required
def  driver_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    drivers = SchoolDriver.objects.get(admin=user)
    print(drivers)
    return render(request,"driver_template/driver_profile.html",{"user":user,"driver":drivers}) 
    
@csrf_exempt
@login_required
def get_students_by_route(request):
    if request.method == 'POST':
        route_id = request.POST.get('route')
        try:
            route = Route.objects.get(id=route_id)
            students = route.students.all()
            student_list = [{'id': student.id, 'name': (student.admin.first_name, student.admin.last_name)} for student in students]
            return JsonResponse(student_list, safe=False)
        except Route.DoesNotExist:
            return JsonResponse([], safe=False)

    # Handle other HTTP methods or invalid requests gracefully
    return JsonResponse([], safe=False)

@csrf_exempt
@login_required
def save_transport_attendance_data(request):
    if request.method == 'POST':
        try:
            # Extract data from the POST request
            driver = SchoolDriver.objects.get(admin=request.user)
            student_ids = request.POST.getlist('student_ids[]')
            attendance_date = request.POST.get('transport_date')
            route_id = request.POST.get('route_id')
            
            # Find the route
            route = Route.objects.get(id=route_id)
            
            # Create a new TransportationAttendance record
            attendance_record = TransportationAttendance(
                route=route,
                date=attendance_date,
                driver=driver,
            )
            attendance_record.save()

            # Add selected students to the transportation attendance record
            students = Students.objects.filter(id__in=student_ids)  # Get the selected students by their IDs            
            attendance_report_list = []
            for student in students:                
                attendance_report = TransportationAttendanceReport(
                    student=student,
                    attendance=attendance_record,
                    status=True  # You can set the status as needed
                )
                attendance_report_list.append(attendance_report)

            TransportationAttendanceReport.objects.bulk_create(attendance_report_list)

            # Debug message to ensure the code reaches this point
            print("Data saved successfully")

            # Return JSON response with "status" set to "OK"
            return JsonResponse({"status": "OK"})
        except Exception as e:
            # Debug message to print the error
            print("Error:", str(e))
            return JsonResponse({"status": "Error", "error_message": str(e)})

    # Handle other HTTP methods or invalid requests gracefully
@csrf_exempt
@login_required  # Ensure that the view is accessible only to logged-in drivers
def get_transport_attendance_data(request):
    if request.method == 'POST':
        try:
            # Get route_id, transport_date, and driver from the POST request
            route_id = request.POST.get('route_id')
            transport_date = request.POST.get('transport_date')
            driver = SchoolDriver.objects.get(admin=request.user)  # Assuming that the currently logged-in user is a driver
            
            # Debugging: Print received data
            
            
            # Retrieve the TransportationAttendance for the specified route, date, and driver
            attendance = get_object_or_404(
                TransportationAttendance,
                route__id=route_id,
                date=transport_date,
                driver=driver
            )            
            # Debugging: Print retrieved attendance object
            
            
            # Extract student attendance data
            attendance_data = []
            for attendance_report in attendance.transportationattendancereport_set.all():
                student = attendance_report.student
               
                attendance_data.append({
                    'id': student.id,
                    'name': (student.admin.first_name, student.admin.last_name),
                    'status': attendance_report.status,
                })
            print(attendance_data)
            return JsonResponse(attendance_data, safe=False)

        except Exception as e:
            # Debugging: Print any exceptions that occur
            print(f"Error: {e}")
            return JsonResponse({"status": "Error", "error_message": str(e)})

    # If the request method is not POST, return an error response
    return JsonResponse({"status": "Error", "error_message": "Invalid request method"})
        
@login_required      
def get_all_transport_dates(request):
    if request.method == 'GET':
        # Query to fetch distinct transport dates
        distinct_dates = TransportationAttendance.objects \
            .annotate(transport_date=Cast(F('date'), DateField())) \
            .values('transport_date') \
            .distinct() \
            .order_by('transport_date')

        # Extract the dates from the query result
        transport_dates = [item['transport_date'].strftime('%Y-%m-%d') for item in distinct_dates]
        
        return JsonResponse(transport_dates, safe=False)

    # Handle other HTTP methods or errors
    return JsonResponse({'error': 'Invalid request'}, status=400)       

    # Handle other HTTP methods or invalid requests gracefully
    
@login_required    
def driver_take_attendance(request):
    routes = Route.objects.all()   
    driver = SchoolDriver.objects.get(admin=request.user)  # Assuming that the currently logged-in user is a driver
    return render(request,"driver_template/driver_take_attendance.html",{"routes":routes,"driver":driver})  
  
@login_required
def driver_update_attendance(request):
    routes = Route.objects.all() 
    driver = SchoolDriver.objects.get(admin=request.user)  # Assuming that the currently logged-in user is a driver
    return render(request,"driver_template/driver_update_attendance.html",{"routes":routes,"driver":driver})

@login_required
def driver_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("driver_profile"))
    
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
          
          drivers = SchoolDriver.objects.get(admin = customuser.id)
          drivers.address = address
          drivers.save()
          messages.success(request,"profile is successfully edited")
          return HttpResponseRedirect(reverse("driver_profile"))
      
       except:
            messages.error(request,"editing  of profile  failed")
            return HttpResponseRedirect(reverse("driver_profile"))
       
@csrf_exempt
@login_required
def update_transport_attendance_data(request):
    if request.method == 'POST':
        try:
            # Get the data from the POST request
            student_ids = request.POST.get('student_ids')
            transport_date = request.POST.get('transport_date')
            route_id = request.POST.get('route_id')

            # Parse the JSON data
            student_data = json.loads(student_ids)

            # Find the TransportationAttendance object
            attendance = get_object_or_404(
                TransportationAttendance,
                route__id=route_id,
                date=transport_date,
                driver=SchoolDriver.objects.get(admin=request.user)  # Assuming the currently logged-in user is a driver
            )

            # Update attendance data
            for data in student_data:
                student_id = data['id']
                status = data['status']
                student_report, created = TransportationAttendanceReport.objects.get_or_create(
                    student_id=student_id,
                    attendance=attendance
                )
                student_report.status = status
                student_report.save()

            return JsonResponse({"status": "OK"})
        except Exception as e:
            return JsonResponse({"status": "Error", "error_message": str(e)})

    # If the request method is not POST, return an error response
    return JsonResponse({"status": "Error", "error_message": "Invalid request method"})  

@login_required
def view_driver_details(request, driver_id):
    driver = get_object_or_404(SchoolDriver.objects.select_related(
        'admin', 'medical_info', 'license_info', 'contact_info',
        'employment_info', 'vehicle_info'
    ).prefetch_related('languages_spoken', 'references'), id=driver_id)   
    context = {'driver': driver}
    return render(request, 'driver_template/details_schooldriver.html', context)

def driver_salary(request):
    # Retrieve and display the list of staff salaries for the logged-in staff
    driver_salaries = DriverSalary.objects.filter(driver_member__admin=request.user)
    context = {'driver_salaries': driver_salaries}
    return render(request, 'driver_template/manage_driver_salary_list.html', context)