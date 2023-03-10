from django.urls import path
from .views import *

app_name = 'administrator'

urlpatterns = [
    path('',dashboard_page,name='dashboard_page'),
    path('accounts/',accounts_page,name='accounts_page'),
    path('issues/',issues_page,name='issues_page'),
    path('logs/',logs_page,name='logs_page'),
    path('users/',users_page,name='users_page'),
    path('addstudents/',addstudents_page,name='addstudents_page'),
    path('addfaculties/',addfaculties_page,name='addfaculties_page'),

    path('notice/',notice_page,name='notice_page'),
    path('maintenance/',maintenance_page,name='maintenance_page'),
    path('departments/',departments_page,name='departments_page'),
    path('adddepartments/',adddepartments_page,name='adddepartments_page'),
    path('courses/<str:department_id>/',courses_page,name='courses_page'),
    path('addcourses/<str:department_id>/',addcourses_page,name='addcourses_page'),
    path('semesters/<str:course_id>/',semesters_page,name='semesters_page'),
    path('addsemesters/<course_id>/',addsemesters_page,name='addsemesters_page'),
    path('subjects/<str:semester_id>/',subjects_page,name='subjects_page'),
    path('addsubjects/<str:semester_id>/',addsubjects_page,name='addsubjects_page'),

    path('delete_subjects/<str:subject_id>/',delete_subjects,name='delete_subjects'),
    path('delete_semesters/<str:semester_id>/',delete_semesters,name='delete_semesters'),
    path('delete_courses/<str:course_id>/',delete_courses,name='delete_courses'),
    path('delete_departments/<str:department_id>/',delete_departments,name='delete_departments'),
    
    path('get_courses_json/',get_courses_json,name='get_courses_json'),
    path('get_semesters_json/',get_semesters_json,name='get_semesters_json'),
    path('get_subjects_json/',get_subjects_json,name='get_subjects_json'),

    path('set_issue_solved_to_true/<str:issue_id>/',set_issue_solved_to_true,name='set_issue_solved_to_true'),

]



