from django.urls import path
from .views import *

urlpatterns = [
    path('create/',create_order),
    path('getall/',getall_order),
    path('get_order_by_id/',get_order_by_id),
    path('update_finish/',update_finish),
    path('getbycusandpro/',get_order_by_customerId_and_productId)
]
