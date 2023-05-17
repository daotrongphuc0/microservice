from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from user_regis.models import *
from django.views.decorators.http import require_http_methods
# Create your views here.

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_customer(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if(id ==None):
            return JsonResponse({'status':'error','message':"error id"},status=400)
        
        response = requests.delete(f'http://127.0.0.1:8002/delete_cart/?customerId={id}')
        if response.status_code == 200:
            try:
                obj = Customer.objects.get(id=id)
                obj.delete()
                return JsonResponse({'status':'success','message':"delete success"},status=200)
            except Customer.DoesNotExist:
                return JsonResponse({'status':'error','message':"không timg thấy customer"},status=400)
        else:
            return JsonResponse({"status":"erorr","message":"can not delete cart"},status=400)
    return JsonResponse({"status":"erorr","message":"method is not DELETE"},status=400)

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_admin(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if(id ==None):
            return JsonResponse({'status':'error','message':"error id"},status=400)
        try:
            obj = Admin.objects.get(id=id)
            obj.delete()
            return JsonResponse({'status':'success','message':"delete success"},status=200)
        except Admin.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy admin"},status=400)
    return JsonResponse({"status":"erorr","message":"method is not DELETE"},status=400)

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_employee(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if(id ==None):
            return JsonResponse({'status':'error','message':"error id"},status=400)
        try:
            obj = Admin.objects.get(id=id)
            obj.delete()
            return JsonResponse({'status':'success','message':"delete success"},status=200)
        except Admin.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy employee"},status=400)
    return JsonResponse({"status":"erorr","message":"method is not DELETE"},status=400)
