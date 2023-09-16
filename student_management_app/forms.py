from django import forms

# from student_management_app.models import  SessionYearModel, Staffs
import random
from datetime import date
from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    # Student Information
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['registration_number'].initial = self.generate_registration_number()

    def generate_registration_number(self):
        current_year = date.today().year
        random_number = random.randint(100000, 999999)
        registration_number = f"{random_number}-{current_year}"
        return registration_number
    full_name = forms.CharField(label='Full Name', max_length=100, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label='Sheia Address', max_length=100, widget=forms.TextInput(attrs={"class":"form-control"}))
    street_address = forms.CharField(label='Street Address', max_length=100, widget=forms.TextInput(attrs={"class":"form-control"}))
    house_number = forms.CharField(label='House Number', max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    health_status = forms.CharField(label='Health Status', max_length=100, widget=forms.TextInput(attrs={"class":"form-control"}))
    physical_disability = forms.CharField(label='Physical Disability', max_length=100, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_photo = forms.ImageField(label='Student Photo', widget=forms.ClearableFileInput(attrs={"class":"form-control-file"}))
    birth_certificate_id = forms.CharField(label='Birth Certificate ID', max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    birth_certificate_photo = forms.ImageField(label='Birth Certificate Photo', required=False, widget=forms.ClearableFileInput(attrs={"class":"form-control-file"}))
    allergies = forms.CharField(label='Allergies', max_length=100, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    current_year = forms.IntegerField(label='Current Year of Study', widget=forms.NumberInput(attrs={"class":"form-control"}))
    IS_FINISHED_CHOICES = (
        (False, 'Not Finished'),
        (True, 'Finished'),
    )
    is_finished = forms.ChoiceField(label='Is Finished', choices=IS_FINISHED_CHOICES, initial=False)
    SCHOOL_SEGMENT_CHOICES = (
        ("Nursery", "Nursery Level"),
        ("Primary", "Primary Level"),
        ("Secondary", "Secondary Level"),
    )

    NURSERY_CLASS_CHOICES = [
        ("Baby", "Baby"),
        ("KG1", "KG1"),
        ("KG2", "KG2")
    ]

    PRIMARY_CLASS_CHOICES = [
        ("I", "I"),
        ("II", "II"),
        ("III", "III"),
        ("IV", "IV"),
        ("V", "V"),
        ("VI", "VI")
    ]

    SECONDARY_CLASS_CHOICES = [
        ("Form I", "Form I"),
        ("Form II", "Form II"),
        ("Form III", "Form III"),
        ("Form IV", "Form IV")
    ]

    school_segment = forms.ChoiceField(
        label='School Segment',
        choices=SCHOOL_SEGMENT_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True
    )

    current_class = forms.ChoiceField(
        label='Current Class',
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_current_class_choices(self.initial.get('school_segment'))

    def set_current_class_choices(self, segment):
        if segment == "Nursery":
            choices = self.NURSERY_CLASS_CHOICES
        elif segment == "Primary":
            choices = self.PRIMARY_CLASS_CHOICES
        elif segment == "Secondary":
            choices = self.SECONDARY_CLASS_CHOICES
        else:
            choices = []  # Set empty choices if segment is not valid

        self.fields['current_class'].choices = choices

    # Parent Information
    father_name = forms.CharField(label="Father's Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    father_phone_number = forms.CharField(label="Father's Phone Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    father_address = forms.CharField(label="Father's Sheia Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    father_street_address = forms.CharField(label="Father's Street Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    father_house_number = forms.CharField(label="Father's House Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    father_national_id = forms.CharField(label="Father's National ID", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    father_status_choices = (
        ("Deceased", "Deceased"),
        ("Alive", "Alive"),
    )
    father_status = forms.ChoiceField(
        label="Father's Status",
        choices=father_status_choices,
        widget=forms.Select(attrs={"class":"form-control"}),
        required=True
    )
    father_profession = forms.CharField(label="Father's Profession", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    mother_name = forms.CharField(label="Mother's Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    mother_phone_number = forms.CharField(label="Mother's Phone Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    mother_address= forms.CharField(label="Mother's Sheia Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    mother_street_address = forms.CharField(label="Mother's Street Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    mother_house_number = forms.CharField(label="Mother's House Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    mother_national_id = forms.CharField(label="Mother's National ID", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    mother_status_choices = (
        ("Deceased", "Deceased"),
        ("Alive", "Alive"),
    )
    mother_status = forms.ChoiceField(
        label="mother's Status",
        choices=mother_status_choices,
        widget=forms.Select(attrs={"class":"form-control"}),
        required=True
    )
    mother_profession = forms.CharField(label="Mother's Profession", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    # Guardian Information (optional)
    guardian_name = forms.CharField(label="Guardian's Name", max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    guardian_phone_number = forms.CharField(label="Guardian's Phone Number", max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    guardian_address = forms.CharField(label="Guardian's Sheia Address", max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    guardian_street_address = forms.CharField(label="Guardian's Street Address", max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    guardian_house_number = forms.CharField(label="Guardian's House Number", max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    guardian_national_id = forms.CharField(label="Guardian's National ID", max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    guardian_status_choices = (
        ("Deceased", "Deceased"),
        ("Alive", "Alive"),
    )
    guardian_status = forms.ChoiceField(
        label="guardian's Status",
        choices=guardian_status_choices,
        widget=forms.Select(attrs={"class":"form-control"}),
        required=True
    )    
    guardian_profession = forms.CharField(label="Guardian's Profession", max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))

    # Sponsor Information (optional)
    sponsor_name = forms.CharField(label="Sponsor's Name", max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    sponsor_phone_number = forms.CharField(label="Sponsor's Phone Number", max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    sponsor_address = forms.CharField(label="Sponsor's Sheia Address", max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    sponsor_street_address = forms.CharField(label="Sponsor's Street Address", max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    sponsor_house_number = forms.CharField(label="Sponsor's House Number", max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    sponsor_national_id = forms.CharField(label="Sponsor's National ID", max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    sponsor_status_choices = (
        ("Deceased", "Deceased"),
        ("Alive", "Alive"),
    )
    sponsor_status = forms.ChoiceField(
        label="sponsor's Status",
        choices=sponsor_status_choices,
        widget=forms.Select(attrs={"class":"form-control"}),
        required=True
    )       
    sponsor_profession = forms.CharField(label="Sponsor's Profession", max_length=50, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))

    # Other fields...

    def clean(self):
        cleaned_data = super().clean()

        # Check if all required parent information is provided
        if not cleaned_data.get('father_name') and not cleaned_data.get('mother_name'):
            raise forms.ValidationError("At least one parent's information must be provided.")

        return cleaned_data

    
    
class EditStudentForm(forms.Form):
    email = forms.CharField(label='EMAIL',max_length=50,widget = forms.EmailInput(attrs={"class":"form-control"}))    
    first_name = forms.CharField(label='First Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label='Last Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username  = forms.CharField(label='Username',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label='Address',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    # course_list = []    
    # courses = Courses.objects.all()    
    # for course in courses:
    #        small_course = (course.id,course.Course_name)
    #        course_list.append(small_course)
           
   
        # course_list = []    
    
    # session_year_list = []    
    # sessions = SessionYearModel.objects.all()    
    # for session in sessions:
    #        small_session_list = (session.id,str(session.session_start_year)+" To "+str(session.session_end_year))
    #        session_year_list.append(small_session_list)
           
    
    #     # session_year_list = []     
    # gender_choice = (
    #     ("Male","Male"),
    #     ("Female","Female")
    # )    
    # # course_name = forms.ChoiceField(label='Course', choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))    
    # sex = forms.ChoiceField(label='Sex', choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    # session_year_id= forms.ChoiceField(label='Session Year',choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    # profile_pic = forms.FileField(label='Profile Pic',max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)
    
    
    
class AddStaffForm(forms.Form):
    email = forms.CharField(label='EMAIL',max_length=50,widget = forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label='Password',max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label='First Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label='Last Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username  = forms.CharField(label='Username',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label='Address',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    
class EditStaffForm(forms.Form):
    email = forms.CharField(label='EMAIL',max_length=50,widget = forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label='First Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label='Last Name',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username  = forms.CharField(label='Username',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label='Address',max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
  
class AddCourseForm(forms.Form):
    course = forms.CharField(label='Course Name',max_length=50,widget = forms.TextInput(attrs={"class":"form-control"}))


class AddSubjectForm(forms.Form):
    SCHOOL_SEGMENT_CHOICES = (
        ('Nursery', 'Nursery'),
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
    )

    subject_name = forms.CharField(
        label='Subject Name',
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    school_segment = forms.ChoiceField(
        label='School level',
        choices=SCHOOL_SEGMENT_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    
class AddSessionYearForm(forms.Form):
    session_start = forms.DateField(label='Session start year',widget = forms.DateInput(attrs={"class":"form-control","placeholder":"Enter session start year","type":"date"}))
    session_end = forms.DateField(label='Session end year',widget = forms.DateInput(attrs={"class":"form-control","placeholder":"Enter session end year","type":"date"}))
    

  