from django.urls import path
from .views import *

urlpatterns = [
    path('create/',create_ship),
    path('getall/',getall_ship),
    path('get_ship_by_id/',get_ship_by_id),
    path('update_finish/',update_finish),
    path('add_stage/',add_stage),
    path('delete_stage/',delete_stage),
]
