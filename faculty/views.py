from django.shortcuts import render,redirect
from django.http import HttpResponse
from management.models import *
from .models import *
import os

# Create your views here.
def dashboard_page(request):
    user = User.objects.get(id=request.user.id)
    notice = get_notice()
    facultysubjectaccess = FacultySubjectAccess.objects.filter(user=user)

    courses = []

    for fac in facultysubjectaccess:
        course = fac.subject.semester.course
        if not course in courses:
            courses.append(course)

    context={
        'courses':courses,
        'notice':notice,
    }
    return render(request,'faculty/dashboard.html',context)

def accounts_page(request):
    user = User.objects.get(id=request.user.id)
    facultyuser = FacultyUser.objects.get(user=user)
    facultysubjectaccess = FacultySubjectAccess.objects.filter(user=user)
    
    context = {
        'facultyuser':facultyuser,
        'facultysubjectaccess':facultysubjectaccess,
    }
    return render(request,'faculty/accounts.html',context)

def logs_page(request):
    user = User.objects.get(id=request.user.id)
    logs = Log.objects.filter(user=user)
    
    context = {
        'logs':logs,
    }
    return render(request,'faculty/logs.html',context)


def semesters_page(request,course_id):
    user = User.objects.get(id=request.user.id)
    course = Course.objects.get(id=course_id)
    notice = get_notice()
    facultysubjectaccess = FacultySubjectAccess.objects.filter(user=user)
    semesters = []

    for fac in facultysubjectaccess:
        if not fac.subject.semester in semesters and fac.subject.semester.course == course:
            semesters.append(fac.subject.semester)

    context={
        'semesters':semesters,
        'course':course,
        'notice':notice,
    }
    return render(request,'faculty/semester.html',context)

def subjects_page(request,semester_id):    
    user = User.objects.get(id=request.user.id)
    semester = Semester.objects.get(id=semester_id)
    course = Course.objects.get(id=semester.course.id)
    notice = get_notice()
    facultysubjectaccess = FacultySubjectAccess.objects.filter(user=user)
    
    context={
        'course':course,
        'semester':semester,
        'facultysubjectaccess':facultysubjectaccess,
        'notice':notice,
    }
    return render(request,'faculty/subjects.html',context)

def studymaterials_page(request,subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
    except:
        return HttpResponse('Subject not found')
    if not is_faculty_subject_accessible(request,subject):
        error_message = 'Subject: '+subject.subject_name+' access is denied'
        return HttpResponse(error_message)
    
    notice = get_notice()
    semester = Semester.objects.get(id=subject.semester.id)
    course = Course.objects.get(id=semester.course.id)

    context={
        'subject':subject,
        'semester':semester,
        'course':course,
        'notice':notice,
    }
    return render(request,'faculty/studymaterials.html',context)

def resources_page(request,subject_id):
    subject = None
    try:
        subject = Subject.objects.get(id=subject_id)
    except:
        return HttpResponse('Subject not found')

    if not is_faculty_subject_accessible(request,subject):
        error_message = 'Subject: '+subject.subject_name+' access is denied'
        return HttpResponse(error_message)
    
    notice = get_notice()
    semester = Semester.objects.get(id=subject.semester.id)
    course = Course.objects.get(id=semester.course.id)
    resources = Resource.objects.filter(subject=subject)

    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        if keyword:
            resources = Resource.objects.filter(subject=subject,title__contains=keyword)
            print(resources)

    context={
        'subject':subject,
        'semester':semester,
        'course':course,
        'resources':resources,
        'notice':notice,

    }
    return render(request,'faculty/resources.html',context)

def addresources_page(request,subject_id):
    subject = None
    try:
        subject = Subject.objects.get(id=subject_id)
    except:
        return HttpResponse('Subject not found')

    if not is_faculty_subject_accessible(request,subject):
        error_message = 'Subject: '+subject.subject_name+' access is denied'
        return HttpResponse(error_message)

    semester = Semester.objects.get(id=subject.semester.id)
    course = Course.objects.get(id=semester.course.id)
    notice = get_notice()

    if request.method == 'POST':
        resource_title = request.POST.get('resource_title')
        resource_file = request.FILES.get('resource_file')

        print(resource_title,resource_file)

        try:
            resource = Resource.objects.create(title=resource_title,resource_file=resource_file,subject=subject)
        except:
            return HttpResponse('Not able to add resources, try again later')
        return redirect('faculty:resources_page',subject.id)
    
    context={
        'subject':subject,
        'semester':semester,
        'course':course,
        'notice':notice,
    }    
    return render(request,'faculty/addresources.html',context)

def syllabus_page(request,subject_id):
    subject = None
    try:
        subject = Subject.objects.get(id=subject_id)
    except:
        return HttpResponse('Subject not found')

    if not is_faculty_subject_accessible(request,subject):
        error_message = 'Subject: '+subject.subject_name+' access is denied'
        return HttpResponse(error_message)
    
    notice = get_notice()
    semester = Semester.objects.get(id=subject.semester.id)
    course = Course.objects.get(id=semester.course.id)

    if request.method == 'POST':
        syllabus_file = request.FILES.get('syllabus_file')
        syllabus = Syllabus.objects.update_or_create(subject=subject,defaults={'syllabus_file':syllabus_file})

    syllabus = None

    try:
        syllabus = Syllabus.objects.get(subject=subject)
    except:
        print('Data not found')

    context={
        'subject':subject,
        'semester':semester,
        'course':course,
        'syllabus':syllabus,
        'notice':notice,

    } 
    return render(request,'faculty/syllabus.html',context)

def videolectures_page(request,subject_id):
    subject = None
    try:
        subject = Subject.objects.get(id=subject_id)
    except:
        return HttpResponse('Subject not found')

    if not is_faculty_subject_accessible(request,subject):
        error_message = 'Subject: '+subject.subject_name+' access is denied'
        return HttpResponse(error_message)
    
    notice = get_notice()
    semester = Semester.objects.get(id=subject.semester.id)
    course = Course.objects.get(id=semester.course.id)
    videolectures = VideoLecture.objects.filter(subject=subject)

    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        print(keyword)

        if keyword:
            videolectures = VideoLecture.objects.filter(subject=subject,title__icontains=keyword)

    context={
        'subject':subject,
        'semester':semester,
        'course':course,
        'videolectures':videolectures,
        'notice':notice,
    }  
    return render(request,'faculty/videolectures.html',context)

def addvideolectures_page(request,subject_id):
    subject = None
    try:
        subject = Subject.objects.get(id=subject_id)
    except:
        return HttpResponse('Subject not found')

    if not is_faculty_subject_accessible(request,subject):
        error_message = 'Subject: '+subject.subject_name+' access is denied'
        return HttpResponse(error_message)

    notice = get_notice()
    semester = Semester.objects.get(id=subject.semester.id)
    course = Course.objects.get(id=semester.course.id)

    if request.method == 'POST':
        title = request.POST.get('videolecture_title')
        link = request.POST.get('videolecture_link')
        description = request.POST.get('videolecture_description')
        link = conv_video_into_embed_format(link)
        videolecture = VideoLecture.objects.create(title=title,video_link=link,description=description,subject=subject)
        return redirect('faculty:videolectures_page',subject.id)
    context={
        'subject':subject,
        'semester':semester,
        'course':course,
        'notice':notice,
    }
    return render(request,'faculty/addvideolectures.html',context)

def references_page(request,subject_id):
    subject = Subject.objects.get(id=subject_id)
    semester = Semester.objects.get(id=subject.semester.id)
    course = Course.objects.get(id=semester.course.id)
    references = Reference.objects.filter(subject=subject)
    notice = get_notice()

    if request.method == 'POST':
        title = request.POST.get('reference_title')
        link = request.POST.get('reference_link')
        description = request.POST.get('reference_description')
        reference = Reference.objects.create(title=title,link=link,description=description,subject=subject)

    context={
        'subject':subject,
        'semester':semester,
        'course':course,    
        'references':references, 
        'notice':notice,   
    }
    return render(request,'faculty/references.html',context)

def issues_page(request):
    notice = get_notice()

    context={
        'notice':notice,
    }

    if request.method == 'POST':
        issue = request.POST.get('issue')
        user = User.objects.get(id=request.user.id)
        try:
            issues = Issue.objects.create(user=user,issue=issue)
            context = {
                'success':1,
                'notice':notice,
            }
        except:
            return HttpResponse('Some error occurred while sending your response, kindly try again later.')
    return render(request,'faculty/issues.html',context)



# Functions
# Deleting functions

def delete_syllabus(request,syllabus_id):
    syllabus = Syllabus.objects.get(id=syllabus_id)
    subject = Subject.objects.get(id=syllabus.subject.id)
    os.remove(syllabus.syllabus_file.path)
    syllabus.delete()
    return redirect('faculty:syllabus_page',subject.id)

def delete_resources(request,resource_id):
    resources = Resource.objects.get(id=resource_id)
    subject = Subject.objects.get(id=resources.subject.id)
    os.remove(resources.resource_file.path)
    resources.delete()
    return redirect('faculty:resources_page',subject.id)

def delete_videolectures(request,videolecture_id):
    videolectures = VideoLecture.objects.get(id=videolecture_id)
    subject = Subject.objects.get(id=videolectures.subject.id)
    videolectures.delete()
    return redirect('faculty:videolectures_page',subject.id)

def delete_references(request,reference_id):
    references = Reference.objects.get(id=reference_id)
    subject = Subject.objects.get(id=references.subject.id)
    references.delete()
    return redirect('faculty:references_page',subject.id)


# Updating functions

def update_resources(request,resource_id):
    if request.method == 'POST':
        resource_title = request.POST.get('resource_title')
        resource = Resource.objects.get(id=resource_id)
        resources = Resource.objects.update_or_create(id=resource.id,defaults={'title':resource_title})
    
    return redirect('faculty:resources_page',resource.subject.id)

def update_videolectures(request,videolecture_id):
    if request.method == 'POST':
        title = request.POST.get('videolecture_title')
        description = request.POST.get('videolecture_description')
        videolecture = VideoLecture.objects.get(id=videolecture_id)
        videolectures = VideoLecture.objects.update_or_create(id=videolecture.id,defaults={'title':title,'description':description})
    
    return redirect('faculty:videolectures_page',videolecture.subject.id)

# Other functions
def is_faculty_subject_accessible(request,subject):
    user = User.objects.get(id=request.user.id)
    try:
        facultysubjectaccess = FacultySubjectAccess.objects.get(subject=subject,user=user)
        return True
    except:
        return False
    return False

def get_notice():
    try:
        notice = Notice.objects.all()
        return notice[0]
    except:
        return False

def conv_video_into_embed_format(string):
    print(string)

    code = string.split('youtu.be/')[1]
    main_str = 'https://youtube.com/embed/'+code
    print('result: ',main_str)
    return main_str