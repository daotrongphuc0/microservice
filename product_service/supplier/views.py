from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import *
# Create your views here.

@csrf_exempt
def create_supplier(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        name = data.get("name")
        address = data.get("address")
        email = data.get("email")
        phone = data.get("phone")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (name and address and email and phone ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{name} and {address} and {email} and {phone} "},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được
    supplier = Supplier(
        name=name,
        email=email,
        address=address,
        phone=phone
    )
    supplier.save()
    # Trả về thông tin vừa tạo nếu thành công
    return JsonResponse({"status": "success", "message": "Đăng ký Supplier thành công.", "supplier": supplier.to_dict()})


@csrf_exempt
def getall_supplier(request):
    suppliers = Supplier.objects.all()
    suppliers_dicts = [supplier.to_dict() for supplier in suppliers]
    return JsonResponse({"data": suppliers_dicts}, status=200)

@csrf_exempt
def get_supplier_by_id(request):
    id = request.GET.get('id')
    if(id ==None):
        return JsonResponse({'status':'error','message':"error id"},status=400)
    try:
        obj = Supplier.objects.get(id=id)
        return JsonResponse({'data':obj.to_dict()},status=200)
    except Supplier.DoesNotExist:
        return JsonResponse({'status':'error','message':"không tim thấy supplier"},status=400)

@csrf_exempt
def get_supplier_by_name(request):
    code = request.GET.get('code')
    if(code ==None):
        return JsonResponse({'status':'error','message':"error code"},status=400)
    try:
        obj = Supplier.objects.get(code=code)
        return JsonResponse({'data':obj.to_dict()},status=200)
    except Supplier.DoesNotExist:
        return JsonResponse({'status':'error','message':"không timg thấy supplier"},status=400)

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_supplier_by_id(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if(id ==None):
            return JsonResponse({'status':'error','message':"error id"},status=400)
        try:
            obj = Supplier.objects.get(id=id)
            obj.delete()
            return JsonResponse({'status':'success','message':"delete success"},status=200)
        except Supplier.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy supplier"},status=400)
    return JsonResponse({"status":"erorr","message":"method is not DELETE"},status=400)