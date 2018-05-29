from django.db import models

# Create your models here.


class Classes(models.Model):

    classId = models.CharField('班级编号', max_length=20)
    className = models.CharField('班级名称', max_length=20)

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = '班级'

    def __str__(self):
        return str(self.id)


class Student(models.Model):

    studentname = models.CharField("姓名", max_length=20)
    studentpassword = models.CharField("密码", max_length=20)
    studentClass = models.ForeignKey(Classes, verbose_name='班级', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = '学生'

    def __str__(self):
        return str(self.id)

class Images(models.Model):

    imagesUrl = models.CharField("图片路径", max_length=200)

    class Meta:

        verbose_name = '图片'
        verbose_name_plural = '图片'


class Teacher(models.Model):

    teacherName = models.CharField("姓名", max_length=20)
    teacherPassword = models.CharField("密码", max_length=20)
    classes = models.ManyToManyField('Classes' ,related_name='xxx')
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师'
        db_table = 'teacherUser'

    def __str__(self):
        return str(self.id)
        