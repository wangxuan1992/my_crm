from django.shortcuts import render,redirect,HttpResponse,reverse
from crm import models
from crm.forms import RegForm
import hashlib


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
