from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from management.models import *
from django.db import IntegrityError
from student.models import StudentUser
from faculty.models import FacultyUser
# Create your views here.
def dashboard_page(request):
    notice = get_notice()
    context = {
        'notice':notice,
    }
    return render(request,'administrator/dashboard.html',context)

def accounts_page(request):
    user = User.objects.get(id=request.user.id)
    context = { 
        'user':user,
    }
    return render(request,'administrator/accounts.html',context)

def issues_page(request):
    issues = Issue.objects.filter(is_solved=False).order_by('-created_on')
    context = {
        'issues':issues,
    }
    return render(request,'administrator/issues.html',context)

def logs_page(request):
    user = User.objects.get(id=request.user.id)
    logs = Log.objects.filter(user=user)
    context = {
        'logs':logs,
    }
    return render(request,'administrator/logs.html',context)

def users_page(request):
    notice = get_notice()
    context = {
        'notice':notice,
    }
    return render(request,'administrator/users.html',context)

def addstudents_page(request):
    departments = None
    success = None
    error = None

    try:
        departments = Department.objects.all()
    except:
        return HttpResponse('Department not found')

    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        password = request.POST.get('password')
        semester = request.POST.get('semester')

        print(student_name,password,semester)
        try:
            user = User.objects.create_user(username=student_name,password=password,is_student=True)
            semester = Semester.objects.get(id=semester)
            student = StudentUser.objects.create(user=user,semester=semester)
            user.save()
            success = True
        except IntegrityError:
            error = True
        except:
            return HttpResponse('Unable to create user, kindly try again later')

    context={
        'departments':departments,
        'success':success,
        'error':error,
    }
    return render(request,'administrator/addstudents.html',context)

def addfaculties_page(request):
    departments = None
    success = False
    error = False
    try:
        departments = Department.objects.all()
    except:
        return HttpResponse('Departments not found')

    if request.method == 'POST':
        subjects = request.POST.getlist('subjects')
        faculty_name = request.POST.get('faculty_name')
        password = request.POST.get('password')
        department = request.POST.get('department')

        print(faculty_name,password,department)
        for s in subjects:
            print(s)    

        try:
            department = Department.objects.get(id=department)
            # Create the user
            user = User.objects.create_user(username=faculty_name,password=password,is_faculty=True)
            user.save()

            # Create the specific user
            facultyuser = FacultyUser.objects.create(user=user,department=department)

            for s in subjects:
                subject = Subject.objects.get(id=s)
                facultysubjectaccess = FacultySubjectAccess.objects.update_or_create(user=user,defaults={'subject':subject})
            success = True
        except IntegrityError:
            error = True
        except:
            return HttpResponse('Unable to create user')

        
    context={
        'departments':departments,
        'success':success,
        'error':error,
    }
    return render(request,'administrator/addfaculties.html',context)


def notice_page(request):
    notice = get_notice()

    if request.method == 'POST':
        notice_message = request.POST.get('notice')

        if notice:
            notice.notice = notice_message
            notice.save()
        else:
            notice = Notice.objects.create(notice=notice_message)
          
    context = {
        'notice':notice,
    }
    return render(request,'administrator/notice.html',context)

def maintenance_page(request):
    notice = get_notice()
    maintenance = get_maintenance()

    if request.method == 'POST':
        maintenance_status = request.POST.get('maintenance_status')

        if maintenance:
            if maintenance_status == 'on':
                maintenance.is_ongoing = True
                maintenance.save()
            else:
                maintenance.is_ongoing = False
                maintenance.save()
        else:
            if maintenance_status == 'on':
                maintenance = Maintenance.objects.create(is_ongoing=True)
            else:
                maintenance = Maintenance.objects.create(is_ongoing=False)
        
        return redirect('administrator:maintenance_page')

    context = {
        'notice':notice,
        'maintenance':maintenance,
    }
    return render(request,'administrator/maintenance.html',context)

def departments_page(request):
    notice = get_notice()
    departments = Department.objects.all()
    context = {
        'departments':departments,
        'notice':notice,
    }
    return render(request,'administrator/departments.html',context)

def adddepartments_page(request):
    notice = get_notice()
    if request.method == 'POST':
        department_name = request.POST.get('department_name')
        try:
            department = Department.objects.create(department_name=department_name)
        except:
            return HttpResponse('Unable to add department, kindly try again later')
        return redirect('administrator:departments_page')

    context={
        'notice':notice,
    }
    return render(request,'administrator/adddepartments.html',context)

def courses_page(request,department_id):
    notice = get_notice()
    department = Department.objects.get(id=department_id)
    courses = Course.objects.filter(department=department)

    context={
        'department':department,
        'courses':courses,
        'notice':notice,
    }
    return render(request,'administrator/courses.html',context)

def addcourses_page(request,department_id):
    notice = get_notice()
    department = Department.objects.get(id=department_id)
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        try:
            course = Course.objects.create(course_name=course_name,department=department)
        except:
            return HttpResponse('Unable to add course, kindly try again later')
        return redirect('administrator:courses_page',department.id)
    
    context={
        'notice':notice,
    }
    return render(request,'administrator/addcourses.html',context)

def semesters_page(request,course_id):
    notice = get_notice()
    course = Course.objects.get(id=course_id)
    semesters = Semester.objects.filter(course=course)

    context={
        'department':course.department,
        'course':course,
        'semesters':semesters,
        'notice':notice,
    }
    return render(request,'administrator/semesters.html',context)

def addsemesters_page(request,course_id):
    notice = get_notice()
    course = Course.objects.get(id=course_id)
    
    if request.method == 'POST':
        sem = request.POST.get('sem')
        try:
            semester = Semester.objects.create(sem=sem,course=course)
        except:
            return HttpResponse('Unable to add semester, kindly try again later')
        return redirect('administrator:semesters_page',course.id)
    context={
        'department':course.department,
        'course':course,
        'notice':notice,
    }
    return render(request,'administrator/addsemesters.html',context)

def subjects_page(request,semester_id):
    notice = get_notice()
    semester = Semester.objects.get(id=semester_id)
    subjects = Subject.objects.filter(semester=semester)

    context={
        'department':semester.course.department,
        'course':semester.course,
        'semester':semester,
        'notice':notice,
        'subjects':subjects,
    }
    return render(request,'administrator/subjects.html',context)

def addsubjects_page(request,semester_id):
    notice = get_notice()
    semester = Semester.objects.get(id=semester_id)
    subjects = Subject.objects.filter(semester=semester)

    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        try:
            subject = Subject.objects.create(subject_name=subject_name,semester=semester)
        except:
            return HttpResponse('Unable to add subject, kindly try again later')
        return redirect('administrator:subjects_page',semester.id)
    
    context={
        'department':semester.course.department,
        'course':semester.course,
        'semester':semester,
        'subjects':subjects,
        'notice':notice,
    }
    return render(request,'administrator/addsubjects.html',context)


# Delete functions
def delete_subjects(request,subject_id):
    subject = Subject.objects.get(id=subject_id)
    semester = subject.semester

    try:
        subject.delete()
    except:
        return HttpResponse('Unable to delete subject, kindly try again later')
    
    return redirect('administrator:subjects_page',semester.id)
    
def delete_semesters(request,semester_id):
    semester = Semester.objects.get(id=semester_id)
    course = Course.objects.get(id=semester.course.id)

    try:
        semester.delete()
    except:
        return HttpResponse('Unable to delete semester, kindly try again later')
    return redirect('administrator:semesters_page',course.id)

def delete_courses(request,course_id):
    course = Course.objects.get(id=course_id)
    department = Department.objects.get(id=course.department.id)

    try:
        course.delete()
    except:
        return HttpResponse('Unable to delete course, kindly try again later')
    return redirect('administrator:courses_page',department.id)

def delete_departments(request,department_id):
    department = Department.objects.get(id=department_id)

    try:
        department.delete()
    except:
        return HttpResponse('Unable to delete department, kindly try again later')
    return redirect('administrator:departments_page')



# Ajax functions
def get_courses_json(request):
    department_id = request.GET.get('department_id')
    department = Department.objects.get(id=department_id)
    courses = list(Course.objects.filter(department=department).values())
    return JsonResponse({'data':courses},safe=False)

def get_semesters_json(request):
    course_id = request.GET.get('course_id')
    course = Course.objects.get(id=course_id)
    semesters = list(Semester.objects.filter(course=course).values())
    return JsonResponse({'data':semesters},safe=False)

def get_subjects_json(request):
    semester_id = request.GET.get('semester_id')
    semester = Semester.objects.get(id=semester_id)
    subjects = list(Subject.objects.filter(semester=semester).values())
    return JsonResponse({'data':subjects},safe=False)

# Other functions
def get_notice():
    try:
        notice = Notice.objects.all()
        return notice[0]
    except:
        return False

def get_maintenance():
    try:
        maintenance = Maintenance.objects.all()
        return maintenance[0]
    except:
        return False

def set_issue_solved_to_true(request,issue_id):
    issue = Issue.objects.get(id=issue_id)
    issue.is_solved = True
    issue.save()
    return redirect('administrator:issues_page')

