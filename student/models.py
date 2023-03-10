from django.db import models
from management.models import *

# Create your models here.
class StudentUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
