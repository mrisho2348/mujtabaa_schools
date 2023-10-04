from django.db import models
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save,post_delete
from django.contrib.auth.models import BaseUserManager
from decimal import Decimal
from twilio.rest import Client
from django.conf import settings
# Create your models here.

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects=models.Manager()
    
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, user_type=1, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 1)  # Set the default user_type for superusers
        return self.create_user(username, email, password, **extra_fields)
    
        
class CustomUser(AbstractUser):
    user_type_data = (
        (1, "HOD"),
        (2, "Staff"),
        (3, "Student"),
        (4, "SchoolDriver"),
        (5, "SchoolSecurityPerson"),
        (6, "Cooker"),
        (7, "SchoolCleaner"),
        (8, "Parent"),
    )
    user_type = models.CharField(default=1, choices=user_type_data, max_length=15)

    # Replace the default manager with the custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.username

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    surname = models.TextField(blank=True)
    street_address = models.TextField(blank=True)
    house_number = models.TextField(blank=True)
    gender = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(blank=True, default='2000-01-01')
    contact_number = models.CharField(max_length=20, blank=True)
    background_check = models.TextField(blank=True)
    availability = models.CharField(max_length=255, blank=True)
    preferred_grade_level = models.CharField(max_length=255, blank=True, null=True)
    salary_expectations = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.FileField(null=True, blank=True)
    national_identity_number = models.TextField(null=True, blank=True)
    national_id_photo = models.FileField(null=True, blank=True)
    birth_certificate_photo = models.FileField(null=True, blank=True)
    personal_statement = models.TextField(blank=True)
    fcm_token = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subjects = models.ManyToManyField('Subject', related_name='staffs_subjects', blank=True)
    objects = models.Manager()

class StaffRoleAssignment(models.Model):
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE)  # Link to the staff/user
    role = models.CharField(max_length=255)  # Role or position of the staff    
    notes = models.TextField(blank=True, null=True)
    assigned_date = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return f"{self.staff.username} - {self.role}"

    class Meta:
        verbose_name = "Staff Role Assignment"
        verbose_name_plural = "Staff Role Assignments"
class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    school_segment = models.CharField(max_length=255, null=True, blank=True)
    subject_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name='staff_subjects', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
class Qualifications(models.Model):
    id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    teaching_experience = models.IntegerField(null=True,blank=True)
    educational_qualification = models.CharField(max_length=255)
    certification = models.CharField(max_length=255)
    cv = models.FileField(null=True, blank=True)
    other_certificates = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
class Skills(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    subject_expertise = models.TextField(null=True,blank=True)
    teaching_methods = models.TextField(null=True,blank=True)
    professional_development = models.TextField(null=True,blank=True)
    language_proficiency = models.TextField(null=True,blank=True)
    technology_skills = models.TextField(null=True,blank=True)
    certificate_url = models.FileField(null=True, blank=True)
    special_skills = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    
class EmploymentHistory(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    employment_history = models.TextField(null=True, blank=True)
    company_name = models.TextField(null=True)
    company_address = models.TextField(null=True, blank=True)
    position = models.TextField(null=True,blank=True)
    start_date = models.DateField(blank=True, default='2000-01-01')
    end_date = models.DateField(blank=True, default='2000-01-01')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
class References(models.Model):
    id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    staff_position = models.TextField(null=True,blank=True)
    company_name = models.TextField(null=True,blank=True)
    company_address = models.TextField(null=True,blank=True)
    company_contact_person = models.TextField(null=True,blank=True)
    company_contact_email = models.TextField(null=True,blank=True)
    company_contact_phone = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()    

class Meetings(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)
    agenda = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
class Attendees(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    meeting_id = models.ForeignKey(Meetings, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

# models.py

class SchoolDriver(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=20, blank=False)    
    contact_number = models.CharField(max_length=20, blank=False)
    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=200, blank=False)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True)
    profile_pic = models.ImageField(upload_to='driver_profiles/', blank=True, null=True)
    driving_license_photo = models.ImageField(upload_to='driver_licenses/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"


class SchoolDriverMedicalInfo(models.Model):
    driver = models.OneToOneField(SchoolDriver, on_delete=models.CASCADE, related_name='medical_info')
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)
    health_condition = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Medical Info for {self.driver}"


class SchoolDriverLicenseInfo(models.Model):
    driver = models.OneToOneField(SchoolDriver, on_delete=models.CASCADE, related_name='license_info')
    license_type = models.CharField(max_length=20, blank=True, null=True)
    drivers_license_expiry_reminder = models.DateField(blank=True, null=True)
    additional_licenses = models.TextField(blank=True, null=True)
    certification = models.CharField(max_length=100, blank=True, null=True)
    driver_training_certifications = models.TextField(blank=True, null=True)
    experience_in_transportation = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"License Info for {self.driver}"


class SchoolDriverContact(models.Model):
    driver = models.OneToOneField(SchoolDriver, on_delete=models.CASCADE, related_name='contact_info')
    alternate_contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Contact Info for {self.driver}"


class SchoolDriverEmergencyContact(models.Model):
    driver = models.OneToOneField(SchoolDriver, on_delete=models.CASCADE, related_name='emergency_contact_info')
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Emergency Contact Info for {self.driver}"

# driver infor 
class SchoolDriverEmployment(models.Model):
    driver = models.OneToOneField(SchoolDriver, on_delete=models.CASCADE, related_name='employment_info')
    date_of_joining = models.DateField(blank=True, null=True)
    employment_start_date = models.DateField(blank=True, null=True)
    employment_end_date = models.DateField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_information = models.TextField(blank=True, null=True)
    performance_ratings = models.TextField(blank=True, null=True)
    shift_schedule = models.CharField(max_length=100, blank=True, null=True)
    driving_hours = models.CharField(max_length=100, blank=True, null=True)
    uniform_size = models.CharField(max_length=10, blank=True, null=True)
    uniform_issued_date = models.DateField(blank=True, null=True)
    uniform_return_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Employment Info for {self.driver}"


class SchoolDriverVehicle(models.Model):
    driver = models.OneToOneField(SchoolDriver, on_delete=models.CASCADE, related_name='vehicle_info')
    vehicle_assigned = models.ForeignKey('Car', on_delete=models.SET_NULL, blank=True, null=True)
    personal_vehicle_information = models.TextField(blank=True, null=True)
    vehicle_registration_number = models.CharField(max_length=20, blank=True, null=True)
    vehicle_maintenance_records = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Vehicle Info for {self.driver}"


class SchoolDriverLanguage(models.Model):
    driver = models.ForeignKey(SchoolDriver, on_delete=models.CASCADE, related_name='languages_spoken')
    language = models.CharField(max_length=50)

    def __str__(self):
        return f"Language: {self.language} for {self.driver}"


class SchoolDriverReference(models.Model):
    driver = models.ForeignKey(SchoolDriver, on_delete=models.CASCADE, related_name='references')
    reference_name = models.CharField(max_length=100)
    reference_contact = models.CharField(max_length=20)

    def __str__(self):
        return f"Reference: {self.reference_name} for {self.driver}"


# Car model for vehicle information
class Car(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    make = models.CharField(max_length=100, blank=False)
    model = models.CharField(max_length=100, blank=False)
    year = models.PositiveIntegerField(blank=False)
    license_plate = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(SchoolDriver, on_delete=models.CASCADE, related_name='cars', blank=True, null=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"    

class SchoolSecurityPerson(models.Model):
    # Personal Information
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20, blank=False)
    address = models.CharField(max_length=200, blank=False)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True)
    profile_pic = models.ImageField(upload_to='security_person_profiles/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # Role-specific Information
    security_clearance_expiry = models.DateField(blank=True, null=True)
    patrol_area = models.CharField(max_length=100, blank=True, null=True)
    security_training_courses = models.TextField(blank=True, null=True)

    # Relationships
    

    # Additional fields
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)
    shift_start_time = models.TimeField(blank=True, null=True)
    shift_end_time = models.TimeField(blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    
    uniform_size = models.CharField(max_length=10, blank=True, null=True)
    vehicle_assigned = models.ForeignKey('Car', on_delete=models.SET_NULL, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"



class Cooker(models.Model):
    # Personal Information
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20, blank=False)
    address = models.CharField(max_length=200, blank=False)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True)
    profile_pic = models.ImageField(upload_to='cooker_profiles/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # Role-specific Information
    cooking_shift_hours = models.CharField(max_length=50, blank=True, null=True)
    uniform_size = models.CharField(max_length=10, blank=True, null=True)
    special_dietary_requirements = models.TextField(blank=True, null=True)

    # Relationships
    assigned_classrooms = models.ManyToManyField('Classroom', related_name='cooking_staff', blank=True)

    # Additional fields (if applicable)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    performance_ratings = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"

class SchoolCleaner(models.Model):
    # Personal Information
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20, blank=False)
    address = models.CharField(max_length=200, blank=False)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True)
    profile_pic = models.ImageField(upload_to='cleaner_profiles/', blank=True, null=True)

    # Role-specific Information
    cleaning_shift_hours = models.CharField(max_length=50, blank=True, null=True)
    uniform_size = models.CharField(max_length=10, blank=True, null=True)
    cleaning_duties = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # Relationships
    assigned_classrooms = models.ManyToManyField('Classroom', related_name='cleaning_staff', blank=True)

    # Additional fields (if applicable)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    performance_ratings = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"
    
    

class Classroom(models.Model):
    # Classroom Information
    name = models.CharField(max_length=50, blank=False)
    grade_level = models.CharField(max_length=10, blank=False)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    room_number = models.CharField(max_length=10, blank=True, null=True)
    building = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # Additional fields (if applicable)
    class_rules = models.TextField(blank=True, null=True)
    class_events = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    





class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  
    surname = models.CharField(max_length=100)    
    service_type = models.CharField(max_length=100, default='school', blank=True)    
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10)    
    phone_number = models.CharField(max_length=20)
    school_segment = models.CharField(max_length=100)
    current_class = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    birth_certificate_id = models.CharField(max_length=100)
    allergies = models.TextField(blank=True, null=True)
    current_year = models.IntegerField(blank=True, null=True)
    is_finished = models.BooleanField(default=False)
    address = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)
    house_number = models.CharField(max_length=20)
    health_status = models.CharField(max_length=200)
    physical_disability = models.CharField(max_length=200)
    subjects = models.ManyToManyField(Subject, related_name='students', blank=True)
    profile_pic = models.FileField(null=True, blank=True)
    birth_certificate_photo = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    # Add the ForeignKey field to SessionYearModel
    session_year = models.ForeignKey(SessionYearModel, on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager()
    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
    
    
    
class Parent(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    TYPE_CHOICES = [
        ('parent', 'Parent'),
        ('guardian', 'Guardian'),
        ('sponsor', 'Sponsor'),
    ]
    
    
    phone = models.CharField(max_length=20)
    occupation = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    national_id = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    parent_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    student = models.ManyToManyField(Students,  related_name='parent')
    fcm_token = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)       
    objects = models.Manager()    
    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"

class Route(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Students, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)       
    objects = models.Manager()   

    def __str__(self):
        return self.name    
class TransportationAttendance(models.Model):
    id = models.AutoField(primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    date = models.DateField()
    driver = models.ForeignKey(SchoolDriver, on_delete=models.CASCADE,blank=True,null=True)  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Transportation Attendance for {self.date} on {self.route} by {self.driver}"  
class TransportationAttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    attendance = models.ForeignKey(TransportationAttendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Transportation Attendance Report for {self.student} on {self.attendance.date} - Status: {self.status}"
         
class Attendance(models.Model):
    id = models.AutoField(primary_key=True)  
    subject_id = models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    attendance_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)  
    objects = models.Manager()


class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)  
    student_id = models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance,on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)   
    objects = models.Manager()
    
class LeaveReportStudent(models.Model):
     id = models.AutoField(primary_key=True)     
     student_id = models.ForeignKey(Students,on_delete=models.DO_NOTHING)
     leave_date = models.DateTimeField(auto_now_add=True)
     leave_message = models.TextField()
     leave_status = models.IntegerField(default=0)    
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now_add=True)   
     objects = models.Manager()
     
     
class LeaveReportStaffs(models.Model):
     id = models.AutoField(primary_key=True)     
     staff_id = models.ForeignKey(Staffs,on_delete=models.DO_NOTHING)
     leave_date = models.DateTimeField(auto_now_add=True)
     leave_message = models.TextField()
     leave_status = models.IntegerField(default=0)    
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now_add=True)   
     objects = models.Manager()
     
class LeaveReportSchoolDriver(models.Model):
    id = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(SchoolDriver, on_delete=models.CASCADE)
    leave_date = models.DateTimeField(auto_now_add=True)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Leave Report for Driver: {self.driver_id.admin.first_name} {self.driver_id.admin.last_name}"
    
    
class LeaveReportSchoolSecurityPerson(models.Model):
    id = models.AutoField(primary_key=True)
    security_person_id = models.ForeignKey(SchoolSecurityPerson, on_delete=models.CASCADE)
    leave_date = models.DateTimeField(auto_now_add=True)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Leave Report for Security Person: {self.security_person_id.admin.first_name} {self.security_person_id.admin.last_name}"
    
class LeaveReportCooker(models.Model):
    id = models.AutoField(primary_key=True)
    cooker_id = models.ForeignKey(Cooker, on_delete=models.CASCADE)
    leave_date = models.DateTimeField(auto_now_add=True)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Leave Report for Cooker: {self.cooker_id.admin.first_name} {self.cooker_id.admin.last_name}"
    
    
class LeaveReportSchoolCleaner(models.Model):
    id = models.AutoField(primary_key=True)
    cleaner_id = models.ForeignKey(SchoolCleaner, on_delete=models.CASCADE)
    leave_date = models.DateTimeField(auto_now_add=True)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Leave Report for Cleaner: {self.cleaner_id.admin.first_name} {self.cleaner_id.admin.last_name}"
    
    
class LeaveReportParent(models.Model):
    id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE)
    leave_date = models.DateTimeField(auto_now_add=True)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Leave Report for Parent: {self.parent_id.admin.first_name} {self.parent_id.admin.last_name}"

     
class FeedBackStudent(models.Model):
     id = models.AutoField(primary_key=True)     
     student_id = models.ForeignKey(Students,on_delete=models.DO_NOTHING)
     feedback = models.CharField(max_length=255)     
     feedback_reply = models.TextField()    
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now_add=True)   
     objects = models.Manager()
     
     
class FeedBackStaff(models.Model):
     id = models.AutoField(primary_key=True)     
     staff_id = models.ForeignKey(Staffs,on_delete=models.DO_NOTHING)
     feedback = models.CharField(max_length=255)     
     feedback_reply = models.TextField()    
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now_add=True)   
     objects = models.Manager() 
     
class FeedbackSchoolDriver(models.Model):
    id = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(SchoolDriver, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Feedback for Driver: {self.driver_id.admin.first_name} {self.driver_id.admin.last_name}"
    
class FeedbackSchoolSecurityPerson(models.Model):
    id = models.AutoField(primary_key=True)
    security_person_id = models.ForeignKey(SchoolSecurityPerson, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Feedback for Security Person: {self.security_person_id.admin.first_name} {self.security_person_id.admin.last_name}"
    
class FeedbackCooker(models.Model):
    id = models.AutoField(primary_key=True)
    cooker_id = models.ForeignKey(Cooker, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Feedback for Cooker: {self.cooker_id.admin.first_name} {self.cooker_id.admin.last_name}"
    
    
class FeedbackSchoolCleaner(models.Model):
    id = models.AutoField(primary_key=True)
    cleaner_id = models.ForeignKey(SchoolCleaner, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Feedback for Cleaner: {self.cleaner_id.admin.first_name} {self.cleaner_id.admin.last_name}"
    
class FeedbackParent(models.Model):
    id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Feedback for Parent: {self.parent_id.admin.first_name} {self.parent_id.admin.last_name}"
     
class NotificationStudent(models.Model):
     id = models.AutoField(primary_key=True)     
     student_id = models.ForeignKey(Students,on_delete=models.DO_NOTHING)     
     message = models.TextField()       
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now_add=True)   
     objects = models.Manager()   
     
     
class NotificationSchoolDriver(models.Model):
    id = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(SchoolDriver, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Notification for Driver: {self.driver_id.admin.first_name} {self.driver_id.admin.last_name}"

class NotificationSchoolSecurityPerson(models.Model):
    id = models.AutoField(primary_key=True)
    security_person_id = models.ForeignKey(SchoolSecurityPerson, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Notification for Security Person: {self.security_person_id.admin.first_name} {self.security_person_id.admin.last_name}"
    
    
class NotificationCooker(models.Model):
    id = models.AutoField(primary_key=True)
    cooker_id = models.ForeignKey(Cooker, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Notification for Cooker: {self.cooker_id.admin.first_name} {self.cooker_id.admin.last_name}"
    
    
class NotificationSchoolCleaner(models.Model):
    id = models.AutoField(primary_key=True)
    cleaner_id = models.ForeignKey(SchoolCleaner, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Notification for Cleaner: {self.cleaner_id.admin.first_name} {self.cleaner_id.admin.last_name}"
    
    
class NotificationParent(models.Model):
    id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Notification for Parent: {self.parent_id.admin.first_name} {self.parent_id.admin.last_name}"
       
     
class NotificationStaff(models.Model):
     id = models.AutoField(primary_key=True)     
     staff_id = models.ForeignKey(Staffs,on_delete=models.DO_NOTHING)     
     message = models.TextField()       
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now_add=True)   
     objects = models.Manager()   
     
     
    
    
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:  # HOD
            AdminHOD.objects.create(admin=instance)
        elif instance.user_type == 2:  # Staff
            Staffs.objects.create(admin=instance)
        elif instance.user_type == 3:  # Student
            Students.objects.create(admin=instance, address="", profile_pic="", gender="")
        elif instance.user_type == 4:  # SchoolDriver
            SchoolDriver.objects.create(admin=instance, address="", profile_pic="", gender="", license_number="")
        elif instance.user_type == 5:  # SchoolSecurityPerson
            SchoolSecurityPerson.objects.create(admin=instance, address="", profile_pic="", gender="")
        elif instance.user_type == 6:  # Cooker
            Cooker.objects.create(admin=instance, address="", profile_pic="", gender="")
        elif instance.user_type == 7:  # SchoolCleaner
            SchoolCleaner.objects.create(admin=instance, address="", profile_pic="", gender="")
        elif instance.user_type == 8:  # Parent
            Parent.objects.create(admin=instance, address="", gender="")
            
 
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    elif instance.user_type == 2:
        instance.staffs.save()
    elif instance.user_type == 3:
        instance.students.save()
    elif instance.user_type == 4:  # SchoolDriver
        instance.schooldriver.save()
    elif instance.user_type == 5:  # SchoolSecurityPerson
        instance.schoolsecurityperson.save()
    elif instance.user_type == 6:  # Cooker
        instance.cooker.save()
    elif instance.user_type == 7:  # SchoolCleaner
        instance.schoolcleaner.save()
    elif instance.user_type == 8:  # Parent
        instance.parent.save()


class ExamType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()  # Additional field for a description of the exam type
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()  # Additional field for the creation date
    # Other fields...



class Result(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    date_of_exam = models.DateField()
    current_class = models.CharField(max_length=100,default="Form I")
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def calculate_performance(self):
        if self.total_marks:
            return (self.marks / self.total_marks) * 100
        else:
            return None

    def determine_grade(self):
        if self.marks >= Decimal('75.00'):
            return 'A'
        elif self.marks >= Decimal('65.00'):
            return 'B'
        elif self.marks >= Decimal('45.00'):
            return 'C'
        elif self.marks >= Decimal('30.00'):
            return 'D'
        else:
            return 'F'

    def determine_pass_fail(self):
        pass_threshold = 45  # Adjust this threshold as needed
        if self.marks >= pass_threshold:
            return 'Pass'
        else:
            return 'Fail'




    
    
 
    
    
class StudentExamInfo(models.Model):   # ... (other fields)

    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    division = models.CharField(max_length=50, null=True, blank=True)
    current_class = models.CharField(max_length=100,default="Form I")
    total_grade_points = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0)
    best_subjects = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
        return f"{self.student} - {self.exam_type}"      
    

    
    
class StudentPositionInfo(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    position = models.IntegerField(null=True, blank=True)
    current_class = models.CharField(max_length=100,default="Form I")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.student} - {self.exam_type} - Position: {self.position}"


    
   
   
# Define the signal handler
@receiver(post_save, sender=Result)
@receiver(post_delete, sender=Result)
def update_student_exam_info(sender, instance, **kwargs):
    # Define a function to calculate the grade based on the provided logic
    def calculate_grade(score):
        if score >= 75:
            return 1
        elif score >= 65:
            return 2
        elif score >= 45:
            return 3
        elif score >= 30:
            return 4
        else:
            return 5

    # Check if there are at least seven subjects with results for the student
    student = instance.student
    current_class = instance.current_class
    exam_type = instance.exam_type

    exam_results = Result.objects.filter(
        student=student,
        exam_type=exam_type,
        current_class=current_class
    )

    if exam_results.count() >= 7:
        # Calculate the seven subjects with the highest scores
        sorted_subjects = sorted(exam_results, key=lambda x: x.marks, reverse=True)[:7]
        seven_best_subjects = [subject.subject.subject_name for subject in sorted_subjects]

        # Calculate total grade points
        total_grade_points = sum(calculate_grade(subject.marks) for subject in sorted_subjects)

        # Calculate division based on total grade points
        if 7 <= total_grade_points <= 17:
            division = "Division 1"
        elif 18 <= total_grade_points <= 21:
            division = "Division 2"
        elif 22 <= total_grade_points <= 24:
            division = "Division 3"
        elif 26 <= total_grade_points <= 29:
            division = "Division 4"
        else:
            division = "Division 0"

        # Update or create StudentExamInfo instance
        student_exam_info, created = StudentExamInfo.objects.get_or_create(
            student=student,
            exam_type=exam_type,
            current_class=current_class,
        )

        student_exam_info.division = division
        student_exam_info.total_grade_points = total_grade_points
        student_exam_info.best_subjects = seven_best_subjects
        student_exam_info.save()
        
        

@receiver(post_save, sender=StudentExamInfo)
@receiver(post_delete, sender=StudentExamInfo)
def update_student_position(sender, instance, **kwargs):
    # Retrieve all students with the same current class and exam type
    students = StudentExamInfo.objects.filter(
        current_class=instance.current_class,
        exam_type=instance.exam_type,
    ).order_by('total_grade_points')  # Order by total_grade_points in ascending order

    # Update the positions based on total_grade_points
    for index, student in enumerate(students, start=1):
        student_position, created = StudentPositionInfo.objects.get_or_create(
            student=student.student,
            exam_type=student.exam_type,
            current_class=student.current_class,
        )
        student_position.position = index
        student_position.save()     