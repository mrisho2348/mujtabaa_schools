from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from student_management_app.models import (Car,
                                           Students,
                                           SchoolDriver,
                                           SchoolSecurityPerson,
                                           Cooker,
                                           Staffs,
                                           CustomUser,
                                           )


class Contribution(models.Model):
    contributor_name = models.CharField(max_length=50, blank=True, null=True) 
    organization = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    def __str__(self):
        return f"Contribution from {self.source} - {self.date}"
    
    

class ServiceDetails(models.Model):
    service_name = models.CharField(max_length=100)
    amount_required = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return self.service_name
    
class Income_Payment(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    service_details = models.ForeignKey(ServiceDetails, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    amount_remaining = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def save(self, *args, **kwargs):
        # Calculate the amount remaining
        self.amount_remaining = self.service_details.amount_required - self.amount_paid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.service_details.service_name}"    
    
    
class EquipmentPurchase(models.Model):    
    equipment_name = models.CharField(max_length=100)
    equipment_cost = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_by = models.CharField(max_length=50, blank=True, null=True)   
    purchase_date = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
       
    @property
    def remaining_payment(self):
        # Calculate the remaining payment by subtracting the paid amount from the total amount required.
        return self.equipment_cost - self.paid_amount
    
    def __str__(self):
        return f"Equipment Purchase: {self.equipment_name} - {self.purchase_date}"

class Expense(models.Model):
    CATEGORY_CHOICES = [   
        ('Electricity Bill', 'Electricity Bill'),
        ('Water Bill', 'Water Bill'),
        ('WiFi Bill', 'WiFi Bill'),        
        ('Advertising', 'Advertising'),
        # Add more categories as needed
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.get_category_display()} - {self.date}"      

class StaffSalary(models.Model):
    staff_member = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    month = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount_required = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    @property
    def remaining_payment(self):
        # Calculate the remaining payment by subtracting the paid amount from the total amount required.
        return self.total_amount_required - self.paid_amount
    
    def __str__(self):
        return f"{self.staff_member.username} - {self.month.strftime('%B %Y')} Salary"
    
class DriverSalary(models.Model):
    driver_member = models.ForeignKey(SchoolDriver, on_delete=models.CASCADE)
    month = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount_required = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    @property
    def remaining_payment(self):
        # Calculate the remaining payment by subtracting the paid amount from the total amount required.
        return self.total_amount_required - self.paid_amount
    
    def __str__(self):
        return f"{self.staff_member.username} - {self.month.strftime('%B %Y')} Salary"
    
class SecuritySalary(models.Model):
    security_member = models.ForeignKey(SchoolSecurityPerson, on_delete=models.CASCADE)
    month = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount_required = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    @property
    def remaining_payment(self):
        # Calculate the remaining payment by subtracting the paid amount from the total amount required.
        return self.total_amount_required - self.paid_amount
    
    def __str__(self):
        return f"{self.staff_member.username} - {self.month.strftime('%B %Y')} Salary"
    
    
class CookerSalary(models.Model):
    cooker_member = models.ForeignKey(Cooker, on_delete=models.CASCADE)
    month = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount_required = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    @property
    def remaining_payment(self):
        # Calculate the remaining payment by subtracting the paid amount from the total amount required.
        return self.total_amount_required - self.paid_amount
    
    def __str__(self):
        return f"{self.staff_member.username} - {self.month.strftime('%B %Y')} Salary"


    
class CarExpense(models.Model):
    expense_date = models.DateField()
    description = models.TextField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2) 
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return f"Car Expense for {self.car.car_number} - {self.expense_date}"
    class Meta:
        ordering = ['-expense_date']   
         
 # Create the FinancialSummary model for tracking total income and expense
class FinancialSummary(models.Model):
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_capital = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    @property
    def remaining_payment(self):
        # Calculate the remaining payment by subtracting the paid amount from the total amount required.
        return self.total_expense - self.total_income
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return "Financial Summary"
       
 
        
@receiver([post_save, post_delete], sender=EquipmentPurchase)
@receiver([post_save, post_delete], sender=StaffSalary)
@receiver([post_save, post_delete], sender=DriverSalary)
@receiver([post_save, post_delete], sender=SecuritySalary)
@receiver([post_save, post_delete], sender=CookerSalary)
@receiver([post_save, post_delete], sender=CarExpense)
@receiver([post_save, post_delete], sender=Expense)
def update_financial_summary_expense(sender, instance, **kwargs):
    # Calculate the total expenses based on the amounts in related models
    total_expense = (
        EquipmentPurchase.objects.aggregate(total=models.Sum('paid_amount'))['total'] +
        StaffSalary.objects.aggregate(total=models.Sum('paid_amount'))['total'] +
        DriverSalary.objects.aggregate(total=models.Sum('paid_amount'))['total'] +
        SecuritySalary.objects.aggregate(total=models.Sum('paid_amount'))['total'] +
        CookerSalary.objects.aggregate(total=models.Sum('paid_amount'))['total'] +
        CarExpense.objects.aggregate(total=models.Sum('paid_amount'))['total'] + 
        Expense.objects.aggregate(total=models.Sum('paid_amount'))['total']
    )
    
    # Update the FinancialSummary model
    financial_summary, created = FinancialSummary.objects.get_or_create(pk=1)
    financial_summary.total_expense = total_expense or 0
    financial_summary.save()        
    
# Connect to the signal for updating the FinancialSummary when income records change
@receiver([post_save, post_delete], sender=Contribution)
@receiver([post_save, post_delete], sender=Income_Payment)

def update_financial_summary_income(sender, instance, **kwargs):
    # Calculate the total income by aggregating the 'amount' field from income models
    total_income = (
        Contribution.objects.aggregate(total_income=models.Sum('amount'))['amount_paid'] +
        Income_Payment.objects.aggregate(total_income=models.Sum('amount'))['amount_paid'] 

    )

    # Update the FinancialSummary model
    financial_summary, created = FinancialSummary.objects.get_or_create(pk=1)
    financial_summary.total_income = total_income or 0
    financial_summary.save()    
    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"  
    
@receiver(post_save, sender=Contribution)
def create_contribution_notification(sender, instance, **kwargs):
    # Create a notification when a new contribution is added
    user = instance.user  # Assuming there's a user associated with the contribution
    message = f"A new contribution of ${instance.amount} has been added."
    Notification.objects.create(user=user, message=message)      
    
@receiver(post_save, sender=Income_Payment)
def create_school_fee_notification(sender, instance, created, **kwargs):
    if created:
        # Assuming there's a user associated with the student, replace 'instance.student.user' with the actual user field.
        user = instance.student.user
        message = f"A new school fee payment of ${instance.amount_paid} has been added."
        Notification.objects.create(user=user, message=message)
       

            