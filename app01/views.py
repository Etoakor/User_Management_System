# Create your views here.
from django.shortcuts import render,redirect,HttpResponse
from app01 import models
def login(request):
    message = ""
    v = request.session
    print(type(v))
    from django.contrib.sessions.backends.db import SessionStore
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        c = models.Administrator.objects.filter(username=user, password=pwd).count()
        if c:
            request.session['is_login'] = True
            request.session['username'] = user
            rep = redirect('/index.html')
            return rep
        else:
            message = "用户名或密码错误"
    obj = render(request,'login.html', {'msg': message})
    return obj

def logout(request):
    request.session.clear()
    return redirect('/login.html')


def auth(func):
    def inner(request, *args, **kwargs):
        is_login = request.session.get('is_login')
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect('/login.html')
    return inner

@auth
def index(request):
    current_user = request.session.get('username')
    return render(request, 'index.html',{'username': current_user})
@auth
def handle_classes(request):
   if request.method == "GET":
       # 当前页
       current_page = request.GET.get('p',1)
       current_page = int(current_page)
       # 所有数据的个数
       total_count = models.Classes.objects.all().count()
       from utils.page import PagerHelper
       obj = PagerHelper(total_count, current_page, '/classes.html',5)
       pager = obj.pager_str()
       cls_list = models.Classes.objects.all()[obj.db_start:obj.db_end]
       current_user = request.session.get('username')
       return render(request,
                     'classes.html',
                     {'username': current_user, 'cls_list': cls_list, 'str_pager': pager})

   elif request.method == "POST":
       # Form表单提交的处理方式
       """
       caption = request.POST.get('caption',None)
       if caption:
           models.Classes.objects.create(caption=caption)
       return redirect('/classes.html')
       """
       # Ajax
       import json
       response_dict = {'status': True, 'error': None, 'data': None}
       caption = request.POST.get('caption', None)
       print(caption)
       if caption:
           obj = models.Classes.objects.create(caption=caption)
           response_dict['data'] = {'id': obj.id, 'caption': obj.caption}
       else:
           response_dict['status'] = False
           response_dict['error'] = "标题不能为空"
       return HttpResponse(json.dumps(response_dict))

@auth
def handle_add_classes(request):
   message = ""
   if request.method == "GET":
       return render(request, 'add_classes.html', {'msg': message})
   elif request.method == "POST":
       caption = request.POST.get('caption',None)
       if caption:
           models.Classes.objects.create(caption=caption)
       else:
           message = "标题不能为空"
           return render(request, 'add_classes.html', {'msg': message})
       return redirect('/classes.html')
   else:
       return redirect('/index.html')

@auth
def handle_edit_classes(request):
   if request.method == "GET":
       nid = request.GET.get('nid')
       obj = models.Classes.objects.filter(id=nid).first()
       return render(request, 'edit_classes.html', {'obj': obj})
   elif request.method == "POST":
       nid = request.POST.get('nid')
       caption = request.POST.get('caption')
       models.Classes.objects.filter(id=nid).update(caption=caption)
       return redirect('/classes.html')
   else:
       return redirect('/index.html')
@auth
def handle_del_classes(request):
   nid = request.GET.get('nid')
   a = models.Classes.objects.get(id=nid).delete();
   return redirect('/classes.html')
@auth
def handle_student(request):
   if request.method == "GET":
       # for i in range(10):
       #     models.Student.objects.create(name='root' + str(i),
       #                                   email='root@live.com' + str(i),
       #                                   cls_id=i)
       result = models.Student.objects.all()
       current_user = request.session.get('username')
       return render(request, 'student.html', {'username': current_user,'result': result})
   elif request.method == "POST":
       return redirect('/index.html')
   else:
       return redirect('/index.html')

@auth
def add_student(request):
   if request.method == "GET":
       cls_list = models.Classes.objects.all()
       return render(request, 'add_student.html',{"cls_list":cls_list})
   elif request.method == "POST":
       name = request.POST.get('name')
       email = request.POST.get('email')
       cls_id = request.POST.get('cls_id')
       models.Student.objects.create(name=name,email=email,cls_id=cls_id)
       return redirect('/student.html')
@auth
def edit_student(request):
   if request.method == "GET":
       cls_list = models.Classes.objects.all()[0: 20]
       nid = request.GET.get('nid')
       obj = models.Student.objects.get(id=nid)
       return render(request, 'edit_student.html', {'cls_list': cls_list, "obj": obj})
   elif request.method == "POST":
       nid = request.POST.get('id')
       name = request.POST.get('name')
       email = request.POST.get('email')
       cls_id = request.POST.get('cls_id')
       models.Student.objects.filter(id=nid).update(name=name,email=email,cls_id=cls_id)
       return redirect('/student.html')
@auth
def handle_teacher(request):
   # FBV,CBV
   current_user = request.session.get('username')

   # teacher_list = models.Teacher.objects.all()
   # for obj in teacher_list:
   #     print(obj.id,obj.name,obj.cls.all())

   # teacher_list = models.Teacher.objects.filter(id__in=models.Teacher.objects.all()[0:5]).values('id','name','cls__id','cls__caption')
   teacher_list = models.Teacher.objects.values('id','name','cls__id','cls__caption')
      #构造数据结构
   result = {}
   for t in teacher_list:
       # print(t['id'],t['name'],t['cls__id'],t['cls__caption'])
       if t['id'] in result:
           if t['cls__id']:
               result[t['id']]['cls_list'].append({'id':t['cls__id'], 'caption': t['cls__caption'] })
       else:
           if t['cls__id']:
               temp = [{'id': t['cls__id'], 'caption': t['cls__caption']},]
           else:
               temp = []
           result[t['id']] = {
               'nid': t['id'],
               'name': t['name'],
               'cls_list': temp
           }
   # result = {
   #     1: {
   #         'nid': 1,
   #         'name': '仓夜空',
   #         'cls_list':[
   #             {'id': 1, 'caption': "python最牛逼"},
   #             {'id': 2, 'caption': "java最牛逼"}
   #         ]
   #     },
   #     2: {
   #         'nid': 2,
   #         'name': '经夜空1',
   #         'cls_list': [
   #             {'id': 1, 'caption': "全栈二班最牛逼"},
   #             {'id': 5, 'caption': "阿萨德发生地方"}
   #         ]
   #     }
   # }
   return render(request, 'teacher.html', {'username': current_user, "teacher_list": result})
def add_teacher(request):
   if request.method == 'GET':
       cls_list = models.Classes.objects.all()
       return render(request, 'add_teacher.html', {'cls_list': cls_list})
   elif request.method == "POST":
       name = request.POST.get('name')
       cls = request.POST.getlist('cls')
       # print(name,cls)
       # 创建老师
       obj = models.Teacher.objects.create(name=name)
       # 创建老师和班级的对应关系
       obj.cls.add(*cls)
       return redirect('/teacher.html')
def edit_teacher(request,nid):
   # 获取当前老师信息
   # 获取当前老师对应的所有班级
   # - 获取所有的班级
   # - 获取当前老师未对应的所有班级
   if request.method == "GET":
       # 当前老师的信息
       obj = models.Teacher.objects.get(id=nid)
       # 获取当前老师已经管理的所有班级
       # [ (1,"root1"),(2,"root2"),(3,"root3"),]
       obj_cls_list = obj.cls.all().values_list('id', 'caption')
       # 已经管理的班级的ID列表
       id_list = list(zip(*obj_cls_list))[0] if obj_cls_list else []
       print(id_list)
       # # [1,2,3]
       # 获取不包括已经管理的班级，
       # cls_list = models.Classes.objects.filter(id__in=id_list)
       cls_list = models.Classes.objects.exclude(id__in=id_list)
       # # 1
       return render(request, 'edit_teacher.html', {'obj': obj,"obj_cls_list": obj_cls_list,"cls_list":cls_list})
   elif request.method == "POST":
       # nid = request.POST.get('nid')
       name = request.POST.get('name')
       cls_li = request.POST.getlist('cls')
       obj = models.Teacher.objects.get(id=nid)
       obj.name = name
       obj.save()
       obj.cls.set(cls_li)
       return redirect('/teacher.html')