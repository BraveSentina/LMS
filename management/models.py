from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    date_of_birth = models.DateField(blank=True,null=True)
    is_faculty = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Department(models.Model):
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name

class Course(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name

class Semester(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    sem = models.CharField(max_length=100)

    def  __str__(self):
        return self.sem

class Subject(models.Model):
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subject_name

class FacultySubjectAccess(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Reference(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    link = models.CharField(max_length=500,null=True,blank=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Resource(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    resource_file = models.FileField(upload_to='files')
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)

    def __str__(self):
        return self.subject.subject_name

class Syllabus(models.Model):
    syllabus_file = models.FileField(upload_to='files')
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)

    def __str__(self):
        return self.subject.subject_name

class VideoLecture(models.Model):
    video_link = models.CharField(max_length=500,null=True,blank=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    
    def __str__(self):
        return self.video_link

class Issue(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    issue = models.CharField(max_length=500,null=True,blank=True)
    created_on = models.DateField(auto_now_add=True)
    is_solved = models.BooleanField(default=False)

    def __str__(self):
        return self.issue

class Notice(models.Model):
    notice = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.notice

class Maintenance(models.Model):
    is_ongoing = models.BooleanField(default=False)

    def __str__(self):
        return str(self.is_ongoing)

class Log(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    log = models.CharField(max_length=500,null=True,blank=True)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.log