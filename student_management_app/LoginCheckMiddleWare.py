from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from student_management_app.models import Staffs,StaffRoleAssignment

class LoginCheckMiddleWare(MiddlewareMixin):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        
        if user.is_authenticated:
            # Allow access to library_management_app's login page
            if modulename == "library_management_app.views" and request.path == reverse("library_management_app:login-page"):
                pass
            else:
                # HOD (User Type 1)
                if user.user_type == "1":
                    # Allow specific views and static pages
                    if (modulename == "student_management_app.HodView" or
                        modulename == "student_management_app.views" or
                        modulename == "student_management_app.Delete" or
                        modulename == "django.views.static" or
                        modulename == "library_management_app.views" or
                        modulename == "financial_management.Financial" or
                        modulename == "financial_management.Invoice" or
                        modulename == "financial_management.Delete" or
                        modulename == "financial_management.Update" or                        
                        modulename == "exams.views"):
                        pass
                    # Allow access to Django admin main dashboard
                    elif request.path == reverse("admin:index"):
                        pass
                    else:
                        return HttpResponseRedirect(reverse("admin_home"))
                 
                # Staff (User Type 2)
                elif user.user_type == "2":
                    staff = Staffs.objects.filter(admin=user).first()
                    
                    if staff:
                        staff_assignment = StaffRoleAssignment.objects.filter(staff=staff).first()
                        if staff_assignment and staff_assignment.role == "Accountant":
                            if (modulename == "financial_management.views" or
                                modulename == "student_management_app.views" or
                                modulename == "financial_management.Invoice" or
                                  modulename == "financial_management.Financial"):
                                pass
                            else:    
                                return HttpResponseRedirect(reverse("financial_management:accountant_home"))
                        else:                            
                            # Allow specific views and static pages
                            if (modulename == "student_management_app.StaffView" or
                                modulename == "student_management_app.views" or
                                modulename == "django.views.static" or
                                modulename == "library_management_app.views" or
                                modulename == "financial_management.views" or
                                modulename == "financial_management.Financial" or
                                modulename == "exams.views"):
                                pass
                            else:
                                return HttpResponseRedirect(reverse("staff_home"))
                
                # Student (User Type 3)
                elif user.user_type == "3":
                    # Allow specific views and static pages
                    if (modulename == "student_management_app.StudentView" or
                        modulename == "student_management_app.views" or
                        modulename == "django.views.static" or
                        modulename == "library_management_app.views" or
                        modulename == "exams.views"):
                        pass
                    else:
                        return HttpResponseRedirect(reverse("student_home"))
                    
            # SchoolDriver (User Type 4)
                elif user.user_type == "4":
                    # Allow specific views and static pages
                    if (modulename == "student_management_app.DriverView" or
                        modulename == "student_management_app.views" or
                        modulename == "django.views.static"):
                        pass
                    else:
                        return HttpResponseRedirect(reverse("driver_home"))
            
            # SchoolSecurityPerson (User Type 5)
                elif user.user_type == "5":
                    # Allow specific views and static pages
                    if (modulename == "student_management_app.SchoolSecurityPersonView" or
                        modulename == "student_management_app.views" or
                        modulename == "django.views.static"):
                        pass
                    else:
                        return HttpResponseRedirect(reverse("school_security_person_home"))
            
            # Cooker (User Type 6)
                elif user.user_type == "6":
                # Allow specific views and static pages
                    if (modulename == "student_management_app.CookerView" or
                        modulename == "student_management_app.views" or
                        modulename == "django.views.static"):
                        pass
                    else:
                        return HttpResponseRedirect(reverse("cooker_home"))
            
                # SchoolCleaner (User Type 7)
                elif user.user_type == "7":
                # Allow specific views and static pages
                    if (modulename == "student_management_app.SchoolCleanerView" or
                        modulename == "student_management_app.views" or
                        modulename == "django.views.static"):
                        pass
                    else:
                        return HttpResponseRedirect(reverse("school_cleaner_home"))
            
                # Parent (User Type 8)
                elif user.user_type == "8":
                    # Allow specific views and static pages
                    if     (modulename == "student_management_app.ParentView" or
                        modulename == "student_management_app.views" or
                        modulename == "django.views.static"):
                        pass
                    else:
                        return HttpResponseRedirect(reverse("parent_home"))
                
                    # Rest of the user types...

                # Rest of the code for handling different user types

        else:
            # Allow specific paths during login/logout processes
            if (request.path == reverse("login") or
                request.path == reverse("DoLogin") or
                request.path == reverse("logout_user") or
                modulename == "django.contrib.auth.views"):
                pass
            else:
                return HttpResponseRedirect(reverse("login"))






# class LoginCheckMiddleWare(MiddlewareMixin):
    
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         modulename = view_func.__module__
#         user = request.user
        
#         if user.is_authenticated:
#             # HOD (User Type 1)
#             if user.user_type == "1":
#                 # Allow specific views and static pages
#                 if (modulename == "student_management_app.HodView" or
#                     modulename == "student_management_app.views" or
#                     modulename == "django.views.static" or
#                     modulename == "library_management_app.views" or
#                     modulename == "exams.views"
#                  ):
#                     pass
#                 # Allow access to Django admin main dashboard
#                 elif request.path == reverse("admin:index"):
#                     pass
                
#                 else:
#                     return HttpResponseRedirect(reverse("admin_home"))
     
            
#             # Staff (User Type 2)
#             elif user.user_type == "2":
#                 # Allow specific views and static pages
#                 if (modulename == "student_management_app.StaffView" or
#                     modulename == "student_management_app.views" or
#                     modulename == "django.views.static" or
#                     modulename == "library_management_app.views" or
#                     modulename == "exams.views"):
#                     pass
#                 else:
#                     return HttpResponseRedirect(reverse("staff_home"))
            
#             # Student (User Type 3)
#             elif user.user_type == "3":
#                 # Allow specific views and static pages
#                 if (modulename == "student_management_app.StudentView" or
#                     modulename == "student_management_app.views" or
#                     modulename == "django.views.static" or
#                     modulename == "library_management_app.views" or
#                     modulename == "exams.views"):
#                     pass
#                 else:
#                     return HttpResponseRedirect(reverse("student_home"))
            
#             # SchoolDriver (User Type 4)
#             elif user.user_type == "4":
#                 # Allow specific views and static pages
#                 if (modulename == "student_management_app.SchoolDriverView" or
#                     modulename == "student_management_app.views" or
#                     modulename == "django.views.static"):
#                     pass
#                 else:
#                     return HttpResponseRedirect(reverse("school_driver_home"))
            
#             # SchoolSecurityPerson (User Type 5)
#             elif user.user_type == "5":
#                 # Allow specific views and static pages
#                 if (modulename == "student_management_app.SchoolSecurityPersonView" or
#                     modulename == "student_management_app.views" or
#                     modulename == "django.views.static"):
#                     pass
#                 else:
#                     return HttpResponseRedirect(reverse("school_security_person_home"))
            
#             # Cooker (User Type 6)
#             elif user.user_type == "6":
#                 # Allow specific views and static pages
#                 if (modulename == "student_management_app.CookerView" or
#                     modulename == "student_management_app.views" or
#                     modulename == "django.views.static"):
#                     pass
#                 else:
#                     return HttpResponseRedirect(reverse("cooker_home"))
            
#             # SchoolCleaner (User Type 7)
#             elif user.user_type == "7":
#                 # Allow specific views and static pages
#                 if (modulename == "student_management_app.SchoolCleanerView" or
#                     modulename == "student_management_app.views" or
#                     modulename == "django.views.static"):
#                     pass
#                 else:
#                     return HttpResponseRedirect(reverse("school_cleaner_home"))
            
#             # Parent (User Type 8)
#             elif user.user_type == "8":
#                 # Allow specific views and static pages
#                 if (modulename == "student_management_app.ParentView" or
#                     modulename == "student_management_app.views" or
#                     modulename == "django.views.static"):
#                     pass
#                 else:
#                     return HttpResponseRedirect(reverse("parent_home"))
            
#             # Invalid user type
#             else:
#                 return HttpResponseRedirect(reverse("login"))
#         else:
#             # Allow specific paths during login/logout processes
#             if (request.path == reverse("login") or
#                 request.path == reverse("DoLogin") or
#                 request.path == reverse("logout_user") or
#                 modulename == "django.contrib.auth.views"):
#                 pass
#             else:
#                 return HttpResponseRedirect(reverse("login"))
