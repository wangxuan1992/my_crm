from django.shortcuts import render,redirect,HttpResponse,reverse
from crm import models
from crm.forms import CustomerForm


from crm.utils.pagination import Pagination


def customer_list(request):
    if request.path_info == reverse('customer_list'):
        all_customer = models.Customer.objects.filter(consultant__isnull=True)
    else:
        all_customer = models.Customer.objects.filter(consultant=request.user_obj)

    return render(request,'customer_list.html',{'all_customer':all_customer})


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
            return redirect(reverse('customer_list'))

    return render(request, 'customer_change.html', {'form_obj': form_obj,'title':title})

