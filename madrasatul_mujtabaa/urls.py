"""
URL configuration for madrasatul_mujtabaa project.

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
from madrasatul_mujtabaa import settings
from django.views.generic import RedirectView
from student_management_app import StudentView, views,HodView,StaffView,DriverView,Delete,Activate,Secretary

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login', views.ShowLogin, name='login'), 
    path('contact/', views.ContactFormView.as_view(), name='contact_form'),
    
    path('accounts/', include('django.contrib.auth.urls')),   
    path('admin/', admin.site.urls),
    path('library_management_app/', include(('library_management_app.urls', 'library_management_app'), namespace='library_management_app')),
    path('financial_management/', include(('financial_management.urls', 'financial_management'), namespace='financial_management')),
    path('exams/', include(('exams.urls', 'exams'), namespace='exams')),    
    path('GetUserDetails', views.GetUserDetails, name='GetUserDetails'),
    path('dologin', views.DoLogin, name='DoLogin'),
    path('admin_home', HodView.admin_home, name='admin_home'),   
    path('driver-form', HodView.driver_form_view, name='driver_form'),
    path('view_driver_info/<int:driver_id>/', HodView.view_driver_info, name='view_driver_info'),
    path('update_driver_info/<int:driver_id>/', HodView.update_driver_info, name='update_driver_info'),
    path('staff_role_list/', HodView.staff_role_list, name='staff_role_list'),
    path('render_staff_role_assignment_form/', HodView.render_staff_role_assignment_form, name='render_staff_role_assignment_form'),
    path('delete_staff_role/<int:assignment_id>/', HodView.delete_staff_role, name='delete_staff_role'),  
    path('updating_driver_info_save/<int:driver_id>/', HodView.updating_driver_info_save, name='updating_driver_info_save'),
    path('update_cooker_info_save/<int:cooker_id>/', HodView.update_cooker_info_save, name='update_cooker_info_save'),
    path('update_cleaner_info_save/<int:cleaner_id>/', HodView.update_cleaner_info_save, name='update_cleaner_info_save'),
    path('update_cooker_info/<int:cooker_id>/', HodView.update_cooker_info, name='update_cooker_info'),
    path('update_cleaner_info/<int:cleaner_id>/', HodView.update_cleaner_info, name='update_cleaner_info'),
    path('view_security_info/<int:security_id>/', HodView.view_security_info, name='view_security_info'),
    path('update_security_info/<int:security_id>/', HodView.update_security_info, name='update_security_info'),
    path('update_security_info_save/<int:security_id>/', HodView.update_security_info_save, name='update_security_info_save'),
    path('view_cooker_info/<int:cooker_id>/', HodView.view_cooker_info, name='view_cooker_info'),
    path('view_cleaner_info/<int:cleaner_id>/', HodView.view_cleaner_info, name='view_cleaner_info'),   
    path('cars/', HodView.car_list, name='car_list'),
    path('delete_car/<int:car_id>/', HodView.delete_car, name='delete_car'),
    path('delete_classroom/<int:classroom_id>/', HodView.delete_classroom, name='delete_classroom'),
    path('classroom_detail/<int:classroom_id>/', HodView.classroom_detail, name='classroom_detail'),
    path('classroom/update/<int:classroom_id>/', HodView.update_classroom, name='update_classroom'),
    path('update_classroom_save/<int:classroom_id>/', HodView.update_classroom_save, name='update_classroom_save_with_id'),
    path('api/update_classroom_status/<int:classroom_id>/', HodView.update_classroom_status, name='update_classroom_status'),  
    path('delete_route/<int:route_id>/', HodView.delete_route, name='delete_route'),
    path('route_list/', HodView.route_list, name='route_list'),
    
    path('admin_view_transport_attendance/', HodView.admin_view_transport_attendance, name='admin_view_transport_attendance'),
    path('admin_get_transport_dates/', HodView.admin_get_transport_dates, name='admin_get_transport_dates'),
    path('admin_get_transport_attendance/', HodView.admin_get_transport_attendance, name='admin_get_transport_attendance'),
    # Add more URLs for other views if needed
  
    path('student-reports/', HodView.student_reports, name='student_reports'),  
    path('filter_students/', HodView.filter_students, name='filter_students'),  
    path('qualification_form/<int:staff_id>/', HodView.qualifications_form, name='qualification_form'),
    path('skills_form/<int:staff_id>/', HodView.skills_form, name='skills_form'),
    path('employment_history_form/<int:staff_id>/', HodView.employment_history_form, name='employment_history_form'),
    path('references_form/<int:staff_id>/', HodView.references_form, name='references_form'),
    path('student-results/<str:exam_type_id>/<str:current_class>/', HodView.student_results, name='student_results'),
    path('subject-wise-results/<int:student_id>/<int:exam_type_id>/', HodView.subject_wise_result, name='subject_wise_result'),  
    path('save_parent', HodView.save_parent, name='save_parent'),  
    path('update_parent/<int:parent_id>/', HodView.update_parent, name='update_parent'),
    # time table 
    path('students-summary/<str:exam_type>/', HodView.students_summary, name='students_summary'), 
    path('primery_table', HodView.primery_table, name='primery_table'),
    path('secondary_timetable', HodView.secondary_timetable, name='secondary_timetable'), 
    path('subject/<int:subject_id>/', HodView.subject_details, name='subject_details'), 
    path('delete_session/<int:session_id>/', HodView.delete_session, name='delete_session'),
    path('check_email_exist', HodView.check_email_exist, name='check_email_exist'),
    path('check_username_exist', HodView.check_username_exist, name='check_username_exist'),
    path('student_feedback_message', HodView.student_feedback_message, name='student_feedback_message'),
    path('driver_feedback_message', HodView.driver_feedback_message, name='driver_feedback_message'),
    path('student_feedback_message_replied', HodView.student_feedback_message_replied, name='student_feedback_message_replied'),
    path('driver_feedback_message_replied', HodView.driver_feedback_message_replied, name='driver_feedback_message_replied'),
    path('staff_feedback_message_replied', HodView.staff_feedback_message_replied, name='staff_feedback_message_replied'),
    path('staff_feedback_message', HodView.staff_feedback_message, name='staff_feedback_message'),
    path('student_leave_view', HodView.student_leave_view, name='student_leave_view'),  
    path('driver_leave_view', HodView.driver_leave_view, name='driver_leave_view'),  
    path('staff_leave_view', HodView.staff_leave_view, name='staff_leave_view'), 
    path('student_approve_leave/<str:leave_id>', HodView.student_approve_leave, name='student_approve_leave'),  
    path('driver_approve_leave/<str:leave_id>', HodView.driver_approve_leave, name='driver_approve_leave'),  
    path('student_disapprove_leave/<str:leave_id>', HodView.student_disapprove_leave, name='student_disapprove_leave'), 
    path('driver_disapprove_leave/<str:leave_id>', HodView.driver_disapprove_leave, name='driver_disapprove_leave'), 
    path('staff_approve_leave/<str:leave_id>', HodView.staff_approve_leave, name='staff_approve_leave'), 
    path('staff_disapprove_leave/<str:leave_id>', HodView.staff_disapprove_leave, name='staff_disapprove_leave'), 
    path('admin_view_attendance', HodView.admin_view_attendance, name='admin_view_attendance'), 
    path('admin_get_student_attendance', HodView.admin_get_student_attendance, name='admin_get_student_attendance'), 
    path('admin_get_attendance_date', HodView.admin_get_attendance_date, name='admin_get_attendance_date'), 
    path('admin_save_updateattendance', HodView.admin_save_updateattendance, name='admin_save_updateattendance'),
    path('get_subjects_by_education_level', HodView.get_subjects_by_education_level, name='get_subjects_by_education_level'),
    path('get_subject_by_education_level/', HodView.get_subject_by_education_level, name='get_subject_by_education_level'),
    path('admin_profile', HodView.admin_profile, name='admin_profile'),     
    path('single_student_detail/<int:student_id>/', HodView.single_student_detail, name='single_student_detail'),
    path('single_parent_detail/<str:parent_id>', HodView.single_parent_detail, name='single_parent_detail'),
    path('staff_detail/<int:staff_id>/', HodView.single_staff_detail, name='single_staff_detail'), 
    path('students', HodView.student_list, name='student-list'), 
    path('get_class_choices', HodView.get_class_choices, name='get_class_choices'),      
    path('exam-types/', HodView.exam_type_form, name='exam-type-form'),
    
    
    # add
    path('add_driver_contact_info/<int:driver_id>/', HodView.add_driver_contact_info, name='add_driver_contact_info'),
    path('add_session/', HodView.add_session, name='add_session'),
    path('datatables/', HodView.datatables, name='datatables'),
    path('add_session_save/', HodView.add_session_save, name='add_session_save'),
    path('add_parents', HodView.add_parents, name='add_parents'), 
    path('add_student', HodView.add_student, name='add_student'),   
    path('add_student_save', HodView.add_student_save, name='add_student_save'),    
    path('add_subject', HodView.add_subject, name='addsubject'),   
    path('add_subject_save', HodView.add_subject_save, name='addsubjectsave'),
    path('add_cooker_info/', HodView.add_cooker_info_save, name='add_cooker_info'),  
    path('add_route/', HodView.add_route, name='add_route'), 
    path('add_staff', HodView.add_staff, name='addstaff'),
    path('add_driver_info/', HodView.add_driver_info_save, name='add_driver_info'),
    path('add_driver_medical_info/<int:driver_id>/', HodView.add_driver_medical_info, name='add_driver_medical_info'),
    path('add_driver_license_info/<int:driver_id>/', HodView.add_driver_license_info, name='add_driver_license_info'),
    path('add_driver_emergency_contact_info/<int:driver_id>/', HodView.add_driver_emergency_contact_info, name='add_driver_emergency_contact_info'),
    path('add_driver_employment_info/<int:driver_id>/', HodView.add_driver_employment_info, name='add_driver_employment_info'),
    path('add_driver_vehicle_info/<int:driver_id>/', HodView.add_driver_vehicle_info, name='add_driver_vehicle_info'),
    path('add_driver_languages/<int:driver_id>/', HodView.add_driver_languages, name='add_driver_languages'),
    path('add_driver_references/<int:driver_id>/', HodView.add_driver_references, name='add_driver_references'),
    path('add_security_person/', HodView.add_security_person, name='add_security_person'),
    path('add_cooker/', HodView.add_cooker, name='add_cooker'),
    path('add_schoolcleaner/', HodView.add_schoolcleaner, name='add_schoolcleaner'),
    path('add_staff_save', HodView.add_staff_save, name='add_staff_save'),   
    path('add_security_person_info_save/', HodView.add_security_person_info_save, name='add_security_person_info_save'),
    path('add_schoolcleaner_info/', HodView.add_schoolcleaner_info_save, name='add_schoolcleaner_info'),
    path('add_car_view/', HodView.add_car_save, name='add_car_view'),
    path('add_schoolcar_view/', HodView.add_schoolcar_view, name='add_schoolcar_view'),
    path('add_schoolclassroom/', HodView.add_schoolclassroom, name='add_schoolclassroom'),
    path('add_classroom_view/', HodView.add_classroom_save, name='add_classroom'),
    path('get_class_levels/', HodView.get_class_levels, name='get_class_levels'),  
    
    # edit url view 
    path('edit_staff_role/<int:assignment_id>/', HodView.edit_staff_role, name='edit_staff_role'),
    path('edit_car/<int:car_id>/', HodView.edit_car, name='edit_car'),
    path('edit_or_add_route/', HodView.edit_or_add_route, name='edit_or_add_route'),
    path('edit_or_add_route/<int:route_id>/', HodView.edit_or_add_route, name='edit_or_add_route'),
    path('edit_staff/<str:staff_id>', HodView.edit_staff, name='edit_staff'),   
    path('edit_staff_qualification/<str:staff_id>', HodView.edit_staff_qualification, name='edit_staff_qualification'),   
    path('edit_staff_skill/<str:staff_id>', HodView.edit_staff_skill, name='edit_staff_skill'),   
    path('edit_staff_employment_history/<str:staff_id>', HodView.edit_staff_employment_history, name='edit_staff_employment_history'),   
    path('edit_staff_reference/<str:staff_id>', HodView.edit_staff_reference, name='edit_staff_reference'),   
    path('edit_staff_save', HodView.edit_staff_save, name='edit_staff_save'),      
    path('edit_student/<str:student_id>', HodView.edit_student, name='edit_student'),   
    path('edit_parents/<str:parent_id>', HodView.edit_parents, name='edit_parents'),   
    path('edit_student_save', HodView.edit_student_save, name='edit_student_save'), 
    path('edit_subject/<str:subject_id>', HodView.edit_subject, name='edit_subject'),   
    path('edit_subject/<int:subject_id>/', HodView.create_or_edit_subject, name='create_or_edit_subject'),
    path('edit_session/<int:session_id>/', HodView.edit_session, name='edit_session'),
    path('edit_session_save/<int:session_id>/', HodView.edit_session_save, name='edit_session_save'),
    path('edit_profile_save', HodView.edit_profile_save, name='edit_profile_save'), 
    path('exam-types/edit/<int:exam_type_id>/', HodView.exam_type_form, name='exam-type-form'),
    
    
    path('add_class_level/', HodView.add_class_level, name='add_class_level'),
    path('manage-class-level/', HodView.manage_class_level, name='manage_class_level'),      
    path('add_class-level-save/', HodView.add_class_level_save, name='add_class_level_save'),      
    path('edit_class_level_save/<int:class_level_id>/', HodView.edit_class_level_save, name='edit_class_level_save'),
    path('edit_class_level/<int:class_level_id>/', HodView.edit_class_level, name='edit_class_level'),
    path('delete_class_level/<int:class_level_id>/', HodView.delete_class_level, name='delete_class_level'),

    
    path('add_school', HodView.add_school, name='add_school'),   
    path('add_school_save', HodView.add_school_save, name='add_school_save'),   
    path('manage_school_save', HodView.manage_school_save, name='manage_school_save'), 
    path('edit_school/<int:school_id>/', HodView.edit_school, name='edit_school'),
    path('delete_school/<int:school_id>/', HodView.delete_school, name='delete_school'),
    
    path('add_education_level', HodView.add_education_level, name='add_education_level'),   
    path('add_education_level_save', HodView.add_education_level_save, name='add_education_level_save'),   
    path('manage_education_level', HodView.manage_education_level, name='manage_education_level'), 
    path('edit_education_level/<int:education_level_id>/', HodView.edit_education_level, name='edit_education_level'),
    path('delete_education_level/<int:education_level_id>/', HodView.delete_education_level, name='delete_education_level'),
    path('confirm_delete_education_level/<int:education_level_id>/', HodView.confirm_delete_education_level, name='confirm_delete_education_level'),
    
    # manage
    path('manage_security/', HodView.manage_security, name='manage_security'),    
    path('manage_cooker/', HodView.manage_cooker, name='manage_cooker'),
    path('manage_cleaner/', HodView.manage_cleaner, name='manage_cleaner'),
    path('manage_session/', HodView.manage_session, name='manage_session'),
    path('manage_parent', HodView.manage_parent, name='manage_parent'),  
    path('manage_staff', HodView.manage_staff, name='manage_staff'),   
    path('manage_student', HodView.manage_student, name='manage_student'), 
    path('manage_subject', HodView.manage_subject, name='manage_subject'),  
    path('manage_classroom/', HodView.manage_classroom, name='manage_classroom'),
    path('manage_driver', HodView.manage_driver, name='manage_driver'),
    path('exam-types-list/', HodView.exam_type_list, name='exam_type_list'),
    # activation

    path('update_user_status', Activate.update_user_status, name='update_user_status'),
    path('update_cooker_status', Activate.update_cooker_status, name='update_cooker_status'),
    path('update_cleaner_status', Activate.update_cleaner_status, name='update_cleaner_status'),
    path('update_security_status', Activate.update_security_status, name='update_security_status'),
    path('update_parent_status', Activate.update_parent_status, name='update_parent_status'),
    path('update_staff_status', Activate.update_staff_status, name='update_staff_status'),
    path('update_student_status', Activate.update_student_status, name='update_student_status'),
    path('update_classroom_status', Activate.update_classroom_status, name='update_classroom_status'),
    
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
    path('staff_detail', StaffView.staff_detail, name='staff_detail'),  
    path('staff_profile', StaffView.staff_profile, name='staff_profile'),  
    path('staff_salary', StaffView.staff_salary, name='staff_salary'),  
    path('manage_notes/', StaffView.manage_notes, name='manage_notes'),
    path('add_notes/', StaffView.add_notes, name='add_notes'),
    path('edit_notes/<int:note_id>/', StaffView.edit_notes, name='edit_notes'),

   
    path('download_notes/<int:note_id>/', StaffView.download_notes, name='download_notes'),    
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
    path('student_payments_record', StudentView.student_payments_record, name='student_payments_record'),  
    path('student_sendfeedback', StudentView.student_sendfeedback, name='student_sendfeedback'),  
    path('student_sendfeedback_save', StudentView.student_sendfeedback_save, name='student_sendfeedback_save'),    
    path('student_profile', StudentView.student_profile, name='student_profile'),    
    path('student_profile_save', StudentView.student_profile_save, name='student_profile_save'), 
    path('single_student_details', StudentView.single_student_details, name='single_student_details'),   
    path('student_notes', StudentView.student_notes, name='student_notes'), 
    path('student_invoice_list', StudentView.student_invoice_list, name='student_invoice_list'), 
    path('student_transport_attendance_post/', StudentView.student_transport_attendance_post, name='student_transport_attendance_post'),  
    path('student_view_transport_attendance/', StudentView.student_view_transport_attendance, name='student_view_transport_attendance'),  
    path('logout_user', views.logout_user, name='logout_user'),  # Move this line here
    
    # driver url pattern
    path('driver_home', DriverView.driver_home, name='driver_home'),  
    path('driver_salary', DriverView.driver_salary, name='driver_salary'),  
    path('driver_take_attendance', DriverView.driver_take_attendance, name='driver_take_attendance'),  
    path('get-students-by-route', DriverView.get_students_by_route, name='get_students_by_route'),  
    path('save-transport-attendance-data', DriverView.save_transport_attendance_data, name='save_transport_attendance_data'),  
    path('get-transport-attendance-data', DriverView.get_transport_attendance_data, name='get_transport_attendance_data'),  
    path('get_all_transport_dates/', DriverView.get_all_transport_dates, name='get_all_transport_dates'),
    # path('get_student_attendance', DriverView.get_student_attendance, name='get_student_attendance'),  
    path('driver_update_attendance', DriverView.driver_update_attendance, name='driver_update_attendance'),  
    # path('save_updateattendance', DriverView.save_updateattendance, name='save_updateattendance'),  
    path('driver_apply_leave', DriverView.driver_apply_leave, name='driver_apply_leave'),  
    path('driver_apply_leave_save', DriverView.driver_apply_leave_save, name='driver_apply_leave_save'),  
    path('driver_sendfeedback', DriverView.driver_sendfeedback, name='driver_sendfeedback'),  
    path('driver_sendfeedback_save', DriverView.driver_sendfeedback_save, name='driver_sendfeedback_save'),  
    path('driver_profile', DriverView.driver_profile, name='driver_profile'),  
    path('driver_profile_save', DriverView.driver_profile_save, name='driver_profile_save'), 
    path('update-transport-attendance/', DriverView.update_transport_attendance_data, name='update_transport_attendance_data'),
    path('view_driver_details/<int:driver_id>/', DriverView.view_driver_details, name='view_driver_details'),
    
    path('secretary-home/dashboard', Secretary.secretary_home, name='secretary_home'),
    path('secretary/add_parents', Secretary.add_parents, name='secretary_add_parents'), 
    path('secretary/add_student', Secretary.add_student, name='secretary_add_student'),
    path('secretary/save_parent', Secretary.save_parent, name='secretary_save_parent'),  
    path('secretary/update_parent/<int:parent_id>/', Secretary.update_parent, name='secretary_update_parent'),   
    path('secretary/add_student_save', Secretary.add_student_save, name='secretary_add_student_save'),
    path('secretary/edit_student/<str:student_id>', Secretary.edit_student, name='secretary_edit_student'),   
    path('secretary/edit_parents/<str:parent_id>', Secretary.edit_parents, name='secretary_edit_parents'),   
    path('secretary/edit_student_save', Secretary.edit_student_save, name='secretary_edit_student_save'),  
    path('secretary/manage_parent', Secretary.manage_parent, name='secretary_manage_parent'),  
    path('secretary/manage_student', Secretary.manage_student, name='secretary_manage_student'), 
    path('secretary/generate_invoice/<int:payment_id>/', Secretary.generate_invoice, name='secretary_generate_invoice'),
    path('secretary/edit_income_payment/<int:income_payment_id>/', Secretary.edit_income_payment, name='secretary_edit_income_payment'),
    path('secretary/invoice_list/', Secretary.invoice_list, name='secretary_invoice_list'),
    path('secretary/delete_income_payment/<int:payment_id>/', Secretary.delete_income_payment, name='secretary_delete_income_payment'),
    path('secretary/income_payment_list/', Secretary.income_payment_list, name='secretary_income_payment_list'),
    path('secretary/income_payment_form/', Secretary.income_payment_form, name='secretary_income_payment_form'),
    path('secretary/save_income_payment/', Secretary.save_income_payment, name='secretary_save_income_payment'),
    path('secretary/staff_apply_leave', Secretary.staff_apply_leave, name='secretary_staff_apply_leave'),  
    path('secretary/staff_apply_leave_save', Secretary.staff_apply_leave_save, name='secretary_staff_apply_leave_save'),  
    path('secretary/staff_sendfeedback', Secretary.staff_sendfeedback, name='secretary_staff_sendfeedback'),  
    path('secretary/staff_sendfeedback_save', Secretary.staff_sendfeedback_save, name='secretary_staff_sendfeedback_save'),  
    path('secretary/staff_detail', Secretary.staff_detail, name='secretary_staff_detail'),  
    path('secretary/staff_profile', Secretary.staff_profile, name='secretary_staff_profile'),  
    path('secretary/staff_salary', Secretary.staff_salary, name='secretary_staff_salary'),
    path('secretary/single_student_detail/<int:student_id>/', Secretary.single_student_detail, name='secretary_single_student_detail'),
    path('secretary/delete_parent/<int:parent_id>/', Secretary.delete_parent, name='secretary_delete_parent'),    
    path('secretary/delete_student/<int:student_id>/', Secretary.delete_student, name='secretary_delete_student'),  
    
    # delete
    path('delete_cleaner/<int:cleaner_id>/', Delete.delete_cleaner, name='delete_cleaner'),
    path('delete_car/<int:car_id>/', Delete.delete_car, name='delete_car'),
    path('delete_classroom/<int:classroom_id>/', Delete.delete_classroom, name='delete_classroom'),
    path('delete_parent/<int:parent_id>/', Delete.delete_parent, name='delete_parent'),    
    path('delete_cooker/<int:cooker_id>/', Delete.delete_cooker, name='delete_cooker'),
    path('delete_driver/<int:driver_id>/', Delete.delete_driver, name='delete_driver'),
    path('delete_security/<int:security_id>/', Delete.delete_security, name='delete_security'),
    path('delete_session/<int:session_id>/', Delete.delete_session, name='delete_session'),
    path('delete_staff/<int:staff_id>/', Delete.delete_staff, name='delete_staff'),
    path('delete_student/<int:student_id>/', Delete.delete_student, name='delete_student'),
    path('delete_subject/<int:subject_id>/', Delete.delete_subject, name='delete_subject'),
    path('delete_note/<int:note_id>/', Delete.delete_note, name='delete_note'),



]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)