# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('add_service_details/', views.add_service_details, name='add_service_details'),
    
    # URL pattern for generating the income graph
    path('generate_income_graph/', views.generate_income_graph, name='generate_income_graph'),

    # URL pattern for generating the income statement
    path('generate_income_statement/', views.generate_income_statement, name='generate_income_statement'),

    # URL pattern for generating the balance sheet
    path('generate_balance_sheet/', views.generate_balance_sheet, name='generate_balance_sheet'),

    # URL pattern for analyzing income data
    path('analyze_income_data/', views.analyze_income_data, name='analyze_income_data'),
    path('income_payment_form/', views.income_payment_form, name='income_payment_form'),
    path('save_income_payment/', views.save_income_payment, name='save_income_payment'),
    path('contribution_form/', views.contribution_form, name='contribution_form'),
    path('add_contribution/', views.add_contribution, name='add_contribution'),
    path('add_equipment_purchase/', views.add_equipment_purchase, name='add_equipment_purchase'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('expense_list/', views.expense_list, name='expense_list'),
    path('add_staff_salary/', views.add_staff_salary, name='add_staff_salary'),
    path('staff_salary_list/', views.staff_salary_list, name='staff_salary_list'),
    path('add_driver_salary/', views.add_driver_salary, name='add_driver_salary'),
    path('driver_salary_list/', views.driver_salary_list, name='driver_salary_list'),
    path('add_security_salary/', views.add_security_salary, name='add_security_salary'),
    path('security_salary_list/', views.security_salary_list, name='security_salary_list'),
    path('add_cooker_salary/', views.add_cooker_salary, name='add_cooker_salary'),
    path('cooker_salary_list/', views.cooker_salary_list, name='cooker_salary_list'),
]