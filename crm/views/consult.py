from django.shortcuts import render,redirect,HttpResponse,reverse
from crm import models
from crm.forms import ConsultForm
from django.views import View

from django.db.models import Q

from crm.utils.pagination import Pagination

from crm.utils.urls import reverse_url



class Consultlist(View):

    def get(self, request,customer_id):
        # query = request.GET.get('query', '')

        q = self.search([])
        if customer_id == '0':
            all_consult = models.ConsultRecord.objects.filter(q,delete_status=False,
                                                              consultant=request.user_obj).order_by('-date')

        else:
            all_consult = models.ConsultRecord.objects.filter(q,delete_status=False,
                                                              consultant=request.user_obj,customer_id=customer_id).order_by('-date')

        page = Pagination(request.GET.get('page'),request.GET.copy(),all_consult.count(),2)



        return render(request, 'consult_list.html',{'all_consult': all_consult[page.start:page.end], 'page_html': page.page_html})

    def post(self, request,customer_id):
        action = request.POST.get('action')

        if not hasattr(self, action):
            return HttpResponse('非法操作')
        getattr(self, action)()
        return self.get(request,customer_id)



    def search(self, filed_list):
        query = self.request.GET.get('query', '')
        # q = Q(Q(qq__contains=query) | Q(name__contains=query))
        q = Q()
        q.connector = 'OR'
        for field in filed_list:
            # q.children.append(Q(qq__contains=query))
            q.children.append(Q(('{}__contains'.format(field), query)))
        return q


def add_consult(request):
    obj = models.ConsultRecord(consultant=request.user_obj)

    form_obj = ConsultForm(instance=obj)

    if request.method == 'POST':
        form_obj = ConsultForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse_url(request,'consult_list'))

    return render(request,'add_consult.html',{'form_obj':form_obj})

def edit_consult(request,edit_id):
    obj = models.ConsultRecord.objects.filter(pk=edit_id).first()

    form_obj = ConsultForm(instance=obj)

    if request.method == 'POST':
        form_obj = ConsultForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse_url(request,'consult_list'))

    return render(request,'edit_consult.html',{'form_obj':form_obj})