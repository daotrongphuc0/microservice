from django.urls import path

from .views import *

urlpatterns = [
    path('create/', create_brand),
    path('getall/', getall_brand),
    path('getbyid/', get_brand_by_id),
    path('getbycode/', get_brand_by_code),
    path('delete/', delete_brand_by_id),
]