from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import *

# Create your views here.
@csrf_exempt
def register_customer(request):
# Lấy các thông tin cần thiết từ data
    if request.method == 'POST':

        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        username = data.get("username")
        password = data.get("password")
        firstName = data.get("firstName")
        lastName = data.get("lastName")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (username and password and firstName and lastName and phone and email and address):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{username} and {password} and {firstName} and {lastName} and {phone} and {email} and {address}"},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được
    user = Customer(
        username=username,
        password=password,
        firstName=firstName,
        lastName=lastName,
        phone=phone,
        email=email,
        role=1,
        isActive=1,
        address=address,
        isVip=0,
        isNew=1
    )
    user.save()
    response = requests.post('http://127.0.0.1:8002/create_cart/',data=json.dumps({'customerId':user.id}))
    if response.status_code ==200:
        return JsonResponse({"status": "success", "message": "Đăng ký thành công.", "user": {"username": user.username, "email": user.email}})
    else:
        user.delete()
        return JsonResponse({'status':'erorr','message':'erorr cart'},status=400)


@csrf_exempt
def register_admin(request):
# Lấy các thông tin cần thiết từ data
    if request.method == 'POST':

        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        username = data.get("username")
        password = data.get("password")
        firstName = data.get("firstName")
        lastName = data.get("lastName")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")
        position =data.get('position')
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (username and password and firstName and lastName and phone and email and address and position):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{username} and {password} and {firstName} and {lastName} and {phone} and {email} and {address} adn {position}"},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được
    admin = Admin(
        username=username,
        password=password,
        firstName=firstName,
        lastName=lastName,
        phone=phone,
        email=email,
        role=1,
        isActive=1,
        position=position
    )
    admin.save()
    # Trả về thông tin vừa tạo nếu thành công
    return JsonResponse({"status": "success", "message": "Đăng ký thành công.", "user": {"username": admin.username, "email": admin.email}})

@csrf_exempt
def register_employee(request):
# Lấy các thông tin cần thiết từ data
    if request.method == 'POST':

        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        username = data.get("username")
        password = data.get("password")
        firstName = data.get("firstName")
        lastName = data.get("lastName")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")
        position =data.get('position')
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (username and password and firstName and lastName and phone and email and address and position):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{username} and {password} and {firstName} and {lastName} and {phone} and {email} and {address} adn {position}"},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được
    employee = Employee(
        username=username,
        password=password,
        firstName=firstName,
        lastName=lastName,
        phone=phone,
        email=email,
        role=1,
        isActive=1,
        position=position
    )
    employee.save()
    # Trả về thông tin vừa tạo nếu thành công
    return JsonResponse({"status": "success", "message": "Đăng ký thành công.", "user": {"username": employee.username, "email": employee.email}})
