from django.shortcuts import render,redirect,HttpResponse,reverse
from crm import models
from crm.forms import RegForm
import hashlib

from crm.utils.pagination import Pagination


def register(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('login'))


    return render(request,'register.html',{'form_obj':form_obj})

def login(request):
    if request.method == "POST":
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        pwd = md5.hexdigest()

        user_obj = models.UserProfile.objects.filter(username=user,password=pwd,is_active=True).first()
        if user_obj:
            return redirect(reverse("index"))
        else:
            return HttpResponse("PASSWORD NOT OK")
    return render(request,'login.html')

def index(request):
    return HttpResponse('this is index')

def customer_list(request):
    all_customer = models.Customer.objects.all()
    return render(request,'customer_list.html',{'all_customer':all_customer})

users = [{'name':'alex-{}'.format(i),'pwd':'dsb-{}'.format(i)} for i in range(1,302)]

# def user_list(request):
#     page_num = request.GET.get('page')
#     try:
#         page_num = int(page_num)
#         if page_num <= 0:
#             page_num = 1
#     except Exception as e:
#         page_num = 1
#
#     per_num = 15  #每页展示数量
#
#     start = (page_num - 1) * per_num
#     end = page_num * per_num
#
#
#     totil_page_num,more = divmod(all(users),per_num)
#     if more:
#         totil_page_num += 1
#
#
#
#     return render(request,'user_list.html',{'users':users[start:end],'totil_page_num':range(1,totil_page_num+1)})

def user_list(request):
    page = Pagination(request.GET.get('page'),len(users))
    print(users[page.start:page.end])
    print(page.page_html)

    return render(request,'user_list.html',{'users':users[page.start:page.end],'page_html':page.page_html})

