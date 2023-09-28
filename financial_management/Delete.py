from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Import messages for displaying notifications
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
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView




def delete_cooker_salary(request, salary_id):
    # Retrieve the CookerSalary instance
    salary = get_object_or_404(CookerSalary, id=salary_id)
    if request.method == 'POST':
        # Handle the deletion confirmation
        salary.delete()
        # Redirect to a success page or another appropriate page
        return redirect('financial_management:cooker_salary_list')  # Change to your salary list view
    # Render the delete confirmation page
    context = {'salary': salary}
    return render(request, 'delete/delete_cooker_salary.html', context)

def delete_driver_salary(request, salary_id):
    # Retrieve the driver's salary to be deleted
    driver_salary = get_object_or_404(DriverSalary, id=salary_id)

    if request.method == 'POST':
        # If the user confirms the deletion, delete the salary record
        driver_salary.delete()
        messages.success(request, 'Driver salary deleted successfully.')
        return redirect('financial_management:driver_salary_list')
    
    # Render the confirmation template
    context = {'driver_salary': driver_salary}
    return render(request, 'delete/delete_driver_salary.html', context)

def delete_equipment_purchase(request, purchase_id):
    # Retrieve the equipment purchase to be deleted
    equipment_purchase = get_object_or_404(EquipmentPurchase, id=purchase_id)
    if request.method == 'POST':
        # If the user confirms the deletion, delete the purchase record
        equipment_purchase.delete()
        messages.success(request, 'Equipment purchase record deleted successfully.')
        return redirect('financial_management:equipment_purchase_list')    
    # Render the confirmation template
    context = {'equipment_purchase': equipment_purchase}
    return render(request, 'delete/delete_equipment_purchase.html', context)


def delete_expense(request, expense_id):
    # Retrieve the expense record to be deleted
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        # If the user confirms the deletion, delete the expense record
        expense.delete()
        messages.success(request, 'Expense record deleted successfully.')
        return redirect('financial_management:expense_list')    
    # Render the confirmation template
    context = {'expense': expense}
    return render(request, 'delete/delete_expense.html', context)

def delete_security_salary(request, salary_id):
    # Retrieve the security salary record to be deleted
    security_salary = get_object_or_404(SecuritySalary, id=salary_id)

    if request.method == 'POST':
        # If the user confirms the deletion, delete the security salary record
        security_salary.delete()
        messages.success(request, 'Security salary record deleted successfully.')
        return redirect('financial_management:security_salary_list')
    
    # Render the confirmation template
    context = {'security_salary': security_salary}
    return render(request, 'delete/delete_security_salary.html', context)

def delete_service_details(request, service_id):
    # Retrieve the service detail record to be deleted
    service_detail = get_object_or_404(ServiceDetails, id=service_id)

    if request.method == 'POST':
        # If the user confirms the deletion, delete the service detail record
        service_detail.delete()
        messages.success(request, 'Service detail record deleted successfully.')
        return redirect('financial_management:service_details_list')
    
    # Render the confirmation template
    context = {'service_detail': service_detail}
    return redirect('financial_management:service_details_list')

def delete_staff_salary(request, salary_id):
    # Retrieve the staff salary record to be deleted
    staff_salary = get_object_or_404(StaffSalary, id=salary_id)

    if request.method == 'POST':
        # If the user confirms the deletion, delete the staff salary record
        staff_salary.delete()
        messages.success(request, 'Staff salary record deleted successfully.')
        return redirect('financial_management:staff_salary_list')
    
    # Render the confirmation template
    context = {'staff_salary': staff_salary}
    return render(request, 'delete/delete_staff_salary.html', context)

def delete_income_payment(request, payment_id):
    # Fetch the income payment to be deleted
    income_payment = get_object_or_404(Income_Payment, id=payment_id)
    if request.method == 'POST':
        # delete the income payment
        income_payment.delete()
        # Redirect to the income payments list view
        return redirect('financial_management:income_payment_list')
    context = {'income_payment': income_payment}
    return render(request, 'delete/delete_income_payment.html', context)

def delete_contribution(request, contribution_id):
    contribution = get_object_or_404(Contribution, id=contribution_id)
    if request.method == 'POST':
        try:
            # Delete the contribution
            contribution.delete()
            messages.success(request, 'Contribution deleted successfully.')
            return redirect('financial_management:contribution_list')
        except Exception as e:
            messages.error(request, f'Error deleting contribution: {str(e)}')    
            # You can log the exception for debugging purposes if needed

    context = {'contribution': contribution}
    return render(request, 'delete/delete_contribution.html', context)

class CarExpenseDeleteView(DeleteView):
    model = CarExpense
    template_name = 'financial/car_expense_delete.html'
    success_url = reverse_lazy('financial_management:car_expense_list')