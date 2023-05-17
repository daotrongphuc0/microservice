from django.urls import path

from .views import user_login

urlpatterns = [
    path('userlogin/', user_login),
]