from django.urls import path

from .views import *

urlpatterns = [
    path('customer_registration/', register_customer),
    path('admin_registration/', register_admin),
    path('employee_registration/', register_employee)
]