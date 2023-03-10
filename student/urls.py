from django.urls import path
from .views import *

app_name = "student"

urlpatterns =[
    path('',dashboard_page,name='dashboard_page'),
    path('studymaterials/<str:id>/',studymaterials_page,name='studymaterials_page'),
    path('resources/<str:id>/',resources_page,name='resources_page'),
    path('syllabus/<str:id>/',syllabus_page,name='syllabus_page'),
    path('videolectures/<str:id>/',videolectures_page,name='videolectures_page'),
    path('references/<str:id>/',references_page,name='references_page'),
    path('accounts/',accounts_page,name='accounts_page'),
    path('logs/',logs_page,name='logs_page'),
    path('issues/',issues_page,name='issues_page'),

] 