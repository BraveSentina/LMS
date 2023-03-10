from django.urls import path
from .views import *

app_name = 'faculty'

urlpatterns = [
    path('',dashboard_page,name='dashboard_page'),
    path('accounts/',accounts_page,name='accounts_page'),
    path('logs/',logs_page,name='logs_page'),
    path('semesters/<str:course_id>/',semesters_page,name='semesters_page'),
    path('subjects/<str:semester_id>/',subjects_page,name='subjects_page'),
    path('studymaterials/<subject_id>/',studymaterials_page,name='studymaterials_page'),
    path('resources/<str:subject_id>/',resources_page,name='resources_page'),
    path('addresources/<str:subject_id>/',addresources_page,name='addresources_page'),
    path('syllabus/<str:subject_id>',syllabus_page,name='syllabus_page'),
    path('videolectures/<subject_id>/',videolectures_page,name='videolectures_page'),
    path('addvideolectures/<subject_id>/',addvideolectures_page,name='addvideolectures_page'),
    path('references/<str:subject_id>/',references_page,name='references_page'),
    path('issues/',issues_page,name='issues_page'),

    path('delete_syllabus/<str:syllabus_id>/',delete_syllabus,name='delete_syllabus'),
    path('delete_resources/<str:resource_id>/',delete_resources,name='delete_resources'),
    path('delete_videolectures/<str:videolecture_id>/',delete_videolectures,name='delete_videolectures'),
    path('delerte_references/<str:reference_id>/',delete_references,name='delete_references'),

    path('update_resources/<str:resource_id>/',update_resources,name='update_resources'),
    path('update_videolectures/<str:videolecture_id>/',update_videolectures,name='update_videolectures'),
]