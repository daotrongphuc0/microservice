from django.urls import path

from .views import *

urlpatterns = [
    path('create/', create_supplier),
    path('getall/', getall_supplier),
    path('getbyid/', get_supplier_by_id),
    path('getbycode/', get_supplier_by_name),
    path('delete/', delete_supplier_by_id),
]