from django.urls import path

from .views import *

urlpatterns = [
    path('userinfo/', user_info),
    path('customerinfo/', customer_info),
    path('admininfo/', admin_info),
    path('employeeinfo/', employee_info),
    path('get_all_customer/',get_all)
]