from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from user_regis.models import User

def user_validation(username, password):
    user_data = User.objects.filter(username=username, password=password)
    return user_data

@csrf_exempt
def user_login(request):
    if request.method == 'POST':

        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        username = data.get("username")
        password = data.get("password")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    if not (username and password ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                                "data":f"{username} and {password} "},status=400)
    respdata = user_validation(username, password)
    if(respdata):
        return JsonResponse({"status": "Success", "message": "Đăng nhập thành công",
                             "User": respdata[0].username,"role":respdata[0].role},status=200)
    else:
        return JsonResponse({"status": "error", "message": "Sai thông tin đăng nhập"},status=400)
    