from django.contrib import admin
from . import models
# Register your models here.

class ClassesAdmin(admin.ModelAdmin):
    list_display = ('classId', 'className')

admin.site.register(models.Classes, ClassesAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('studentname', 'studentpassword', 'studentClass')

admin.site.register(models.Student, StudentAdmin)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacherName', 'teacherPassword', 'date')

admin.site.register(models.Teacher, TeacherAdmin)    

class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'imagesUrl')

admin.site.register(models.Images, ImagesAdmin)

