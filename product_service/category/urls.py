from django.urls import path

from .views import *

urlpatterns = [
    path('create/', create_category),
    path('getall/', getall_category),
    path('getbyid/', get_category_by_id),
    path('getbycode/', get_category_by_code),
    path('delete/', delete_category_by_id)
]