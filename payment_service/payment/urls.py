from django.urls import path

from .views import *

urlpatterns = [
    path('create/',create_pay),
    path("getall/",getall_pay),
    path('getbyid/',get_pay_by_id),
    path('update_finish/',update_finish)
]