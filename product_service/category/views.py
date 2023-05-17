from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import *
# Create your views here.

@csrf_exempt
def create_category(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        name = data.get("name")
        code = data.get("code")
        picture = data.get("picture")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (name and code and picture ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{name} and {code} and {picture} "},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được
    cate = Category(
        name=name,
        code=code,
        picture=picture,
    )
    cate.save()
    # Trả về thông tin vừa tạo nếu thành công
    return JsonResponse({"status": "success", "message": "Đăng ký category thành công.", "Cartegory": cate.to_dict()})


@csrf_exempt
def getall_category(request):
    cates = Category.objects.all()
    cate_dicts = [cate.to_dict() for cate in cates]
    return JsonResponse({"data": cate_dicts}, status=200)

@csrf_exempt
def get_category_by_id(request):
    id = request.GET.get('id')
    if(id ==None):
        return JsonResponse({'status':'error','message':"error id"},status=400)
    try:
        obj = Category.objects.get(id=id)
        return JsonResponse({'data':obj.to_dict()},status=200)
    except Category.DoesNotExist:
        return JsonResponse({'status':'error','message':"không timg thấy category"},status=400)

@csrf_exempt
def get_category_by_code(request):
    code = request.GET.get('code')
    if(code ==None):
        return JsonResponse({'status':'error','message':"error code"},status=400)
    try:
        obj = Category.objects.get(code=code)
        return JsonResponse({'data':obj.to_dict()},status=200)
    except Category.DoesNotExist:
        return JsonResponse({'status':'error','message':"không timg thấy category"},status=400)

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_category_by_id(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if(id ==None):
            return JsonResponse({'status':'error','message':"error id"},status=400)
        try:
            obj = Category.objects.get(id=id)
            obj.delete()
            return JsonResponse({'status':'success','message':"delete success"},status=200)
        except Category.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy category"},status=400)
    return JsonResponse({"status":"erorr","message":"method is not DELETE"},status=400)