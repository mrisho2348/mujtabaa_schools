# urls.py

from django.urls import path
from . import Financial

urlpatterns = [
    # Other URL patterns
    path('add_service_details/', Financial.add_service_details, name='add_service_details'),
    
    # URL pattern for generating the income graph
    path('generate_income_graph/', Financial.generate_income_graph, name='generate_income_graph'),

    # URL pattern for generating the income statement
    path('generate_income_statement/', Financial.generate_income_statement, name='generate_income_statement'),

    # URL pattern for generating the balance sheet
    path('generate_balance_sheet/', Financial.generate_balance_sheet, name='generate_balance_sheet'),

    # URL pattern for analyzing income data
    path('analyze_income_data/', Financial.analyze_income_data, name='analyze_income_data'),
    path('income_payment_form/', Financial.income_payment_form, name='income_payment_form'),
    path('save_income_payment/', Financial.save_income_payment, name='save_income_payment'),
    path('contribution_form/', Financial.contribution_form, name='contribution_form'),    
    path('add_contribution/', Financial.add_contribution, name='add_contribution'),
    path('add_equipment_purchase/', Financial.add_equipment_purchase, name='add_equipment_purchase'),
    path('add_expense/', Financial.add_expense, name='add_expense'),
    path('expense_list/', Financial.expense_list, name='expense_list'),
    path('add_staff_salary/', Financial.add_staff_salary, name='add_staff_salary'),
    path('staff_salary_list/', Financial.staff_salary_list, name='staff_salary_list'),
    path('add_driver_salary/', Financial.add_driver_salary, name='add_driver_salary'),
    path('driver_salary_list/', Financial.driver_salary_list, name='driver_salary_list'),
    path('add_security_salary/', Financial.add_security_salary, name='add_security_salary'),
    path('security_salary_list/', Financial.security_salary_list, name='security_salary_list'),
    path('add_cooker_salary/', Financial.add_cooker_salary, name='add_cooker_salary'),
    path('cooker_salary_list/', Financial.cooker_salary_list, name='cooker_salary_list'),
    path('accountant_home', Financial.accountant_home, name='accountant_home'), 
    path('staff_apply_leave', Financial.staff_apply_leave, name='staff_apply_leave'),  
    path('staff_apply_leave_save', Financial.staff_apply_leave_save, name='staff_apply_leave_save'),  
    path('staff_sendfeedback', Financial.staff_sendfeedback, name='staff_sendfeedback'),  
    path('staff_sendfeedback_save', Financial.staff_sendfeedback_save, name='staff_sendfeedback_save'),  
    path('staff_profile', Financial.staff_profile, name='staff_profile'),  
    path('staff_profile_save', Financial.staff_profile_save, name='staff_profile_save'),
]