
from django.conf.urls import url
from crm.views import customer,consult

urlpatterns = [
    #公户
    url(r'^customer_list/', customer.Customerlist.as_view(),name='customer_list'),
    # 私户
    url(r'^my_customer/', customer.Customerlist.as_view(),name='my_customer'),
    # 添加客户
    url(r'^add_customer/',customer.customer_change,name='add_customer'),
    # 修改客户
    url(r'^edit_customer/(\d+)/',customer.customer_change,name='edit_customer'),
    # 跟进记录展示
    url(r'^consult_list/(?P<customer_id>\d+)/',consult.Consultlist.as_view(), name='consult_list'),
    # 添加跟进
    url(r'^add_consult/', consult.add_consult, name='add_consult'),
    # 编辑跟进
    url(r'^edit_consult/(\d+)', consult.edit_consult, name='edit_consult'),


]
