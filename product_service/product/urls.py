from django.urls import path

from .views import *

urlpatterns = [
    path('create/', create_product),
    path('getall/', getall_product),
    path('getbyid/', get_product_by_id),
    path('update/', upadte_product),
    path('delete/', delete_product_by_id),
    path('update_inventory/', update_inventory),
    path('get_all_inventory/', getall_inventory),
]