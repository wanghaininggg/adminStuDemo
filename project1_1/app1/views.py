from django.shortcuts import render,redirect,HttpResponse
from . import models
# Create your views here.

def index(request):

    return render(request, 'index.html')

def login(request):

    if request.session.get('is_login', None):
        return redirect('index')

    message = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('password')
        
        try:
            user = models.Student.objects.get(studentname=name)
            if pwd == user.studentpassword:
                request.session['is_login'] = True
                request.session['user_name'] = name
                return redirect('index')
            else:
                message = '密码错误'
        except:
            message = '用户名不存在'
        return render(request, 'login.html', locals())
    return render(request, 'login.html', locals())


def classes(request):

    if request.method == 'POST':
        import json
        """
        classId2 = request.POST.get('classId')
        className2 = request.POST.get('className')
        models.Classes.objects.create(classId = classId2, className= className2)
        return redirect('classes')
        """
        response_dict = {'status':True, 'error':None, 'data': None, 'write':False}
        classId2 = request.POST.get('classId', None)
        className2 = request.POST.get('className', None)

        if classId2 and className2:
            obj = models.Classes.objects.create(classId=classId2, className=className2)
            response_dict['data'] = {'id':obj.id, 'classId':obj.classId, 'className':obj.className}
        else:
            response_dict['status'] = False
            response_dict['error'] = '内容不能为空'
        return HttpResponse(json.dumps(response_dict))


    # for i in range(100):
    #     models.Classes.objects.create(classId='%s'%i, className='云南师范大学%s班'%i)


    # 分页
    current_page = int(request.GET.get('p', 1))  # 当前页
    total_number = models.Classes.objects.all().count()  # 所有数据的个数
    obj = PagerHelper(total_number, current_page)
    pager = obj.page_str()

    classe = models.Classes.objects.all()[obj.page_start:obj.page_end]

    return render(request, 'class.html', {'classe':classe, 'page_list':pager})

def student(request):
    

    if request.method == 'POST':
        # from 提交
        # files = request.FILES.get('img')
        # import os
        # # p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # p = os.path.join('static', 'images', files.name)
        # models.Images.objects.create(imagesUrl=p)
        # with open(p, 'wb') as f:
        #     for i in files.chunks():
        #         f.write(i)
        # return render(request, 'student.html', {'url':p})

        # Ajax提交
        # files = request.FILES.get('img')
        # import os
        # import json
        # p = os.path.join('static', 'images', files.name)
        # models.Images.objects.create(imagesUrl=p)
        # with open(p, 'wb') as f:
        #     for i in files.chunks():
        #         f.write(i)
        # dic = {'status':True, 'files':p}
        # return HttpResponse(json.dumps(dic))

        img = request.FILES.get('file')
        import os
        p = os.path.join('static', 'images', img.name)
        models.Images.objects.create(imagesUrl = p)
        with open(p, 'wb') as f:
            for i in img.chunks():
                f.write(i)
        return HttpResponse(p)
    
    return render(request, 'student.html')


def teacher(request):
    # obj = models.Teacher.objects.filter(teacherName__startswith='42')
    # for i in obj:
    #     print(i.id, i.teacherName, i.teacherPassword, i.date)

    # classe = models.Classes.objects.get(id=586)     #多对多添加
    # obj = models.Teacher.objects.get(id=6)
    # obj.classes.add(classe)

    # class1 = models.Classes.objects.get(id = 600)    #一对多添加
    # obj = models.Student(studentname='whn', studentpassword='123456')
    # obj.studentClass = class1
    # obj.save()
    # models.Student.objects.create(studentname='whn', studentpassword='whn123', studentClass=class1)

    # print(models.Teacher.objects.get(id=6).classes.all().count())   //多对多查找 有条件的那个
    # print(models.Classes.objects.get(id=570).xxx.all().values('id', 'teacherName'))  //多对多查找 无字段那个

    # print(models.Student.objects.filter(studentClass__gt = 580).values_list('studentname', 'studentpassword'))

    # obj = models.Student.objects.filter(studentClass__className__gt = 500)
    # for i in obj:
    #     print(i.studentClass.className)
   
    # obj = models.Classes.objects.filter(student__studentname__contains = 'wh')
    # for i in obj:
    #    print(i.id, i.student_set.all().values(
    #        'id', 'studentname', 'studentpassword'))
    objs = models.Teacher.objects.all()

    return render(request, 'teacher.html', {'objs':objs})
    

class PagerHelper:


    def __init__(self, total_number, current_page, item_numer=10):
        self.total_number = total_number
        self.current_page = current_page
        self.item_number= item_numer
    
    @property
    def page_start(self):
        start = (self.current_page - 1) * self.item_number # 当前页展示数据的行
        return start

    @property
    def page_end(self):
        end = self.current_page * self.item_number # 当前页展示数据的尾行
        return end
        
    def page_str(self):
     
        v, a = divmod(self.total_number, self.item_number) # 计算总共有多少个页码
        if a != 0:
            v += 1

        pager_list = []
        if self.current_page != 1:
            pager_list.append(
                '''<a href="/classes?p=%s" class="list_up">上一页</a>''' % (self.current_page - 1))

        if v <= 9:
            start_page = 1
            end_page = v+1
        else:
            if self.current_page < 5:
                start_page = 1
                end_page = 10
            elif self.current_page > v-4:
                start_page = v - 8
                end_page = v+1
            else:
                start_page = self.current_page - 4
                end_page = self.current_page + 5

        for i in range(start_page, end_page):
            if i == self.current_page:
                pager_list.append(
                    '''<a href="/classes?p=%s" class="active">%s</a>''' % (i, i))
            else:
                pager_list.append('''<a href="/classes?p=%s">%s</a>''' % (i, i))
        if self.current_page != v:
            pager_list.append(
                '''<a href="/classes?p=%s" class="list_down">下一页</a>''' % (self.current_page + 1))
        pager = ''.join(pager_list)
         
        return pager
