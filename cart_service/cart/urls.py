from django.urls import path

from .views import *

urlpatterns = [
    path('create_cart/',create_cart),
    path('delete_cart/',delete_cart_by_id),
    path('add_to_cart/',add_to_cart),
    path('delete_cart_item/',delete_cart_item),
    path('getallbycustomer/',getall_item_cart_by_customer)
]