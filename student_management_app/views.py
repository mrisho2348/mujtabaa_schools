from django.contrib.auth import logout,login
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from student_management_app.models import StaffRoleAssignment,Staffs,   SchoolDriver
from student_management_app.emailBackEnd import EmailBackend
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

def members(request):  
  return render(request,'myfirst.html')

def ShowLogin(request):  
  return render(request,'login.html')



def DoLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not allowed</h2>")
    else:
        user = EmailBackend.authenticate(request, request.POST.get("email"), request.POST.get("password"))
        if user is not None:
            if not user.is_active:
                messages.error(request, "Your account is not active. Please contact the administrator for support.")
                return HttpResponseRedirect(reverse("login"))

            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                staff = Staffs.objects.filter(admin=user).first()
                if staff:
                    staff_assignment = StaffRoleAssignment.objects.filter(staff=staff).first()
                    if staff_assignment and staff_assignment.role == "Accountant":
                        return HttpResponseRedirect(reverse("financial_management:accountant_home"))
                    else:
                        return HttpResponseRedirect(reverse("staff_home"))
                else:
                    messages.error(request, "No associated staff found for this user.")
                    # Handle the case where there is no associated staff for this user
                    return HttpResponseRedirect(reverse("login"))
            elif user.user_type == "3":
                return HttpResponseRedirect(reverse("student_home"))
            elif user.user_type == "4":
                return HttpResponseRedirect(reverse("driver_home"))
            else:
                return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect(reverse("login"))
    
    
def GetUserDetails(request):
  user = request.user
  if user.is_authenticated:
    return HttpResponse("User : "+user.email+" usertype : " + user.usertype)
  else:
    return HttpResponse("Please login first")   
  
  
def logout_user(request):
  logout(request)
  return HttpResponseRedirect(reverse("login"))
    
    

    
 
  
  