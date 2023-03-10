from django.db import models
from management.models import *

# Create your models here.
class FacultyUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
