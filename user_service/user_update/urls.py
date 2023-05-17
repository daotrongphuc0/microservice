from django.urls import path

from .views import *

urlpatterns = [
    path('update_user/',update),
    path("chance_pass/",chance_pass),
    path('forgot_pass/',forgot_pass)
]