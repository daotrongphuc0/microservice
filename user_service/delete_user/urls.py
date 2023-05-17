from django.urls import path

from .views import *

urlpatterns = [
    path('delete_customer/',delete_customer),
    path('delete_admin/', delete_admin),
    path('delete_employee/',delete_employee)
]