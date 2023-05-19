from django.urls import path

from .views import *

urlpatterns = [
    path('create/',create_pay_type),
    path("getall/",getall_pay),
    path('getbyid/',get_pay_by_id),
    path('delete/',delete_pay)
]