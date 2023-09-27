import decimal
from django.shortcuts import render
import matplotlib.pyplot as plt

import pandas as pd
import io
import base64
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.db.models import Sum
from decimal import Decimal
from django.http import HttpResponse
from .models import  (Contribution, 
                      ServiceDetails, 
                      Income_Payment,
                      FinancialSummary,
                      EquipmentPurchase,
                      Expense,
                      StaffSalary,
                      DriverSalary,
                      SecuritySalary,
                      CookerSalary,
                      CarExpense,
                     
                      )
from student_management_app.models import (Car,
                                           Students,
                                           SchoolDriver,
                                           SchoolSecurityPerson,
                                           Cooker,
                                           Staffs,
                                           CustomUser,
                                            Subject,
                                            LeaveReportStaffs,
                                            AttendanceReport,
                                         LeaveReportStudent,
                                           )

def admin_home(request):
    staff_count = Staffs.objects.all().count()
    subject_count = Subject.objects.all().count()
    student_count = Students.objects.all().count()

    subject_all = Subject.objects.all()
    subject_list = [subject.subject_name for subject in subject_all]

    staff_all = Staffs.objects.all()
    attendance_absent_staff_list = []
    staff_name_list = []
    for staff in staff_all:
        leaves = LeaveReportStaffs.objects.filter(staff_id=staff.id, leave_status=1).count()
        attendance_absent_staff_list.append(leaves)
        staff_name_list.append(staff.admin.username)

    student_all = Students.objects.all()
    attendance_present_student_list = []
    attendance_absent_student_list = []
    student_name_list = []
    for student in student_all:
        attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
        attendance_present_student_list.append(attendance)
        attendance_absent_student_list.append(leaves + absent)
        student_name_list.append(student.admin.username)

    context = {
        "staff_count": staff_count,
        "subject_count": subject_count,
        "subject_list": subject_list,
        "attendance_absent_staff_list": attendance_absent_staff_list,
        "staff_name_list": staff_name_list,
        "attendance_present_student_list": attendance_present_student_list,
        "attendance_absent_student_list": attendance_absent_student_list,
        "student_count": student_count,
    }

    return render(request, "hod_template/home_content.html", context)



def generate_income_graph(request):
    # Calculate income data for contributions
    total_contribution = Contribution.objects.aggregate(total=Sum('amount'))['total']

    # Calculate income data for services
    service_categories = ServiceDetails.objects.all()
    income_categories = ['Contribution'] + [service.service_name for service in service_categories]

    # Initialize the income values list with contribution total
    income_values = [total_contribution]

    # Calculate total amounts paid for each service category
    for service in service_categories:
        total_amount_paid = Income_Payment.objects.filter(service_details=service).aggregate(total=Sum('amount_paid'))['total']
        income_values.append(total_amount_paid)

    # Create a bar chart using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(income_categories, income_values)
    plt.xlabel('Income Categories')
    plt.ylabel('Amount (TSH)')
    plt.title('Income Distribution')

    # Convert the chart to a base64-encoded image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.read()).decode()
    buffer.close()

    context = {
        'chart_image': chart_image,
    }
    return render(request, 'income_graph.html', context)


def generate_income_statement(request):
    # Retrieve the FinancialSummary object
    financial_summary = FinancialSummary.objects.first()

    total_income = financial_summary.total_income
    total_expense = financial_summary.total_expense

    net_income = total_income - total_expense

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_income': net_income,
    }
    return render(request, 'income_statement.html', context)

def generate_balance_sheet(request):
    # Calculate assets, liabilities, and equity as needed
    assets = ...
    liabilities = ...
    equity = ...

    context = {
        'assets': assets,
        'liabilities': liabilities,
        'equity': equity,
    }
    return render(request, 'balance_sheet.html', context)


def analyze_income_data(request):
    # Retrieve income data
    contributions = Contribution.objects.all()
    service_details = ServiceDetails.objects.all()

    # Create DataFrames for service details and contributions
    service_df = pd.DataFrame(list(service_details.values()))
    contribution_df = pd.DataFrame(list(contributions.values()))

    # Initialize dictionaries to store analysis results
    service_stats = {}
    contribution_stats = {}

    # Analyze service data
    for service in service_details:
        service_payments = Income_Payment.objects.filter(service_details=service)
        service_stats[service.service_name] = service_payments.aggregate(
            total_paid=Sum('amount_paid'),
            total_remaining=Sum('amount_remaining')
        )

    # Analyze contribution data
    contribution_stats['Contribution'] = contributions.aggregate(
        total=Sum('amount')
    )

    # Pass analysis results to the template
    context = {
        'service_stats': service_stats,
        'contribution_stats': contribution_stats,
    }
    return render(request, 'income_data_analysis.html', context)

def add_service_details(request):
    if request.method == 'POST':
        # Get data from the request
        service_name = request.POST.get('service_name')
        amount_required = request.POST.get('amount_required')

        # Create a new ServiceDetails object and save it
        service_details = ServiceDetails(
            service_name=service_name,
            amount_required=amount_required
        )
        service_details.save()

        # Redirect to a success page or any other desired page
        return redirect('success_page')  # Change 'success_page' to your desired URL name

    return render(request, 'service_details_form.html')

def income_payment_form(request):
    # Fetch the students and service details from your database
    students = Students.objects.all()
    service_details = ServiceDetails.objects.all()

    context = {
        'students': students,
        'service_details': service_details,
    }

    return render(request, 'income_payment_form.html', context)

def save_income_payment(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        service_details_id = request.POST.get('service_details')
        amount_paid = request.POST.get('amount_paid')

        # Retrieve the student and service details objects
        student = Students.objects.get(pk=student_id)
        service_details = ServiceDetails.objects.get(pk=service_details_id)

        # Calculate the amount remaining
        amount_required = service_details.amount_required
        amount_remaining = amount_required - Decimal(amount_paid)

        # Create and save the Income_Payment instance
        income_payment = Income_Payment(
            student=student,
            service_details=service_details,
            amount_paid=amount_paid,
            amount_remaining=amount_remaining,
        )
        income_payment.save()

        # Redirect to a success page or another appropriate URL
        return redirect('success_page_url')

    # Retrieve the list of student members
    students = Students.objects.all()

    context = {'students': students}

    return render(request, 'income_payment_form.html', context)

def contribution_form(request):
    return render(request, 'contribution_form.html')

def add_contribution(request):
    if request.method == 'POST':
        # Get data from the POST request
        contributor_name = request.POST.get('contributor_name')
        organization = request.POST.get('organization')
        source = request.POST.get('source')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        description = request.POST.get('description')

        try:
            # Create a new Contribution object and save it to the database
            contribution = Contribution(
                contributor_name=contributor_name,
                organization=organization,
                source=source,
                amount=amount,
                date=date,
                description=description
            )
            contribution.save()

            # Redirect to a success page or another appropriate page
            return redirect('contribution_list')  # Change 'contribution_list' to the name of your contribution list view
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

    return render(request, 'contribution_form.html')

def add_equipment_purchase(request):
    if request.method == 'POST':
        equipment_name = request.POST.get('equipment_name')
        equipment_cost = request.POST.get('equipment_cost')
        purchased_by = request.POST.get('purchased_by')
        purchase_date = request.POST.get('purchase_date')
        paid_amount = request.POST.get('paid_amount')

        # Calculate the remaining amount
        remaining_amount = float(equipment_cost) - float(paid_amount)

        # Create and save the EquipmentPurchase instance
        equipment_purchase = EquipmentPurchase(
            equipment_name=equipment_name,
            equipment_cost=equipment_cost,
            purchased_by=purchased_by,
            purchase_date=purchase_date,
            paid_amount=paid_amount,
            remaining_amount=remaining_amount
        )
        equipment_purchase.save()

        # Redirect to a success page or another appropriate page
        return redirect('equipment_purchase_list')  # Change to your equipment purchase list view

    return render(request, 'equipment_purchase_form.html')


def add_expense(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        paid_amount = request.POST.get('paid_amount')
        date = request.POST.get('date')
        description = request.POST.get('description')

        # Create and save the Expense instance
        expense = Expense(
            category=category,
            paid_amount=paid_amount,
            date=date,
            description=description
        )
        expense.save()

        # Redirect to a success page or another appropriate page
        return redirect('expense_list')  # Change to your expense list view

    return render(request, 'expense_form.html')

def expense_list(request):
    # Retrieve and display the list of expenses
    expenses = Expense.objects.all()
    context = {'expenses': expenses}
    return render(request, 'expense_list.html', context)

def add_staff_salary(request):
    if request.method == 'POST':
        staff_member_id = request.POST.get('staff_member')
        month = request.POST.get('month')
        paid_amount = request.POST.get('paid_amount')
        total_amount_required = request.POST.get('total_amount_required')
        description = request.POST.get('description')

        # Create and save the StaffSalary instance
        staff_salary = StaffSalary(
            staff_member_id=staff_member_id,
            month=month,
            paid_amount=paid_amount,
            total_amount_required=total_amount_required,
            description=description
        )
        staff_salary.save()

        # Redirect to a success page or another appropriate page
        return redirect('staff_salary_list')  # Change to your staff salary list view

    # Retrieve the list of staff members
    staff_members = StaffSalary.objects.values_list('staff_member__id', 'staff_member__name')

    context = {'staff_members': staff_members}

    return render(request, 'staff_salary_form.html', context)

def staff_salary_list(request):
    # Retrieve and display the list of staff salaries
    staff_salaries = StaffSalary.objects.all()
    context = {'staff_salaries': staff_salaries}
    return render(request, 'staff_salary_list.html', context)



def add_driver_salary(request):
    if request.method == 'POST':
        driver_member_id = request.POST.get('driver_member')
        month = request.POST.get('month')
        paid_amount = request.POST.get('paid_amount')
        total_amount_required = request.POST.get('total_amount_required')
        description = request.POST.get('description')

        # Create and save the DriverSalary instance
        driver_salary = DriverSalary(
            driver_member_id=driver_member_id,
            month=month,
            paid_amount=paid_amount,
            total_amount_required=total_amount_required,
            description=description
        )
        driver_salary.save()

        # Redirect to a success page or another appropriate page
        return redirect('driver_salary_list')  # Change to your driver salary list view

    # Retrieve the list of driver members
    driver_members = DriverSalary.objects.values_list('driver_member__id', 'driver_member__name')

    context = {'driver_members': driver_members}

    return render(request, 'driver_salary_form.html', context)



def driver_salary_list(request):
    # Retrieve and display the list of driver salaries
    driver_salaries = DriverSalary.objects.all()
    context = {'driver_salaries': driver_salaries}
    return render(request, 'driver_salary_list.html', context)

def add_security_salary(request):
    if request.method == 'POST':
        security_member_id = request.POST.get('security_member')
        month = request.POST.get('month')
        paid_amount = request.POST.get('paid_amount')
        total_amount_required = request.POST.get('total_amount_required')
        description = request.POST.get('description')

        # Create and save the SecuritySalary instance
        security_salary = SecuritySalary(
            security_member_id=security_member_id,
            month=month,
            paid_amount=paid_amount,
            total_amount_required=total_amount_required,
            description=description
        )
        security_salary.save()

        # Redirect to a success page or another appropriate page
        return redirect('security_salary_list')  # Change to your security salary list view

    # Retrieve the list of security members
    security_members = SecuritySalary.objects.values_list('security_member__id', 'security_member__name')

    context = {'security_members': security_members}

    return render(request, 'security_salary_form.html', context)

def security_salary_list(request):
    # Retrieve and display the list of security salaries
    security_salaries = SecuritySalary.objects.all()
    context = {'security_salaries': security_salaries}
    return render(request, 'security_salary_list.html', context)




def add_cooker_salary(request):
    if request.method == 'POST':
        cooker_member_id = request.POST.get('cooker_member')
        month = request.POST.get('month')
        paid_amount = request.POST.get('paid_amount')
        total_amount_required = request.POST.get('total_amount_required')
        description = request.POST.get('description')

        # Create and save the CookerSalary instance
        cooker_salary = CookerSalary(
            cooker_member_id=cooker_member_id,
            month=month,
            paid_amount=paid_amount,
            total_amount_required=total_amount_required,
            description=description
        )
        cooker_salary.save()

        # Redirect to a success page or another appropriate page
        return redirect('cooker_salary_list')  # Change to your cooker salary list view

    # Retrieve the list of cooker members
    cooker_members = Cooker.objects.all()

    context = {'cooker_members': cooker_members}

    return render(request, 'cooker_salary_form.html', context)

def cooker_salary_list(request):
    # Retrieve and display the list of cooker salaries
    cooker_salaries = CookerSalary.objects.all()
    context = {'cooker_salaries': cooker_salaries}
    return render(request, 'cooker_salary_list.html', context)

def add_car_expense(request):
    if request.method == 'POST':
        car_id = request.POST.get('car')
        expense_date = request.POST.get('expense_date')
        paid_amount = request.POST.get('paid_amount')
        description = request.POST.get('description')

        # Create and save the CarExpense instance
        car_expense = CarExpense(
            car_id=car_id,
            expense_date=expense_date,
            paid_amount=paid_amount,
            description=description
        )
        car_expense.save()

        # Redirect to a success page or another appropriate page
        return redirect('car_expense_list')  # Change to your car expense list view

    # Retrieve the list of cars
    cars = Car.objects.all()

    context = {'cars': cars}

    return render(request, 'car_expense_form.html', context)

def car_expense_list(request):
    # Retrieve and display the list of car expenses
    car_expenses = CarExpense.objects.all()
    context = {'car_expenses': car_expenses}
    return render(request, 'car_expense_list.html', context)