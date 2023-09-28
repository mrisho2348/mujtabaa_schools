from django.shortcuts import render, redirect, get_object_or_404
from .models import  (Contribution, 
                      ServiceDetails, 
                      Income_Payment,
                    
                      EquipmentPurchase,
                      Expense,
                      StaffSalary,
                      DriverSalary,
                      SecuritySalary,
                      CookerSalary,
                      CarExpense,
                     
                      )

from student_management_app.models import (
                                           SchoolDriver,
                                           SchoolSecurityPerson,
                                           Cooker,
                                           Staffs,
                                            Students,
                                           )
from django.contrib import messages  # Import messages for displaying notifications


def edit_cooker_salary(request, salary_id):
    # Retrieve the CookerSalary instance
    salary = get_object_or_404(CookerSalary, id=salary_id)

    if request.method == 'POST':
        # Handle the form submission for editing
        # update the salary details and save
        salary.month = request.POST.get('month')
        salary.paid_amount = request.POST.get('paid_amount')
        salary.total_amount_required = request.POST.get('total_amount_required')
        salary.description = request.POST.get('description')
        salary.save()

        # Redirect to a success page or another appropriate page
        return redirect('financial_management:cooker_salary_list')  # Change to your salary list view

    # Render the edit form with the salary instance
    context = {'salary': salary}
    return render(request, 'update/edit_cooker_salary.html', context)

def edit_car_expense(request, car_expense_id):
    # Retrieve the CarExpense object to edit
    car_expense = get_object_or_404(CarExpense, id=car_expense_id)

    if request.method == 'POST':
        try:
            # update CarExpense fields based on the POST data
            car_expense.expense_date = request.POST.get('expense_date')
            car_expense.paid_amount = request.POST.get('paid_amount')
            car_expense.description = request.POST.get('description')
            car_expense.save()
            
            messages.success(request, 'Car expense updated successfully.')
            return redirect('financial_management:car_expense_list')
        except Exception as e:
            messages.error(request, f'Error updating car expense: {str(e)}')
            # You can log the exception for debugging purposes if needed

    context = {
        'car_expense': car_expense,
    }
    
    return render(request, 'update/edit_car_expense.html', context)

def edit_contribution(request, contribution_id):
    # Retrieve the Contribution object to edit
    contribution = get_object_or_404(Contribution, id=contribution_id)

    if request.method == 'POST':
        try:
            # update Contribution fields based on the POST data
            contribution.contributor_name = request.POST.get('contributor_name')
            contribution.organization = request.POST.get('organization')
            contribution.source = request.POST.get('source')
            contribution.amount = request.POST.get('amount')
            contribution.date = request.POST.get('date')
            contribution.description = request.POST.get('description')
            contribution.save()
            
            messages.success(request, 'Contribution updated successfully.')
            return redirect('financial_management:contribution_list')
        except Exception as e:
            messages.error(request, f'Error updating contribution: {str(e)}')
            # You can log the exception for debugging purposes if needed

    context = {
        'contribution': contribution,
    }
    
    return render(request, 'update/edit_contribution.html', context)

def edit_cooker_salary(request, cooker_salary_id):
    # Retrieve the CookerSalary object to edit
    cooker_salary = get_object_or_404(CookerSalary, id=cooker_salary_id)

    if request.method == 'POST':
        try:
            # update CookerSalary fields based on the POST data
            cooker_salary.cooker_member_id = request.POST.get('cooker_member')
            cooker_salary.month = request.POST.get('month')
            cooker_salary.paid_amount = request.POST.get('paid_amount')
            cooker_salary.total_amount_required = request.POST.get('total_amount_required')
            cooker_salary.description = request.POST.get('description')
            cooker_salary.save()

            messages.success(request, 'Cooker salary updated successfully.')
            return redirect('financial_management:cooker_salary_list')
        except Exception as e:
            messages.error(request, f'Error updating cooker salary: {str(e)}')
            # You can log the exception for debugging purposes if needed

    context = {
        'cooker_salary': cooker_salary,
        'cooker_members': Cooker.objects.all(),  # You may need to import Cooker model
    }
    
    return render(request, 'update/edit_cooker_salary.html', context)

def edit_driver_salary(request, driver_salary_id):
    # Retrieve the DriverSalary object to edit
    driver_salary = get_object_or_404(DriverSalary, id=driver_salary_id)

    if request.method == 'POST':
        try:
            # update DriverSalary fields based on the POST data
            driver_salary.driver_member_id = request.POST.get('driver_member')
            driver_salary.month = request.POST.get('month')
            driver_salary.paid_amount = request.POST.get('paid_amount')
            driver_salary.total_amount_required = request.POST.get('total_amount_required')
            driver_salary.description = request.POST.get('description')
            driver_salary.save()

            messages.success(request, 'Driver salary updated successfully.')
            return redirect('financial_management:driver_salary_list')
        except Exception as e:
            messages.error(request, f'Error updating driver salary: {str(e)}')
            # You can log the exception for debugging purposes if needed

    context = {
        'driver_salary': driver_salary,
        'driver_members': SchoolDriver.objects.all(),  # You may need to import Driver model
    }
    
    return render(request, 'update/edit_driver_salary.html', context)

def edit_equipment_purchase(request, equipment_purchase_id):
    # Retrieve the EquipmentPurchase object to edit
    equipment_purchase = get_object_or_404(EquipmentPurchase, id=equipment_purchase_id)

    if request.method == 'POST':
        try:
            # update EquipmentPurchase fields based on the POST data
            equipment_purchase.equipment_name = request.POST.get('equipment_name')
            equipment_purchase.equipment_cost = request.POST.get('equipment_cost')
            equipment_purchase.purchased_by = request.POST.get('purchased_by')
            equipment_purchase.purchase_date = request.POST.get('purchase_date')
            equipment_purchase.paid_amount = request.POST.get('paid_amount')
            equipment_purchase.save()

            messages.success(request, 'Equipment purchase updated successfully.')
            return redirect('financial_management:equipment_purchase_list')
        except Exception as e:
            messages.error(request, f'Error updating equipment purchase: {str(e)}')
            # You can log the exception for debugging purposes if needed

    context = {
        'equipment_purchase': equipment_purchase,
    }
    
    return render(request, 'update/edit_equipment_purchase.html', context)

def edit_expense(request, expense_id):
    # Retrieve the Expense object to edit
    expense = get_object_or_404(Expense, id=expense_id)

    if request.method == 'POST':
        try:
            # update Expense fields based on the POST data
            expense.category = request.POST.get('category')
            expense.paid_amount = request.POST.get('paid_amount')
            expense.date = request.POST.get('date')
            expense.description = request.POST.get('description')
            expense.save()

            messages.success(request, 'Expense updated successfully.')
            return redirect('financial_management:expense_list')
        except Exception as e:
            messages.error(request, f'Error updating expense: {str(e)}')
            # You can log the exception for debugging purposes if needed

    context = {
        'expense': expense,
    }
    
    return render(request, 'update/edit_expense.html', context)

def edit_income_payment(request, income_payment_id):
    # Retrieve the Income_Payment object to edit
    income_payment = get_object_or_404(Income_Payment, id=income_payment_id)

    # Retrieve all ServiceDetails
    all_service_details = ServiceDetails.objects.all()

    # Retrieve all Students
    all_students = Students.objects.all()

    if request.method == 'POST':
        try:
            # Update Income_Payment fields based on the POST data
            income_payment.amount_paid = request.POST.get('amount_paid')
            income_payment.save()

            messages.success(request, 'Income payment updated successfully.')
            return redirect('financial_management:income_payment_list')
        except Exception as e:
            messages.error(request, f'Error updating income payment: {str(e)}')
            # You can log the exception for debugging purposes if needed

    context = {
        'income_payment': income_payment,
        'all_service_details': all_service_details,
        'all_students': all_students,
    }
    
    return render(request, 'update/edit_income_payment.html', context)

def edit_security_salary(request, security_salary_id):
    security_salary = get_object_or_404(SecuritySalary, id=security_salary_id)

    if request.method == 'POST':
        # Process the form data for editing
        security_member_id = request.POST.get('security_member')
        month = request.POST.get('month')
        paid_amount = request.POST.get('paid_amount')
        total_amount_required = request.POST.get('total_amount_required')
        description = request.POST.get('description')

        # Retrieve the SchoolSecurityPerson instance
        security_member = SchoolSecurityPerson.objects.get(id=security_member_id)

        # Update the SecuritySalary instance
        security_salary.security_member = security_member
        security_salary.month = month
        security_salary.paid_amount = paid_amount
        security_salary.total_amount_required = total_amount_required
        security_salary.description = description

        security_salary.save()

        messages.success(request, 'Security salary updated successfully.')
        return redirect('financial_management:security_salary_list')
    else:
        # Display the form for editing
        context = {
            'security_salary': security_salary,
            'security_members': SchoolSecurityPerson.objects.all(),
        }
        return render(request, 'update/edit_security_salary.html', context)
    
    
def edit_staff_salary(request, staff_salary_id):
    staff_salary = get_object_or_404(StaffSalary, id=staff_salary_id)

    if request.method == 'POST':
        # Process the form data for editing
        staff_salary.staff_member = request.POST.get('staff_member')
        staff_salary.month = request.POST.get('month')
        staff_salary.paid_amount = request.POST.get('paid_amount')
        staff_salary.total_amount_required = request.POST.get('total_amount_required')
        staff_salary.description = request.POST.get('description')
        staff_salary.save()
        messages.success(request, 'Staff salary updated successfully.')
        return redirect('financial_management:staff_salary_list')
    else:
        # Display the form for editing
        context = {
            'staff_salary': staff_salary,
            'staff_members': Staffs.objects.all(),
        }
        return render(request, 'update/edit_staff_salary.html', context)  

def edit_service_details(request, service_id):
    service = get_object_or_404(ServiceDetails, id=service_id)

    if request.method == 'POST':
        try:
            # Update the service details based on POST data
            service_name = request.POST.get('service_name')
            amount_required = request.POST.get('amount_required')

            # Validate and update the fields
            if service_name and amount_required:
                service.service_name = service_name
                service.amount_required = amount_required
                service.save()

                messages.success(request, 'Service details updated successfully.')
                return redirect('service_details_view', service.id)
            else:
                messages.error(request, 'Please provide valid input for all fields.')
        except Exception as e:
            messages.error(request, f'Error updating service details: {str(e)}')

    context = {'service': service}
    return render(request, 'update/service_details_edit.html', context)      