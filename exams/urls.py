from django.urls import path
from . import views

urlpatterns = [
    # Define your URL patterns here
    # For example:
    path('add-question-save/', views.add_question_save, name='add_question_save'),
    path('add_exam_model/', views.add_exam_model, name='add_exam_model'),
    path('add-question/', views.add_question, name='add_question'),
    path('add-question-paper/', views.add_question_paper, name='add_question_paper'),
    path('add-question-paper-save/', views.add_question_paper_save, name='add_question_paper_save'),
    path('get-questions/', views.get_questions, name='get_questions'),
        # URL for fetching student groups
    path('get_student_groups/', views.get_student_groups, name='get_student_groups'),

    # URL for fetching subjects
    path('get_subjects/', views.get_subjects, name='get_subjects'),

    # URL for fetching question papers
    path('get_question_papers/', views.get_question_papers, name='get_question_papers'),

    # URL for saving the exam
    path('add_exam_save/', views.add_exam_save, name='add_exam_save'),
    # path('some-url/', views.some_view_function, name='some-view'),
    path('question/list/', views.question_list, name='question_list'),
    path('question/edit/<int:qno>/', views.question_edit, name='question_edit'),
    path('handle_action/', views.handle_action, name='handle_action'),
    path('edit_question/<int:qno>/', views.edit_question_save, name='edit_question_save'),
    path('publish_exam/', views.publish_exam, name='publish_exam'),
    path('exams/', views.exams_list, name='exams_list'),
    path('question_papers_list/', views.question_papers_list, name='question_papers_list'),
    path('edit_question_paper/<int:q_paper_id>/', views.edit_question_paper, name='edit_question_paper'),
    path('delete_question_paper/', views.delete_question_paper, name='delete_question_paper'),
    path('edit-question-save/<int:qno>/', views.edit_question_save, name='edit_question_save'),
    path('edit_question_paper_save/<int:q_paper_id>/', views.edit_question_paper_save, name='edit_question_paper_save'),
    path('exams/edit/<int:exam_id>/', views.edit_exam_model, name='edit_exam_model'),    
    path('view/<int:exam_id>/', views.view_exam_model, name='view_exam_model'),
    path('delete_exam/', views.delete_exam_model, name='delete_exam_model'),
    path('edit_exam/<int:exam_id>/save/', views.edit_exam_save, name='edit_exam_save'),
    # path('available_exams/', views.available_exams, name='available_exams'),
    # path('take_exam/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('get_published_exam_count/', views.get_published_exam_count, name='get_published_exam_count'),
    path('exams', views.exams, name='exams'),
    # path('exam_results/', views.exam_results, name='exam_results'),
    path('results', views.results, name='results'),
    path('view_exams_and_result', views.view_exams_and_result, name='view_exams_and_result'),
    
]