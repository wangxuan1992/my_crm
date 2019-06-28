
from django.conf.urls import url
from crm.views import customer

urlpatterns = [
    url(r'^customer_list/', customer.customer_list,name='customer_list'),
    url(r'^my_customer/', customer.customer_list,name='my_customer'),
    url(r'^add_customer/',customer.customer_change,name='add_customer'),
    url(r'^edit_customer/(\d+)/',customer.customer_change,name='edit_customer'),
]
