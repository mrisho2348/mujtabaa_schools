"""
URL configuration for taboracollage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from taboracollage import settings
from student_management_app import StudentView, views,HodView,StaffView

urlpatterns = [
    path('', views.ShowLogin, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),   
    path('admin/', admin.site.urls),
    path('library_management_app/', include(('library_management_app.urls', 'library_management_app'), namespace='library_management_app')),
    path('exams/', include(('exams.urls', 'exams'), namespace='exams')),
    path('financial/', include('financial_management.urls')),
    path('GetUserDetails', views.GetUserDetails, name='GetUserDetails'),
    path('dologin', views.DoLogin, name='DoLogin'),
    path('admin_home', HodView.admin_home, name='admin_home'),   
    path('add_staff', HodView.add_staff, name='addstaff'),
    path('driver-form', HodView.driver_form_view, name='driver_form'),
    path('manage_driver', HodView.manage_driver, name='manage_driver'),
    path('view_driver_info/<int:driver_id>/', HodView.view_driver_info, name='view_driver_info'),
    path('update_driver_info/<int:driver_id>/', HodView.update_driver_info, name='update_driver_info'),
    
      # Other URLs for your app...

    # URL for the view to add driver information
    path('add_driver_info/', HodView.add_driver_info_save, name='add_driver_info'),
    path('updating_driver_info_save/<int:driver_id>/', HodView.updating_driver_info_save, name='updating_driver_info_save'),

    # URL for the view to add driver medical information
    path('add_driver_medical_info/<int:driver_id>/', HodView.add_driver_medical_info, name='add_driver_medical_info'),

    # URL for the view to add driver license information
    path('add_driver_license_info/<int:driver_id>/', HodView.add_driver_license_info, name='add_driver_license_info'),

    # URL for the view to add driver contact information
    path('add_driver_contact_info/<int:driver_id>/', HodView.add_driver_contact_info, name='add_driver_contact_info'),

    # URL for the view to add driver emergency contact information
    path('add_driver_emergency_contact_info/<int:driver_id>/', HodView.add_driver_emergency_contact_info, name='add_driver_emergency_contact_info'),

    # URL for the view to add driver employment information
    path('add_driver_employment_info/<int:driver_id>/', HodView.add_driver_employment_info, name='add_driver_employment_info'),

    # URL for the view to add driver vehicle information
    path('add_driver_vehicle_info/<int:driver_id>/', HodView.add_driver_vehicle_info, name='add_driver_vehicle_info'),

    # URL for the view to add driver languages spoken
    path('add_driver_languages/<int:driver_id>/', HodView.add_driver_languages, name='add_driver_languages'),

    # URL for the view to add driver references
    path('add_driver_references/<int:driver_id>/', HodView.add_driver_references, name='add_driver_references'),
    path('add_security_person/', HodView.add_security_person, name='add_security_person'),
    path('add_cooker/', HodView.add_cooker, name='add_cooker'),
    path('update_cooker_info_save/<int:cooker_id>/', HodView.update_cooker_info_save, name='update_cooker_info_save'),
    path('update_cleaner_info_save/<int:cleaner_id>/', HodView.update_cleaner_info_save, name='update_cleaner_info_save'),
    path('update_cooker_info/<int:cooker_id>/', HodView.update_cooker_info, name='update_cooker_info'),
    path('update_cleaner_info/<int:cleaner_id>/', HodView.update_cleaner_info, name='update_cleaner_info'),
    path('add_schoolcleaner/', HodView.add_schoolcleaner, name='add_schoolcleaner'),
    path('add_staff_save', HodView.add_staff_save, name='add_staff_save'),   
    path('add_security_person_info_save/', HodView.add_security_person_info_save, name='add_security_person_info_save'),
    path('manage_security/', HodView.manage_security, name='manage_security'),
    path('view_security_info/<int:security_id>/', HodView.view_security_info, name='view_security_info'),
    path('update_security_info/<int:security_id>/', HodView.update_security_info, name='update_security_info'),
    path('update_security_info_save/<int:security_id>/', HodView.update_security_info_save, name='update_security_info_save'),
    path('manage_security/', HodView.manage_security, name='manage_security'),
    path('add_cooker_info/', HodView.add_cooker_info_save, name='add_cooker_info'),
    path('manage_cooker/', HodView.manage_cooker, name='manage_cooker'),
    path('manage_cleaner/', HodView.manage_cleaner, name='manage_cleaner'),
    path('view_cooker_info/<int:cooker_id>/', HodView.view_cooker_info, name='view_cooker_info'),
    path('view_cleaner_info/<int:cleaner_id>/', HodView.view_cleaner_info, name='view_cleaner_info'),
    path('add_schoolcleaner_info/', HodView.add_schoolcleaner_info_save, name='add_schoolcleaner_info'), 
    path('add_car_view/', HodView.add_car_save, name='add_car_view'),
    path('add_schoolcar_view/', HodView.add_schoolcar_view, name='add_schoolcar_view'),
    path('add_schoolclassroom/', HodView.add_schoolclassroom, name='add_schoolclassroom'),    
    path('delete_classroom/<int:classroom_id>/', HodView.delete_classroom, name='delete_classroom'),
    path('classroom_detail/<int:classroom_id>/', HodView.classroom_detail, name='classroom_detail'),
    path('classroom/update/<int:classroom_id>/', HodView.update_classroom, name='update_classroom'),
    path('update_classroom_save/<int:classroom_id>/', HodView.update_classroom_save, name='update_classroom_save_with_id'),
    path('api/update_classroom_status/<int:classroom_id>/', HodView.update_classroom_status, name='update_classroom_status'),
    path('manage_classroom/', HodView.manage_classroom, name='manage_classroom'),
    path('add_classroom_view/', HodView.add_classroom_save, name='add_classroom'),
    # Add more URLs for other views if needed
    path('add_student', HodView.add_student, name='add_student'),   
    path('add_student_save', HodView.add_student_save, name='add_student_save'),    
    path('add_subject', HodView.add_subject, name='addsubject'),   
    path('add_subject_save', HodView.add_subject_save, name='addsubjectsave'),    
    path('manage_staff', HodView.manage_staff, name='manage_staff'),   
    path('manage_student', HodView.manage_student, name='manage_student'),   
    path('qualification_form/<int:staff_id>/', HodView.qualifications_form, name='qualification_form'),
    path('skills_form/<int:staff_id>/', HodView.skills_form, name='skills_form'),
    path('employment_history_form/<int:staff_id>/', HodView.employment_history_form, name='employment_history_form'),
    path('references_form/<int:staff_id>/', HodView.references_form, name='references_form'),
    path('student-results/<str:exam_type_id>/<str:current_class>/', HodView.student_results, name='student_results'),
    path('subject-wise-results/<int:student_id>/<int:exam_type_id>/', HodView.subject_wise_result, name='subject_wise_result'),
    path('manage_subject', HodView.manage_subject, name='manage_subject'),  
     
    path('edit_staff/<str:staff_id>', HodView.edit_staff, name='edit_staff'),   
    path('edit_staff_qualification/<str:staff_id>', HodView.edit_staff_qualification, name='edit_staff_qualification'),   
    path('edit_staff_skill/<str:staff_id>', HodView.edit_staff_skill, name='edit_staff_skill'),   
    path('edit_staff_employment_history/<str:staff_id>', HodView.edit_staff_employment_history, name='edit_staff_employment_history'),   
    path('edit_staff_reference/<str:staff_id>', HodView.edit_staff_reference, name='edit_staff_reference'),   
    path('edit_staff_save', HodView.edit_staff_save, name='edit_staff_save'),      
    path('edit_student/<str:student_id>', HodView.edit_student, name='edit_student'),   
    path('edit_parents/<str:parent_id>', HodView.edit_parents, name='edit_parents'),   
    path('edit_student_save', HodView.edit_student_save, name='edit_student_save'),   
    path('add_parents', HodView.add_parents, name='add_parents'),   
    path('save_parent', HodView.save_parent, name='save_parent'),   
    path('manage_parent', HodView.manage_parent, name='manage_parent'),       
    path('update_parent/<int:parent_id>/', HodView.update_parent, name='update_parent'),
    # time table 
    path('students-summary/<str:exam_type>/', HodView.students_summary, name='students_summary'), 
    path('primery_table', HodView.primery_table, name='primery_table'),
    path('secondary_timetable', HodView.secondary_timetable, name='secondary_timetable'),

 
  
    path('edit_subject/<str:subject_id>', HodView.edit_subject, name='edit_subject'),   
    path('edit_subject/<int:subject_id>/', HodView.create_or_edit_subject, name='create_or_edit_subject'),
    path('subject/<int:subject_id>/', HodView.subject_details, name='subject_details'),
    path('add_session/', HodView.add_session, name='add_session'),
    path('add_session_save/', HodView.add_session_save, name='add_session_save'),
    path('edit_session/<int:session_id>/', HodView.edit_session, name='edit_session'),
    path('edit_session_save/<int:session_id>/', HodView.edit_session_save, name='edit_session_save'),
    path('manage_session/', HodView.manage_session, name='manage_session'),
    path('delete_session/<int:session_id>/', HodView.delete_session, name='delete_session'),
    path('check_email_exist', HodView.check_email_exist, name='check_email_exist'),
    path('check_username_exist', HodView.check_username_exist, name='check_username_exist'),
    path('student_feedback_message', HodView.student_feedback_message, name='student_feedback_message'),
    path('student_feedback_message_replied', HodView.student_feedback_message_replied, name='student_feedback_message_replied'),
    path('staff_feedback_message_replied', HodView.staff_feedback_message_replied, name='staff_feedback_message_replied'),
    path('staff_feedback_message', HodView.staff_feedback_message, name='staff_feedback_message'),
    path('student_leave_view', HodView.student_leave_view, name='student_leave_view'),  
    path('staff_leave_view', HodView.staff_leave_view, name='staff_leave_view'), 
    path('student_approve_leave/<str:leave_id>', HodView.student_approve_leave, name='student_approve_leave'),  
    path('student_disapprove_leave/<str:leave_id>', HodView.student_disapprove_leave, name='student_disapprove_leave'), 
    path('staff_approve_leave/<str:leave_id>', HodView.staff_approve_leave, name='staff_approve_leave'), 
    path('staff_disapprove_leave/<str:leave_id>', HodView.staff_disapprove_leave, name='staff_disapprove_leave'), 
    path('admin_view_attendance', HodView.admin_view_attendance, name='admin_view_attendance'), 
    path('admin_get_student_attendance', HodView.admin_get_student_attendance, name='admin_get_student_attendance'), 
    path('admin_get_attendance_date', HodView.admin_get_attendance_date, name='admin_get_attendance_date'), 
    path('admin_save_updateattendance', HodView.admin_save_updateattendance, name='admin_save_updateattendance'), 
    path('admin_profile', HodView.admin_profile, name='admin_profile'), 
    path('edit_profile_save', HodView.edit_profile_save, name='edit_profile_save'), 
    path('single_student_detail/<int:student_id>/', HodView.single_student_detail, name='single_student_detail'),
    path('single_parent_detail/<str:parent_id>', HodView.single_parent_detail, name='single_parent_detail'),
    path('staff_detail/<int:staff_id>/', HodView.single_staff_detail, name='single_staff_detail'), 
    path('students', HodView.student_list, name='student-list'), 
    path('get_class_choices', HodView.get_class_choices, name='get_class_choices'),  
    path('exam-types/edit/<int:exam_type_id>/', HodView.exam_type_form, name='exam-type-form'),
    path('exam-types/', HodView.exam_type_form, name='exam-type-form'),
    path('exam-types-list/', HodView.exam_type_list, name='exam_type_list'),
    # staff url paths  
    path('staff_home', StaffView.staff_home, name='staff_home'),  
    path('staff_take_attendance', StaffView.staff_take_attendance, name='staff_take_attendance'),  
    path('get_students', StaffView.get_students, name='get_students'),  
    path('save_attendance_data', StaffView.save_attendance_data, name='save_attendance_data'),  
    path('get_attendance_date', StaffView.get_attendance_date, name='get_attendance_date'),  
    path('get_student_attendance', StaffView.get_student_attendance, name='get_student_attendance'),  
    path('staff_update_attendance', StaffView.staff_update_attendance, name='staff_update_attendance'),  
    path('save_updateattendance', StaffView.save_updateattendance, name='save_updateattendance'),  
    path('staff_apply_leave', StaffView.staff_apply_leave, name='staff_apply_leave'),  
    path('staff_apply_leave_save', StaffView.staff_apply_leave_save, name='staff_apply_leave_save'),  
    path('staff_sendfeedback', StaffView.staff_sendfeedback, name='staff_sendfeedback'),  
    path('staff_sendfeedback_save', StaffView.staff_sendfeedback_save, name='staff_sendfeedback_save'),  
    path('staff_profile', StaffView.staff_profile, name='staff_profile'),  
    path('staff_profile_save', StaffView.staff_profile_save, name='staff_profile_save'), 
    path('update-students-results/<int:result_id>/<int:student_id>/<int:exam_type_id>/',StaffView.update_students_results,name='update_students_results'),
    path('student/<int:student_id>/<int:exam_type_id>/', StaffView.student_details, name='student_details'),    
    path('subject-wise-result/<int:student_id>/<int:exam_type_id>/', StaffView.subject_wise_results, name='subject_wise_results'),    
    path('assign-results/<int:student_id>/<int:exam_type_id>/', StaffView.assign_results, name='assign_results'),    
    
    path('assign_resutls_save', StaffView.assign_results_save, name='assign_resutls_save'), 
    path('students-summary-staff/<str:exam_type>/', StaffView.students_summary_staff, name='students_summary_staff'), 
    path('form-i-students/<int:exam_type_id>/<str:current_class>/', StaffView.form_i_students, name='form_i_students'),

     
    # student url paths  
    path('student_home', StudentView.student_home, name='student_home'),       
    path('student_view_attendance', StudentView.student_view_attendance, name='student_view_attendance'),       
    path('student_view_attendance_post', StudentView.student_view_attendance_post, name='student_view_attendance_post'), 
    path('student-subject-wise-result/<str:exam_type>/', StudentView.student_subject_wise_result, name='student_subject_wise_result'),  
    path('student_apply_leave', StudentView.student_apply_leave, name='student_apply_leave'),  
    path('student_apply_leave_save', StudentView.student_apply_leave_save, name='student_apply_leave_save'),  
    path('student_sendfeedback', StudentView.student_sendfeedback, name='student_sendfeedback'),  
    path('student_sendfeedback_save', StudentView.student_sendfeedback_save, name='student_sendfeedback_save'),    
    path('student_profile', StudentView.student_profile, name='student_profile'),    
    path('student_profile_save', StudentView.student_profile_save, name='student_profile_save'),    
    path('logout_user', views.logout_user, name='logout_user'),  # Move this line here
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)