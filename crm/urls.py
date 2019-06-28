
from django.conf.urls import url
from crm import views

urlpatterns = [
    url(r'^customer_list/', views.customer_list,name='customer_list'),
    url(r'^user_list/',views.user_list,name='user_list'),
]