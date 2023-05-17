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
def create_comment(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        parent_comment = data.get("parent_comment")
        customerId = data.get("customerId")
        productId = data.get("productId")
        content = data.get("content")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (customerId and productId and content  ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{customerId} and {productId} and {content} "},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được
    try:
        obj_cus = Customer.objects.get(id=customerId)
    except Customer.DoesNotExist:
        return JsonResponse({'status':'error','message':"không tim thấy customer"},status=400)
    
    if parent_comment != None:
        try:
            obj_comment = Comment.objects.get(id=parent_comment)
        except Comment.DoesNotExist:
            return JsonResponse({'status':'error','message':"không tim thấy parent comment"},status=400)
    else:
        obj_comment=None
    
    response = requests.get(f'http://127.0.0.1:8001/product/getbyid/?id={productId}')
    if response.status_code==200:
        current_time = timezone.now()
        formatted_time = current_time.strftime("%M-%H %d/%m/%Y")
        comment = Comment(
            customer=obj_cus,
            productId=productId,
            conten=content,
            parent_comment= obj_comment,
            time=formatted_time
        )
        comment.save()
        return JsonResponse({"status": "success", "message": "Tạo comment thành công.",'data':comment.to_dict()},status=200)
    else:
        return JsonResponse({"status": "Erorr", "message": "No product found"},status=400)

@csrf_exempt
def getall_comment(request):
    comments = Comment.objects.filter(parent_comment=None)
    cate_dicts = [comment.to_dict() for comment in comments]
    return JsonResponse({"data": cate_dicts}, status=200)

@csrf_exempt
def getall_comment_by_product(request):
    productId=request.GET.get('productId')
    response = requests.get(f'http://127.0.0.1:8001/product/getbyid/?id={productId}')
    if response.status_code==200:
        comments = Comment.objects.filter(parent_comment=None,productId=productId)
        cate_dicts = [comment.to_dict() for comment in comments]
        return JsonResponse({"data": cate_dicts}, status=200)
    else:
        return JsonResponse({"status": "Erorr", "message": "No product found"},status=400)

@csrf_exempt
def getall_comment_by_customer(request):
    customerId=request.GET.get('customerId')
    try:
        obj_cus = Customer.objects.get(id=customerId)
    except Customer.DoesNotExist:
        return JsonResponse({'status':'error','message':"không tim thấy customer"},status=400)
    comments = Comment.objects.filter(parent_comment=None,customer=obj_cus)
    cate_dicts = [comment.to_dict() for comment in comments]
    return JsonResponse({"data": cate_dicts}, status=200)

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_comment_by_id(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if(id ==None):
            return JsonResponse({'status':'error','message':"error id"},status=400)
        try:
            obj = Comment.objects.get(id=id)
            obj.delete()
            return JsonResponse({'status':'success','message':"delete success"},status=200)
        except Comment.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy comment"},status=400)
    return JsonResponse({"status":"erorr","message":"method is not DELETE"},status=400)