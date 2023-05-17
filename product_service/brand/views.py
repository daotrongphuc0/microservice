from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import *
# Create your views here.

@csrf_exempt
def create_brand(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        name = data.get("name")
        code = data.get("code")
        description = data.get("description")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (name and code and description ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{name} and {code} and {description} "},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được
    brand = Brand(
        name=name,
        code=code,
        description=description,
    )
    brand.save()
    # Trả về thông tin vừa tạo nếu thành công
    return JsonResponse({"status": "success", "message": "Đăng ký brand thành công.", "Brand": brand.to_dict()})


@csrf_exempt
def getall_brand(request):
    brands = Brand.objects.all()
    brands_dicts = [brand.to_dict() for brand in brands]
    return JsonResponse({"data": brands_dicts}, status=200)

@csrf_exempt
def get_brand_by_id(request):
    id = request.GET.get('id')
    if(id ==None):
        return JsonResponse({'status':'error','message':"error id"},status=400)
    try:
        obj = Brand.objects.get(id=id)
        return JsonResponse({'data':obj.to_dict()},status=200)
    except Brand.DoesNotExist:
        return JsonResponse({'status':'error','message':"không timg thấy brand"},status=400)

@csrf_exempt
def get_brand_by_code(request):
    code = request.GET.get('code')
    if(code ==None):
        return JsonResponse({'status':'error','message':"error code"},status=400)
    try:
        obj = Brand.objects.get(code=code)
        return JsonResponse({'data':obj.to_dict()},status=200)
    except Brand.DoesNotExist:
        return JsonResponse({'status':'error','message':"không timg thấy brand"},status=400)

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_brand_by_id(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if(id ==None):
            return JsonResponse({'status':'error','message':"error id"},status=400)
        try:
            obj = Brand.objects.get(id=id)
            obj.delete()
            return JsonResponse({'status':'success','message':"delete success"},status=200)
        except Brand.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy brand"},status=400)
    return JsonResponse({"status":"erorr","message":"method is not DELETE"},status=400)