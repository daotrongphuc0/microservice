from django.urls import path
from .views import *

urlpatterns = [
    path('create/',create_rate),
    path('getall/',getall_rate),
    path('getbyproduct/',getall_rate_by_product),
    path('delete/',delete_rate_by_id),
]
