from django.shortcuts import render
from .models import *
from django.http import HttpResponse

# Create your views here.
def dashboard_page(request):
    subjects = None
    user = None
    sem = None
    course = None

    try:
        user = User.objects.get(username=request.user)
        studentuser = StudentUser.objects.get(user=user)
        print('success')

        sem = Semester.objects.get(id=studentuser.semester.id)
        course = Course.objects.get(id=sem.course.id)
        subjects = Subject.objects.filter(semester=sem)
    except:
        print('Error occurred while fetching')
    
    context = {
        'subjects':subjects,
    }
    return render(request,'student/dashboard.html',context)

def studymaterials_page(request,id):
    subject = Subject.objects.get(id=id)

    context = {
        'subject':subject,
    }
    return render(request,'student/studymaterials.html',context)

def resources_page(request,id):
    subject = Subject.objects.get(id=id)
    resources = Resource.objects.filter(subject=subject)

    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        if keyword:
            resources = Resource.objects.filter(subject=subject,title__contains=keyword)

    context = {
        'subject':subject,
        'resources':resources,
    }
    return render(request,'student/resources.html',context)

def syllabus_page(request,id):
    syllabus = None
    subject = Subject.objects.get(id=id)
    try:
        syllabus = Syllabus.objects.get(subject=subject)
    except:
        print('Syllabus not found')
    context = {
        'subject':subject,
        'syllabus':syllabus,
    }
    return render(request,'student/syllabus.html',context)

def videolectures_page(request,id):
    subject = Subject.objects.get(id=id)
    videolectures = VideoLecture.objects.filter(subject=subject)
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        if keyword:
            videolectures = VideoLecture.objects.filter(subject=subject,title__contains=keyword)
    
    context = {
        'subject':subject,
        'videolectures':videolectures,
    }
    return render(request,'student/videolectures.html',context)

def references_page(request,id):
    subject = Subject.objects.get(id=id)
    references = Reference.objects.filter(subject=subject)

    context = {
        'subject':subject,
        'references':references,
    }
    return render(request,'student/references.html',context)

def accounts_page(request):
    user = User.objects.get(id=request.user.id)
    studentuser = StudentUser.objects.get(user=user)
    context = {
        'user':user,
        'studentuser':studentuser,
    }
    return render(request,'student/accounts.html',context)

def logs_page(request):
    user = User.objects.get(id=request.user.id)
    logs = Log.objects.filter(user=user)
    
    context = {
        'logs':logs,
    }
    return render(request,'student/logs.html',context)

def issues_page(request):
    context={}
    if request.method == 'POST':
        issue = request.POST.get('issue')
        user = User.objects.get(id=request.user.id)
        try:
            issues = Issue.objects.create(user=user,issue=issue)
            context = {
                'success':1
            }
        except:
            return HttpResponse('Some error occurred while sending your response, kindly try again later.')
    return render(request,'student/issues.html',context)