# urls.py

from django.urls import path
from . import Financial,Delete,Update,views

urlpatterns = [
    # Other URL patterns
    path('add_service_details/', Financial.add_service_details, name='add_service_details'),      
    path('generate_income_graph/', Financial.generate_income_graph, name='generate_income_graph'),    
    path('generate_income_statement/', Financial.generate_income_statement, name='generate_income_statement'), 
    path('generate_balance_sheet/', Financial.generate_balance_sheet, name='generate_balance_sheet'),
    path('analyze_income_data/', Financial.analyze_income_data, name='analyze_income_data'),
    path('income_payment_form/', Financial.income_payment_form, name='income_payment_form'),
    path('save_income_payment/', Financial.save_income_payment, name='save_income_payment'),
    path('contribution_form/', Financial.contribution_form, name='contribution_form'),    
    path('add_contribution/', Financial.add_contribution, name='add_contribution'),
    path('add_equipment_purchase/', Financial.add_equipment_purchase, name='add_equipment_purchase'),
    path('add_expense/', Financial.add_expense, name='add_expense'),    
    path('add_car_expense/', Financial.add_car_expense, name='add_car_expense'),    
    path('add_staff_salary/', Financial.add_staff_salary, name='add_staff_salary'),    
    path('add_driver_salary/', Financial.add_driver_salary, name='add_driver_salary'),    
    path('add_security_salary/', Financial.add_security_salary, name='add_security_salary'),    
    path('add_cooker_salary/', Financial.add_cooker_salary, name='add_cooker_salary'),    
    path('accountant_home', Financial.accountant_home, name='accountant_home'),
     
    path('staff_apply_leave', views.staff_apply_leave, name='staff_apply_leave'),  
    path('staff_apply_leave_save', views.staff_apply_leave_save, name='staff_apply_leave_save'),  
    path('staff_sendfeedback', views.staff_sendfeedback, name='staff_sendfeedback'),  
    path('staff_sendfeedback_save', views.staff_sendfeedback_save, name='staff_sendfeedback_save'),  
    path('staff_profile', views.staff_profile, name='staff_profile'),  
    path('staff_profile_save', views.staff_profile_save, name='staff_profile_save'),
    
    path('contribution_list/', Financial.contribution_list, name='contribution_list'),
    path('equipment_purchase_list/', Financial.equipment_purchase_list, name='equipment_purchase_list'),
    path('car_expense_list/', Financial.car_expense_list, name='car_expense_list'),
    path('service_details_list/', Financial.service_details_list, name='service_details_list'),
    path('staff_salary_list/', Financial.staff_salary_list, name='staff_salary_list'),
    path('expense_list/', Financial.expense_list, name='expense_list'),
    path('driver_salary_list/', Financial.driver_salary_list, name='driver_salary_list'),
    path('cooker_salary_list/', Financial.cooker_salary_list, name='cooker_salary_list'),
    path('security_salary_list/', Financial.security_salary_list, name='security_salary_list'),
    path('income_payment_list/', Financial.income_payment_list, name='income_payment_list'),
    
    path('delete_income_payment/<int:payment_id>/', Delete.delete_income_payment, name='delete_income_payment'),
    path('delete_staff_salary/<int:salary_id>/', Delete.delete_staff_salary, name='delete_staff_salary'),
    path('delete_service_details/<int:service_id>/', Delete.delete_service_details, name='delete_service_details'),
    path('delete_security_salary/<int:salary_id>/', Delete.delete_security_salary, name='delete_security_salary'),
    path('delete_expense/<int:expense_id>/', Delete.delete_expense, name='delete_expense'),
    path('delete_equipment_purchase/<int:purchase_id>/', Delete.delete_equipment_purchase, name='delete_equipment_purchase'),
    path('delete_driver_salary/<int:salary_id>/', Delete.delete_driver_salary, name='delete_driver_salary'),
    path('delete_contribution/<int:contribution_id>/', Delete.delete_contribution, name='delete_contribution'),
    path('delete_cooker_salary/<int:salary_id>/', Delete.delete_cooker_salary, name='delete_cooker_salary'),
    path('car_expense/<int:pk>/delete/', Delete.CarExpenseDeleteView.as_view(), name='delete_car_expense'),
   
    path('edit_cooker_salary/<int:cooker_salary_id>/', Update.edit_cooker_salary, name='edit_cooker_salary'),
    path('edit_car_expense/<int:car_expense_id>/', Update.edit_car_expense, name='edit_car_expense'),
    path('edit_contribution/<int:contribution_id>/', Update.edit_contribution, name='edit_contribution'), 
    path('edit_driver_salary/<int:driver_salary_id>/', Update.edit_driver_salary, name='edit_driver_salary'),
    path('edit_equipment_purchase/<int:equipment_purchase_id>/', Update.edit_equipment_purchase, name='edit_equipment_purchase'),
    path('edit_expense/<int:expense_id>/', Update.edit_expense, name='edit_expense'),
    path('edit_income_payment/<int:income_payment_id>/', Update.edit_income_payment, name='edit_income_payment'),
    path('edit_security_salary/<int:security_salary_id>/', Update.edit_security_salary, name='edit_security_salary'),
    path('edit_staff_salary/<int:salary_id>/', Update.edit_staff_salary, name='edit_staff_salary'),
    path('service_details/<int:service_id>/edit/', Update.edit_service_details, name='edit_service_details'),

]