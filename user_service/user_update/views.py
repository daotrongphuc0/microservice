from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from user_regis.models import *


@csrf_exempt
def update(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        username = data.get("username")
        isVip =data.get('isVip')
        isNew =data.get('isNew')
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    if not (username):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                                "data":f"user name: {username} "},status=400)
    respdata  = Customer.objects.filter(username=username)
    if(respdata):
        if isVip != None:
            respdata[0].isVip = isVip
        if(isNew != None):
            respdata[0].isNew = isNew
        return JsonResponse({'status':'success',"data":respdata[0].to_dict()},status=200)
    else:
        return JsonResponse({"status": "error", "message": "Không tìm thấy Customer"},status=400)
    
@csrf_exempt
def chance_pass(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        username = data.get("username")
        old_pass =data.get('old_pass')
        new_pass =data.get('new_pass')
        new_pass_confirm =data.get('new_pass_confirm')
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    if not (username and old_pass and new_pass and new_pass_confirm ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                                "data":f"user name: {username} "},status=400)
    respdata  = User.objects.filter(username=username)
    if(respdata):
        if(respdata[0].password == old_pass):
            if(new_pass == new_pass_confirm):
                respdata[0].password = new_pass
                return JsonResponse({'status':'success',"data":respdata[0].to_dict()},status=200)
            else:
                return JsonResponse({'status':'erorr',"message":'password confirm not true'},status=400)
        else:
            return JsonResponse({'status':'erorr',"message":'password is wrong'},status=400)
    else:
        return JsonResponse({"status": "error", "message": "Không tìm thấy user"},status=400)
    
@csrf_exempt
def forgot_pass(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        username = data.get("username")
        new_pass =data.get('new_pass')
        new_pass_confirm =data.get('new_pass_confirm')
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    if not (username and new_pass and new_pass_confirm ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                                "data":f"user name: {username} "},status=400)
    respdata  = User.objects.filter(username=username)
    if(respdata):
        if(new_pass == new_pass_confirm):
            respdata[0].password = new_pass
            return JsonResponse({'status':'success',"data":respdata[0].to_dict()},status=200)
        else:
            return JsonResponse({'status':'erorr',"message":'password confirm not true'},status=400)
    else:
        return JsonResponse({"status": "error", "message": "Không tìm thấy user"},status=400)
