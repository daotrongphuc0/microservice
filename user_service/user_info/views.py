from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from user_regis.models import *


@csrf_exempt
def user_info(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        username = data.get("username")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    if not (username):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                                "data":f"user name: {username} "},status=400)
    respdata  = User.objects.filter(username=username)
    if(respdata):
        return JsonResponse({"data":respdata[0].to_dict()},status=200)
    else:
        return JsonResponse({"status": "error", "message": "Không tìm thấy user"},status=400)
    
@csrf_exempt
def customer_info(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        username = data.get("username")
        customerId=data.get("customerId")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    if not (username or customerId):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                                "data":f"user name: {username} "},status=400)
    if customerId:
        respdata  = Customer.objects.filter(id=customerId)
    else:
        respdata  = Customer.objects.filter(username=username)
    if(respdata):
        return JsonResponse({"data":respdata[0].to_dict()},status=200)
    else:
        return JsonResponse({"status": "error", "message": "Không tìm thấy customer"},status=400)
    

@csrf_exempt
def admin_info(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        username = data.get("username")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    if not (username):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                                "data":f"user name: {username} "},status=400)
    respdata  = Admin.objects.filter(username=username)
    if(respdata):
        return JsonResponse({"data":respdata[0].to_dict()},status=200)
    else:
        return JsonResponse({"status": "error", "message": "Không tìm thấy admin"},status=400)
    

@csrf_exempt
def employee_info(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        username = data.get("username")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    if not (username):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                                "data":f"user name: {username} "},status=400)
    respdata  = Employee.objects.filter(username=username)
    if(respdata):
        return JsonResponse({"data":respdata[0].to_dict()},status=200)
    else:
        return JsonResponse({"status": "error", "message": "Không tìm thấy employee"},status=400)
    

@csrf_exempt
def get_all(request):
    customers = Customer.objects.all()
    customer_dicts = [customer.to_dict() for customer in customers]
    return JsonResponse({"data": customer_dicts}, status=200)