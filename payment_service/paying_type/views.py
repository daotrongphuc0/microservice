from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
import requests
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.utils import timezone
# Create your views here.

@csrf_exempt
def create_pay_type(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        name = data.get("name")
        description = data.get("description")
        enable = data.get("enable")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (name and description and enable  ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{name} and {description} and {enable}"},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được   

    paying = Paying_type(
        name= name,
        description=description,
        enable =enable,
    )
    paying.save()
    # Trả về thông tin vừa tạo nếu thành công
    return JsonResponse({"status": "success", "message": "Đăng ký category thành công.", "data": paying.to_dict()})


@csrf_exempt
def getall_pay(request):
    pays = Paying_type.objects.all()
    pay_dicts = [pay.to_dict() for pay in pays]
    return JsonResponse({"data": pay_dicts}, status=200)

@csrf_exempt
def get_pay_by_id(request):
    id = request.GET.get('id')
    if(id ==None):
        return JsonResponse({'status':'error','message':"error id"},status=400)
    try:
        obj = Paying_type.objects.get(id=id)
        return JsonResponse({'data':obj.to_dict()},status=200)
    except Paying_type.DoesNotExist:
        return JsonResponse({'status':'error','message':"không timg thấy paying type"},status=400)


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_pay(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if(id ==None):
            return JsonResponse({'status':'error','message':"error id"},status=400)
        try:
            obj = Paying_type.objects.get(id=id)
            obj.delete()
            return JsonResponse({'status':'success','message':"delete success"},status=200)
        except Paying_type.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy paying type"},status=400)
    return JsonResponse({"status":"erorr","message":"method is not DELETE"},status=400)
