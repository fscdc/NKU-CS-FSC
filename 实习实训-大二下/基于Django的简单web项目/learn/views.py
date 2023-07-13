from django.shortcuts import render
from django.http import HttpResponse
from .models import Userdetail
from .models import User
from django.shortcuts import redirect
import pymysql
# Create your views here.
connect = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='12345678',
            db='homework',
            port=3306,
            charset="utf8"
        )
def welcome(request,id):
    ruser=User.objects.get(id=id)
    ruserdetail=Userdetail.objects.get(User_id=id)
    return HttpResponse('Welcome,{},Have a nice day!</br>详细信息：</br>birth_date:{}</br>email:{}</br>address:{}</br>profile:{}'.format(ruser.name,ruserdetail.birth_date,ruserdetail.email,ruserdetail.address,ruserdetail.profile))
def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        with connect.cursor() as cursor:
            # 使用原生SQL查询
            cursor.execute("SELECT * FROM learn_user WHERE name = %s and password=%s", [name,password])
            row = cursor.fetchone()
        if row is not None:
            id_value = row[0]
            response=redirect('http://127.0.0.1:8000/welcome/{}/'.format(id_value))            
            response.set_cookie('name', name.encode('utf-8'), max_age=3000, path='/learn/')
            response.set_cookie('password', password.encode('utf-8'), max_age=3000, path='/learn/')
            return response
        else:
            error_message = '用户名或密码错误'
    else:
        name = request.COOKIES.get('name')
        password = request.COOKIES.get('password')
        with connect.cursor() as cursor:
            # 使用原生SQL查询
            cursor.execute("SELECT * FROM learn_user WHERE name = %s and password=%s", [name,password])
            row = cursor.fetchone()
        if row is not None:
            id_value =row[0]
            return redirect('http://127.0.0.1:8000/welcome/{}/'.format(id_value))
        else:
            error_message = '自动登录失败，请手动登录'
    return render(request, 'learn/login.html',{'错误信息：': error_message})

def register(request):
    if request.method=="POST":
        name = request.POST.get('name')
        password = request.POST.get('password')
        birth_date = request.POST.get('birth_date')
        email = request.POST.get('email')
        address = request.POST.get('address')
        profile = request.POST.get('profile')
        
                # 创建User实例
        user =User(name=name, password=password)
        user.save()
        
        # 创建UserDetails实例
        userdetail = Userdetail(birth_date=birth_date, email=email, address=address,profile=profile,User=user)
        userdetail.save()
        return redirect('http://127.0.0.1:8000/learn/login/')
    return render(request, 'learn/register.html')
