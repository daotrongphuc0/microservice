from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import *
# Create your views here.

@csrf_exempt
def create_company(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        address = data.get("address")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (name and email and phone and address ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{name} and {email} and {phone} and {address} "},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được
    company = Company(
        name=name,
        email=email,
        address=address,
        phone  = phone
    )
    company.save()
    # Trả về thông tin vừa tạo nếu thành công
    return JsonResponse({"status": "success", "message": "Đăng ký category thành công.", "company": company.to_dict()})


@csrf_exempt
def getall_company(request):
    companys = Company.objects.all()
    company_dicts = [company.to_dict() for company in companys]
    return JsonResponse({"data": company_dicts}, status=200)

@csrf_exempt
def get_company_by_id(request):
    id = request.GET.get('id')
    if(id ==None):
        return JsonResponse({'status':'error','message':"error id"},status=400)
    try:
        obj = Company.objects.get(id=id)
        return JsonResponse({'data':obj.to_dict()},status=200)
    except Company.DoesNotExist:
        return JsonResponse({'status':'error','message':"không timg thấy company"},status=400)


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_company_by_id(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if(id ==None):
            return JsonResponse({'status':'error','message':"error id"},status=400)
        try:
            obj = Company.objects.get(id=id)
            obj.delete()
            return JsonResponse({'status':'success','message':"delete success"},status=200)
        except Company.DoesNotExist:
            return JsonResponse({'status':'error','message':"không tim thấy company"},status=400)
    return JsonResponse({"status":"erorr","message":"method is not DELETE"},status=400)