from datetime import datetime
from django.utils import timezone
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseServerError,HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from student_management_app.models import Students, Subject
from .models import Exam_Model, Group, Question_DB, Question_Paper, Staffs, Stu_Question, StuExam_DB, StuResults_DB
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

@csrf_exempt
def add_question_save(request):
    if request.method == 'POST':
        try:
            # Get data from the POST request
            question = request.POST.get('question')
            optionA = request.POST.get('optionA')
            optionB = request.POST.get('optionB')
            optionC = request.POST.get('optionC')
            optionD = request.POST.get('optionD')
            answer = request.POST.get('answer')
            print(answer)
            # Get the logged-in staff user
            try:
                logged_in_staff = Staffs.objects.get(admin=request.user)
            except ObjectDoesNotExist:
                return JsonResponse({'message': 'Staff information not found'}, status=404)
            
            # Create and save the question
            question_obj = Question_DB(
                teacher=logged_in_staff,
                question=question,
                optionA=optionA,
                optionB=optionB,
                optionC=optionC,
                optionD=optionD,
                answer=answer
            )
            question_obj.save()
            
            return JsonResponse({'message': 'Question saved successfully'})
        except Exception as e:
            return JsonResponse({'message': 'An error occurred', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

def add_question(request):
    return render(request, 'staff_manage_exam/add_question_db.html')

@login_required
def add_question_paper(request): 
    return render(request, 'staff_manage_exam/add_question_paper.html')

@login_required
def add_exam_model(request): 
    return render(request, 'staff_manage_exam/add_exam_model.html')


@csrf_exempt
def add_question_paper_save(request):
    if request.method == 'POST':
        try:
            qPaperTitle = request.POST.get('qPaperTitle')
            selected_questions = request.POST.getlist('selectedQuestions[]')
            action = request.POST.get('action')
            
            # Get the logged-in staff user
            try:
                logged_in_staff = Staffs.objects.get(admin=request.user)
            except ObjectDoesNotExist:
                return JsonResponse({'message': 'Staff information not found'}, status=404)
            
            # Create the Question Paper
            question_paper = Question_Paper(
                teacher=logged_in_staff,
                qPaperTitle=qPaperTitle,
                
            )
            question_paper.save()
            
            # Add selected questions to the question paper
            question_paper.questions.set(selected_questions)
            
            if action == 'save':
                message = 'Question paper saved successfully'
            elif action == 'save-continue':
                message = 'Question paper saved and continue adding'
            else:
                message = 'Question paper saved and continue editing'
            
            return JsonResponse({'message': message})
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Staff not found'}, status=404)
        except Exception as e:
            # Log the error for debugging
            print('Error:', e)
            return JsonResponse({'message': 'An error occurred while processing your request'}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

@csrf_exempt
def get_questions(request):
    if request.method == 'GET':
        try:
            # Retrieve questions for the current logged-in user
            questions = Question_DB.objects.filter(teacher=request.user.staffs)  # Adjust this according to your model relationship
            
            question_list = []
            for question in questions:
                question_text = f'Question No.{question.qno}: {question.question}\nOptions:\nA. {question.optionA}\nB. {question.optionB}\nC. {question.optionC}\nD. {question.optionD}'
                question_list.append({
                    'id': question.qno,  # Use qno as ID
                    'question_text': question_text,
                })

            return JsonResponse(question_list, safe=False)
        except Exception as e:
            return JsonResponse({'message': 'An error occurred', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    
def get_student_groups(request):
    student_groups = Students.objects.values_list('current_class', flat=True).distinct()
    
    # Format the data as a list of dictionaries
    groups_data = [{'id': idx, 'name': group} for idx, group in enumerate(student_groups, start=1)]
    
    return JsonResponse(groups_data, safe=False)
    

@login_required  # Require user authentication
def get_question_papers(request):
    # Assuming the logged-in user is a teacher
    logged_teacher = request.user.staffs  # Replace 'teacher' with the actual field name
    
    # Fetch question papers associated with the logged-in teacher
    question_papers = Question_Paper.objects.filter(teacher=logged_teacher)
    
    # Serialize the question papers
    serialized_papers = []
    for paper in question_papers:
        serialized_papers.append({
            'id': paper.id,
            'name': paper.qPaperTitle,
            # Add other fields as needed
        })
    
    return JsonResponse(serialized_papers, safe=False)  
  

@login_required  # Require user authentication
def get_subjects(request):
    # Assuming the logged-in user is a teacher
    staff = Staffs.objects.get(admin=request.user.id)
    subjects = staff.subjects.all()     
    # Serialize the subjects
    serialized_subjects = []
    for subject in subjects:
        serialized_subjects.append({
            'id': subject.id,
            'name': subject.subject_name,
            # Add other fields as needed
        })
    
    return JsonResponse(serialized_subjects, safe=False)




@login_required
def add_exam_save(request):
    if request.method == 'POST':
        try:
            # Get data from the form
            name = request.POST.get('name')
            total_marks = request.POST.get('totalMarks')
            duration = int(request.POST.get('duration'))  # Convert duration to an integer
            question_paper_id = request.POST.get('questionPaper')
            group_id = request.POST.get('studentGroups')  # Use the correct field name
            print(group_id)
            subjects = request.POST.getlist('subjects')  # If the field supports multiple selections
            start_date_str = request.POST.get('startDate')
            start_time_str = request.POST.get('startTime')
            end_date_str = request.POST.get('endDate')
            end_time_str = request.POST.get('endTime')
            
            # Combine date and time strings and convert to datetime objects
            start_datetime = datetime.strptime(start_date_str + ' ' + start_time_str, '%Y-%m-%d %H:%M')
            end_datetime = datetime.strptime(end_date_str + ' ' + end_time_str, '%Y-%m-%d %H:%M')
            
            # Validate start and end times
            if start_datetime >= end_datetime:
                return JsonResponse({'message': 'Start time must be before end time.'}, status=400)
            
            # Calculate duration in minutes
            duration_minutes = (end_datetime - start_datetime).seconds // 60
            if duration != duration_minutes:
                return JsonResponse({'message': 'Duration does not match the time difference.'}, status=400)
            
            # Assuming you have a logged-in teacher or staff associated with the request
            staff = request.user.staffs  # Replace with the actual way to get the staff
            
            # Create the Exam_Model instance
            exam = Exam_Model.objects.create(
                staff=staff,
                name=name,
                total_marks=total_marks,
                duration=duration,
                question_paper_id=question_paper_id,
                group_id=group_id,  # Use the correct field name
                start_time=start_datetime,
                end_time=end_datetime
            )
            
            # Add subjects (assuming you have ManyToManyField relationships)
            exam.subjects.set(subjects)
            
            return JsonResponse({'message': 'Exam saved successfully.'})
        except Exception as e:
            return JsonResponse({'message': f'Error saving exam: {str(e)}'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)
    
    
def edit_exam_model(request, exam_id):
    exam = get_object_or_404(Exam_Model, id=exam_id)
    student_groups = Group.objects.all()  # Fetch all student groups
    subjects = Subject.objects.all()  # Fetch all subjects
    question_papers = Question_Paper.objects.all()  # Fetch all question papers
    
    context = {
       'exam': exam,
       'student_groups': student_groups,
       'subjects': subjects,
       'question_papers': question_papers,
        'examData': {
             'studentGroups': [exam.group.id] if exam.group else [],
             'subjects': [subject.id for subject in exam.subjects.all()],
             'questionPaper': exam.question_paper.id,  # Assuming you have a question_paper field in your Exam_Model
        # ... other exam data
         }
     }
    return render(request, 'staff_manage_exam/edit_exams_model.html', context)

def view_exam_model(request, exam_id):
    exam = get_object_or_404(Exam_Model, id=exam_id)
    # print(exam.subjects.all())  # Check the subjects associated with the exam
    context = {'exam': exam}
    return render(request, 'staff_manage_exam/detail_of_exams_model.html', context)

@csrf_exempt
def edit_exam_save(request, exam_id):
    if request.method == 'POST':
        try:
            exam = get_object_or_404(Exam_Model, id=exam_id)
            
            exam.name = request.POST.get('name')
            exam.total_marks = request.POST.get('totalMarks')
            exam.duration = request.POST.get('duration')
            
            # Convert time strings to datetime objects
            start_date_str = request.POST.get('startDate')
            start_time_str = request.POST.get('startTime')
            end_date_str = request.POST.get('endDate')
            end_time_str = request.POST.get('endTime')
            
            # Combine date and time strings and convert to datetime objects
            start_datetime = datetime.strptime(start_date_str + ' ' + start_time_str, '%Y-%m-%d %H:%M')
            end_datetime = datetime.strptime(end_date_str + ' ' + end_time_str, '%Y-%m-%d %H:%M')
            
            # Validate start and end times
            if start_datetime >= end_datetime:
                return JsonResponse({'message': 'Start time must be before end time.'}, status=400)
            
            # Calculate duration in minutes
            duration_minutes = (end_datetime - start_datetime).seconds // 60
            if int(request.POST.get('duration')) != duration_minutes:
                return JsonResponse({'message': 'Duration does not match the time difference.'}, status=400)
            
            # Update the time components of the existing start_time and end_time
            exam.start_time = exam.start_time.replace(hour=start_datetime.hour, minute=start_datetime.minute)
            exam.end_time = exam.end_time.replace(hour=end_datetime.hour, minute=end_datetime.minute)
            
            # Handle 'questionPaper'
            question_paper_id = request.POST.get('questionPaper')
            exam.question_paper = Question_Paper.objects.get(id=question_paper_id)
            
            # Handle 'studentGroups'
            group_id = request.POST.get('studentGroups')
            exam.group = Group.objects.get(id=group_id)
            
            # Handle 'subjects'
            subject_ids = request.POST.getlist('subjects')
            exam.subjects.set(subject_ids)
            print('Start Time String:', start_date_str)
            print('End Time String:', start_time_str)
            exam.save()
            
            return JsonResponse({'message': 'Exam updated successfully.'})
        except Exam_Model.DoesNotExist:
            return JsonResponse({'message': 'Exam not found.'}, status=404)
        except Question_Paper.DoesNotExist:
            return JsonResponse({'message': 'Question Paper not found.'}, status=404)
        except Group.DoesNotExist:
            return JsonResponse({'message': 'Student Group not found.'}, status=404)
        except Subject.DoesNotExist:
            return JsonResponse({'message': 'Subject not found.'}, status=404)
        except Exception as e:
            # Log the error for debugging
            print('Error:', e)
            return JsonResponse({'message': 'An error occurred while updating the exam.'}, status=500)
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@csrf_exempt
def publish_exam(request):
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        try:
            exam = Exam_Model.objects.get(id=exam_id)
            if not exam.is_published:
                exam.is_published = True
                exam.publish_date = datetime.now()  # Use datetime.now() instead of timezone.now()
                exam.save()
                message = f"Exam '{exam.name}' has been published."
                return JsonResponse({'message': message})
            else:
                message = f"Exam '{exam.name}' is already published."
                return JsonResponse({'message': message})
        except Exam_Model.DoesNotExist:
            return JsonResponse({'message': 'Exam not found.'})
    else:
        return JsonResponse({'message': 'Invalid request method.'})
    
    
def delete_exam_model(request):
    if request.method == 'POST':
        try:
            exam_id = request.POST.get('exam_id')
            exam = get_object_or_404(Exam_Model, id=exam_id)
            exam.delete()
            return JsonResponse({'message': 'Exam deleted successfully.'})
        except Exam_Model.DoesNotExist:
            return JsonResponse({'message': 'Exam not found.'}, status=404)
        except Exception as e:
            # Log the error for debugging
            print('Error:', e)
            return JsonResponse({'message': 'An error occurred while deleting the exam.'}, status=500)
    return JsonResponse({'message': 'Invalid request method.'}, status=400)
  

def question_list(request):
    user = request.user
    questions = Question_DB.objects.filter(teacher=user.staffs) # Filter questions related to the current user
    context = {'questions': questions}
    return render(request, 'staff_manage_exam/question_list.html', context)    



def question_edit(request, qno):
    question = get_object_or_404(Question_DB, qno=qno)  # Get the question by qno
    if request.method == 'POST':
        question.question = request.POST.get('question')
        question.optionA = request.POST.get('optionA')
        question.optionB = request.POST.get('optionB')
        question.optionC = request.POST.get('optionC')
        question.optionD = request.POST.get('optionD')
        question.answer = request.POST.get('answer')
        question.save()
        return redirect('question_list')  # Redirect to the list view after editing
    context = {'question': question}
    return render(request, 'staff_manage_exam/edit_question_db.html', context)



@csrf_exempt
def handle_action(request):
    if request.method == 'POST':
        selected_action = request.POST.get('action')
        if selected_action == 'delete_selected':
            # Get the list of selected items
            selected_items = request.POST.getlist('_selected_action')

            try:
                # Delete the selected items from the database
                deleted_count, _ = Question_DB.objects.filter(qno__in=selected_items).delete()
                print("Deleted count:", deleted_count)
                return JsonResponse({'message': f'{deleted_count} selected items deleted successfully.'})
            except ObjectDoesNotExist:
                return JsonResponse({'message': 'Selected items not found.'}, status=400)
            except ValidationError as ve:
                return JsonResponse({'message': f'Validation error: {ve}'}, status=400)
            except Exception as e:
                print("Error:", e)
                return JsonResponse({'message': f'Error deleting selected items: {str(e)}'}, status=400)

    return JsonResponse({'message': 'Error handling the action.'}, status=400)


@csrf_exempt
def edit_question_save(request, qno):
    question = get_object_or_404(Question_DB, qno=qno)

    if request.method == 'POST':
        # Update the question fields
        question.question = request.POST.get('question')
        question.optionA = request.POST.get('optionA')
        question.optionB = request.POST.get('optionB')
        question.optionC = request.POST.get('optionC')
        question.optionD = request.POST.get('optionD')
        question.answer = request.POST.get('answer')
        question.save()
        
        return JsonResponse({'message': 'Question updated successfully.'})
    
    return JsonResponse({'message': 'Invalid request method.'}, status=405)


    
@login_required  # Ensures the user is logged in to access this view
def exams_list(request):
    user = request.user
    exams = Exam_Model.objects.filter(staff=user.staffs)  # Filter exams by the logged-in user
    context = {'exams': exams}
    return render(request, 'staff_manage_exam/list_of_exams_model.html', context)    

@login_required
def question_papers_list(request):
    question_papers = Question_Paper.objects.all()
    context = {'question_papers': question_papers}
    return render(request, 'staff_manage_exam/list_of_questional_paper.html', context)
@login_required
def question_papers_list(request):
    question_papers = Question_Paper.objects.all()
    context = {'question_papers': question_papers}
    return render(request, 'staff_manage_exam/list_of_questional_paper.html', context)





@login_required
def edit_question_paper(request, q_paper_id):
    q_paper = get_object_or_404(Question_Paper, id=q_paper_id)
    
    # Fetch questions that belong to the logged-in staff
    questions = Question_DB.objects.filter(teacher=request.user.staffs)

    # Create a list to store formatted question data for the selection options
    question_list = []
    selected_question_ids = q_paper.questions.all().values_list('qno', flat=True)  # IDs of selected questions
    for question in questions:
        question_text = f'Question No.{question.qno}: {question.question}\nOptions:\nA. {question.optionA}\nB. {question.optionB}\nC. {question.optionC}\nD. {question.optionD}'
        question_list.append({
            'id': question.qno,
            'question_text': question_text,
            'selected': question.qno in selected_question_ids,
        })

    # Fetch existing question papers for the logged-in staff
    question_papers = Question_Paper.objects.filter(teacher=request.user.staffs)

    context = {
        'q_paper': q_paper,
        'question_list': question_list,
        'question_papers': question_papers,
    }

    return render(request, 'staff_manage_exam/edit_question_paper.html', context)

@csrf_exempt
def edit_question_paper_save(request, q_paper_id):
    if request.method == 'POST':
        try:
            q_paper = Question_Paper.objects.get(id=q_paper_id)
            
            qPaperTitle = request.POST.get('q_paper_title')
            selected_questions = request.POST.getlist('selected_questions[]')
            
            q_paper.qPaperTitle = qPaperTitle
            q_paper.questions.set(selected_questions)
            q_paper.save()
            
            message = 'Question paper saved successfully'
            
            return JsonResponse({'message': message})
        except Question_Paper.DoesNotExist:
            return JsonResponse({'message': 'Question paper not found'}, status=404)
        except Exception as e:
            # Log the error for debugging
            print('Error:', e)
            return JsonResponse({'message': 'An error occurred while processing your request'}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


@login_required
def delete_question_paper(request):
    if request.method == 'POST':
        q_paper_id = request.POST.get('q_paper_id')
        try:
            q_paper = Question_Paper.objects.get(id=q_paper_id)
            q_paper.delete()
            return JsonResponse({'message': 'Question Paper deleted successfully.'})
        except Question_Paper.DoesNotExist:
            return JsonResponse({'message': 'Question Paper not found.'})
    return JsonResponse({'message': 'Invalid request method.'})

@require_POST
def edit_question_save(request, qno):
    try:
        question = Question_DB.objects.get(qno=qno)

        # Update the fields with the submitted data
        question.question = request.POST.get('question')
        question.optionA = request.POST.get('optionA')
        question.optionB = request.POST.get('optionB')
        question.optionC = request.POST.get('optionC')
        question.optionD = request.POST.get('optionD')
        question.answer = request.POST.get('answer')
        question.save()

        # Return a success response
        return JsonResponse({'message': 'Question changed successfully.'})
    except Question_DB.DoesNotExist:
        return JsonResponse({'message': 'Question not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'message': f'Error saving question: {str(e)}'}, status=500)
    
# for students 

def get_published_exam_count(request):
    student = Students.objects.get(admin=request.user.id)
    group_name = student.current_class
    
    student_group = Group.objects.filter(name=group_name).first()

    if student_group:
        count = Exam_Model.objects.filter(is_published=True, group=student_group).count()
        print(count)
    else:
        count = 0

    return JsonResponse({"count": count})  
    

def take_exam(request, exam_id):
    exam = Exam_Model.objects.get(pk=exam_id)
    question_paper = exam.question_paper
    questions = question_paper.questions.all()

    # Calculate the duration in seconds
    exam_duration_seconds = exam.duration * 60

    return render(request, "student_manage_exam/take_exam.html", {
        "exam": exam,
        "questions": questions,
        "exam_duration": exam_duration_seconds,
        "exam_id": exam_id  # Pass exam_id to the template context
    })




def available_exams(request):    
    student = Students.objects.get(admin=request.user.id)
    group_name = student.current_class
    student_group = Group.objects.filter(name=group_name).first()

    if student_group:
        current_time = timezone.now()

        # Exclude exams that are already completed by the student
        completed_exam_ids = StuExam_DB.objects.filter(student=student).values_list('qpaper__id', flat=True)
        available_exams = Exam_Model.objects.filter(
            Q(is_published=True),
            Q(group=student_group),
            Q(end_time__gt=current_time),
            ~Q(id__in=completed_exam_ids)
        )

        return render(request, "student_manage_exam/available_exams.html", {"available_exams": available_exams})
    else:
        return render(request, "student_manage_exam/available_exams.html", {"available_exams": None})


  
    
def exam_results(request):
    student = Students.objects.get(admin=request.user.id)
    completed_exams = StuExam_DB.objects.filter(student=student)
    results = StuResults_DB.objects.filter(student=student).first()
    
    context = {
        'completed_exams': completed_exams,
        'results': results
    }
    
    return render(request, 'student_manage_exam/exam_results_template.html', context) 
 



def exams(request):
    student = Students.objects.get(admin=request.user.id)
    studentExamsList = StuExam_DB.objects.filter(student=student)

    if request.method == 'POST' and not request.POST.get('papertitle', False):
        paper = request.POST['paper']
        stuExam = StuExam_DB.objects.get(examname=paper, student=student)
        qPaper = stuExam.qpaper
        examMain = Exam_Model.objects.get(name=paper)

        # TIME COMPARISON
        exam_start_time = examMain.start_time
        curr_time = timezone.now()

        if curr_time < exam_start_time:
            return redirect('exams:exams')  # Redirect to available exams page if the exam has already started

        # Clear existing questions
        stuExam.questions.all().delete()

        # Copy questions from question paper to student's exam record
        qPaperQuestionsList = qPaper.questions.all()
        for ques in qPaperQuestionsList:
            student_question = Stu_Question(
                question=ques.question, optionA=ques.optionA, optionB=ques.optionB,
                optionC=ques.optionC, optionD=ques.optionD,
                answer=ques.answer, student=student
            )
            student_question.save()
            stuExam.questions.add(student_question)
        stuExam.completed = 1
        stuExam.save()
        mins = examMain.duration
        secs = 0

        return render(request, 'student_manage_exam/take_exam.html', {
            'qpaper': qPaper, 'question_list': stuExam.questions.all(), 'student': student,
            'exam': paper, 'min': mins, 'sec': secs
        })

    elif request.method == 'POST' and request.POST.get('papertitle', False):
        paper = request.POST['paper']
        title = request.POST['papertitle']
        stuExam = StuExam_DB.objects.get(examname=paper, student=student)
        qPaper = stuExam.qpaper

        # Update selected answers and calculate score
        examQuestionsList = stuExam.questions.all()
        examScore = 0
        for ques in examQuestionsList:
            ans = request.POST.get(ques.question, False)
            if not ans:
                ans = "E"
            ques.choice = ans
            ques.save()
            if ans == ques.answer:
                examScore += 1

        stuExam.score = examScore
        stuExam.save()

        return render(request, 'student_manage_exam/result.html', {
            'Title': title, 'Score': examScore, 'students': student,
            'is_passed': stuExam.is_passed
        })

    return render(request, 'student_manage_exam/available_exams.html', {
        'students': student, 'paper': studentExamsList
    })
    

def results(request):
    student = Students.objects.get(admin=request.user.id)
    
    studentExamList = StuExam_DB.objects.filter(student=student, completed=1)

    if request.method == 'POST':
        paper = request.POST['paper']
        viewExam = StuExam_DB.objects.get(examname=paper, student=student)
        return render(request, 'student_manage_exam/individual_exam_result.html', {
            'exam': viewExam, 'students': student, 'quesn': viewExam.questions.all()
        })

    return render(request, 'student_manage_exam/exam_results_template.html', {
        'students': student, 'paper': studentExamList
    })
    

def view_exams_and_result(request):
    student = Students.objects.get(admin=request.user.id)

    group_name = student.current_class
    student_group = Group.objects.filter(name=group_name).first()

    examsList = []
    if student_group:
        stud_exams = Exam_Model.objects.filter(group=student_group)
        
        if stud_exams.exists():
            if stud_exams.count() > 1:
                for stud_exam in stud_exams:
                    examsList.append(stud_exam)
                    
            else:
                examsList.append(stud_exams.first())

    passed_exams = []
    failed_exams = []
    if examsList:
        for exam in examsList:
            currentExamList = StuExam_DB.objects.filter(examname=exam.name, student=student)

            if not currentExamList.exists():  # If no exams are there, add exams
                tempExam = StuExam_DB(student=student, examname=exam.name,
                                        qpaper=exam.question_paper, score=0, completed=0)
                tempExam.save()
                exam_question_paper = exam.question_paper
                questions_in_paper = exam_question_paper.questions.all()
                
                for ques in questions_in_paper:
                    # Add all the questions from the question paper to the student's database
                    studentQuestion = Stu_Question(question=ques.question, optionA=ques.optionA, optionB=ques.optionB,
                                                    optionC=ques.optionC, optionD=ques.optionD,
                                                    answer=ques.answer, student=student)
                    studentQuestion.save()
                    tempExam.questions.add(studentQuestion)
            
            current_exam = currentExamList.first()
            if current_exam and current_exam.is_passed:
                passed_exams.append(current_exam)
            elif current_exam:
                failed_exams.append(current_exam)

    return render(request, 'student_manage_exam/view_exam_result.html', {
        'students': student,
        'passed_exams': passed_exams,
        'failed_exams': failed_exams
    })
