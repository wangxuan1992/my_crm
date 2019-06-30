from django.shortcuts import render,redirect,HttpResponse,reverse
from crm import models
from crm.forms import EnrollmentForm
from django.views import View

from django.db.models import Q

from crm.utils.pagination import Pagination

from crm.utils.urls import reverse_url


class Enrollmentlist(View):

    def get(self, request):
        q = self.search([])
        all_enrollment = models.Enrollment.objects.filter(q,delete_status=False,
                                                       customer_id__in=[i.pk for i in request.user_obj.customers.all()])

        page = Pagination(request.GET.get('page'),request.GET.copy(),all_enrollment.count(),10)
        return render(request, 'enrollment_list.html',{'all_enrollment': all_enrollment[page.start:page.end],'page_html': page.page_html})

    def post(self, request):
        action = request.POST.get('action')

        if not hasattr(self, action):
            return HttpResponse('非法操作')
        getattr(self, action)()
        return self.get(request)



    def search(self, filed_list):
        query = self.request.GET.get('query', '')
        # q = Q(Q(qq__contains=query) | Q(name__contains=query))
        q = Q()
        q.connector = 'OR'
        for field in filed_list:
            # q.children.append(Q(qq__contains=query))
            q.children.append(Q(('{}__contains'.format(field), query)))
        return q


def enrollment_change(request,customer_id=None, enrollment_id=None):

    obj = models.Enrollment.objects.filter(pk=enrollment_id).first() if enrollment_id else models.Enrollment(
        customer_id=customer_id)

    form_obj = EnrollmentForm(instance=obj)
    if request.method == 'POST':
        form_obj = EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()

            return redirect(reverse_url(request, 'enrollment_list'))
    title = '编辑报名记录' if enrollment_id else '新增报名记录'
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})