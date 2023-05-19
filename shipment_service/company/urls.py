from django.urls import path

from .views import *

urlpatterns = [
    path('create/', create_company),
    path('getall/', getall_company),
    path('getbyid/', get_company_by_id),
    path('delete/', delete_company_by_id)
]