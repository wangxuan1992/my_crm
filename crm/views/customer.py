from django.shortcuts import render,redirect,HttpResponse,reverse
from crm import models
from crm.forms import CustomerForm
from django.views import View

from django.db.models import Q

from crm.utils.pagination import Pagination

from crm.utils.urls import reverse_url

from django.db import transaction
from django.conf import settings


# def customer_list(request):
#     if request.path_info == reverse('customer_list'):
#         all_customer = models.Customer.objects.filter(consultant__isnull=True)
#     else:
#         all_customer = models.Customer.objects.filter(consultant=request.user_obj)
#
#     return render(request,'customer_list.html',{'all_customer':all_customer})

class Customerlist(View):

    def get(self,request):
        # query = request.GET.get('query', '')

        q = self.search(['qq', 'name', 'date'])
        if request.path_info == reverse('customer_list'):
            all_customer = models.Customer.objects.filter(q,consultant__isnull=True)
        else:
            all_customer = models.Customer.objects.filter(consultant=request.user_obj)

        page = Pagination(request.GET.get('page'),request.GET.copy(),all_customer.count(),4)

        return render(request, 'customer_list.html', {'all_customer': all_customer[page.start:page.end],'page_html':page.page_html})

    def post(self,request):
        action = request.POST.get('action')

        if not hasattr(self,action):
            return HttpResponse('非法操作')
        ret = getattr(self,action)()
        if ret:
            return ret
        return self.get(request)


    def multi_apply(self):
        # 公户变私户
        ids = self.request.POST.getlist('ids')

        # 设置销售的客户上限
        if self.request.user_obj.customers.count() + len(ids) > settings.MAX_CUSTOMER_NUM:
            return HttpResponse('做人不要太贪心，给队友留点')

        # 方式一
        with transaction.atomic():
            queryset = models.Customer.objects.filter(pk__in=ids,consultant__isnull=True).select_for_update()
            if len(ids) == queryset.__len__():
                queryset.update(consultant=self.request.user_obj)
                return
            return HttpResponse('您选中的客户，应该已被其他用户领走')


        # 方式二
        # self.request.user_obj.customers.add(*models.Customer.objects.filter(pk__in=ids))

    def multi_pub(self):
        # 私户变公户
        ids = self.request.POST.getlist('ids')
        # 方式一
        # models.Customer.objects.filter(pk__in=ids).update(consultant=None)

        # 方式二
        self.request.user_obj.customers.remove(*models.Customer.objects.filter(pk__in=ids))

    def search(self, filed_list):
        query = self.request.GET.get('query', '')
        # q = Q(Q(qq__contains=query) | Q(name__contains=query))
        q = Q()
        q.connector = 'OR'
        for field in filed_list:
            # q.children.append(Q(qq__contains=query))
            q.children.append(Q(('{}__contains'.format(field), query)))
        return q


# def add_customer(request):
#     form_obj = CustomerForm()
#     if request.method == 'POST':
#         form_obj = CustomerForm(request.POST)
#         if form_obj.is_valid():
#             form_obj.save()
#             return redirect('customer_list')
#
#     return render(request,'add_customer.html',{'form_obj':form_obj})
#
# def edit_customer(request,edit_id):
#     obj = models.Customer.objects.filter(pk=edit_id).first()
#     form_obj = CustomerForm(instance=obj)
#     if request.method == 'POST':
#         form_obj = CustomerForm(request.POST,instance=obj)
#         if form_obj.is_valid():
#             form_obj.save()
#             return redirect(reverse('customer_list'))
#
#     return render(request,'edit_customer.html',{'form_obj':form_obj})

def customer_change(request,edit_id=None):
    obj = models.Customer.objects.filter(pk=edit_id).first()
    form_obj = CustomerForm(instance=obj)
    title = '编辑客户' if edit_id else '新增客户'
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()


            return redirect(reverse_url(request,'customer_list'))

    return render(request, 'customer_change.html', {'form_obj': form_obj,'title':title})

