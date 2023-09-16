from django.shortcuts import render
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from django.shortcuts import render
from django.db.models import Sum
from .models import SchoolFee, BoardingFee, FoodCharge, Contribution,FinancialSummary


# Create your views here.
def generate_income_graph(request):
    # Calculate income data
    total_school_fee = SchoolFee.objects.aggregate(total=Sum('amount'))['total']
    total_boarding_fee = BoardingFee.objects.aggregate(total=Sum('amount'))['total']
    total_food_charge = FoodCharge.objects.aggregate(total=Sum('amount'))['total']
    total_contribution = Contribution.objects.aggregate(total=Sum('amount'))['total']

    income_categories = ['School Fee', 'Boarding Fee', 'Food Charge', 'Contribution']
    income_values = [total_school_fee, total_boarding_fee, total_food_charge, total_contribution]

    # Create a bar chart using Matplotlib
    plt.figure(figsize=(8, 6))
    plt.bar(income_categories, income_values)
    plt.xlabel('Income Categories')
    plt.ylabel('Amount (USD)')
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
    school_fees = SchoolFee.objects.all()
    boarding_fees = BoardingFee.objects.all()
    food_charges = FoodCharge.objects.all()
    contributions = Contribution.objects.all()

    # Convert data to DataFrames for analysis using Pandas
    school_fee_df = pd.DataFrame(list(school_fees.values()))
    boarding_fee_df = pd.DataFrame(list(boarding_fees.values()))
    food_charge_df = pd.DataFrame(list(food_charges.values()))
    contribution_df = pd.DataFrame(list(contributions.values()))

    # Perform data analysis with Pandas
    # Calculate statistics and trends for each income category
    school_fee_stats = school_fee_df['amount'].describe()
    boarding_fee_stats = boarding_fee_df['amount'].describe()
    food_charge_stats = food_charge_df['amount'].describe()
    contribution_stats = contribution_df['amount'].describe()

    # You can perform more complex analysis, such as time series analysis, data visualization, etc.
    # Example: Calculate the total income per month for each income category
    school_fee_monthly_total = school_fee_df.groupby(school_fee_df['date'].dt.strftime('%Y-%m'))['amount'].sum()
    boarding_fee_monthly_total = boarding_fee_df.groupby(boarding_fee_df['date'].dt.strftime('%Y-%m'))['amount'].sum()
    food_charge_monthly_total = food_charge_df.groupby(food_charge_df['date'].dt.strftime('%Y-%m'))['amount'].sum()
    contribution_monthly_total = contribution_df.groupby(contribution_df['date'].dt.strftime('%Y-%m'))['amount'].sum()

    # Pass analysis results to the template
    context = {
        'school_fee_stats': school_fee_stats,
        'boarding_fee_stats': boarding_fee_stats,
        'food_charge_stats': food_charge_stats,
        'contribution_stats': contribution_stats,
        'school_fee_monthly_total': school_fee_monthly_total,
        'boarding_fee_monthly_total': boarding_fee_monthly_total,
        'food_charge_monthly_total': food_charge_monthly_total,
        'contribution_monthly_total': contribution_monthly_total,
        # Add more analysis results to the context as needed
    }
    return render(request, 'income_data_analysis.html', context)