from django.urls import path
from .views import *

urlpatterns = [
    path('create/',create_comment),
    path('getall/',getall_comment),
    path('getbyproduct/',getall_comment_by_product),
    path('getbycustomer/',getall_comment_by_customer),
    path('delete/',delete_comment_by_id),
]
