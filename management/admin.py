from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email',)
    ordering = ('email',)
    list_display = ('email','username','date_of_birth','last_login','is_activated','is_superuser', 'is_staff', 'is_faculty',
                    'is_student','is_active')
    list_filter = ('is_active', 'is_faculty',
                   'is_student','is_superuser','is_activated')

    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',
                                    'is_faculty', 'is_student', 'is_activated','is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email','password1', 'password2', 'is_staff', 'is_superuser', 'is_faculty', 'is_student','is_activated', 'is_active')
        }),
    )


admin.site.register(User,UserAdminConfig)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Semester)
admin.site.register(Reference)
admin.site.register(Resource)
admin.site.register(Syllabus)
admin.site.register(VideoLecture)
admin.site.register(Issue)
admin.site.register(Notice)
admin.site.register(Maintenance)
admin.site.register(FacultySubjectAccess)
admin.site.register(Log)