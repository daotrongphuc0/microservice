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
def create_rate(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        customerId = data.get("customerId")
        productId = data.get("productId")
        rating = data.get("rating")
        content = data.get("content")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (customerId and productId and content and rating ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{customerId} and {productId} and {content} and {rating}"},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được
    try:
        obj_cus = Customer.objects.get(id=customerId)
    except Customer.DoesNotExist:
        return JsonResponse({'status':'error','message':"không tim thấy customer"},status=400)
    
    
    #response = requests.get(f'http://127.0.0.1:8001/product/getbyid/?id={productId}')
    response =  requests.get(f'http://127.0.0.1:8005/order/getbycusandpro/?productId={productId}&customerId={customerId}')
    if response.status_code==200:
        try:
            rate = Rate.objects.get(productId=productId,customer=obj_cus)
            rate.rating= rating
            rate.content =content
            rate.save()
        except Rate.DoesNotExist:
            rate = Rate(
                customer=obj_cus,
                productId=productId,
                content=content,
                rating =rating
            )
            rate.save()
        return JsonResponse({"status": "success", "message": "Tạo comment thành công.",'data':rate.to_dict()},status=200)
    else:
        return JsonResponse({"status": "Erorr", "message": "chua mua sna pham nay"},status=400)

@csrf_exempt
def getall_rate(request):
    rates = Rate.objects.all()
    rate_dicts = [rate.to_dict() for rate in rates]
    return JsonResponse({"data": rate_dicts}, status=200)

@csrf_exempt
def getall_rate_by_product(request):
    productId=request.GET.get('productId')
    response = requests.get(f'http://127.0.0.1:8001/product/getbyid/?id={productId}')
    if response.status_code==200:
        rates = Rate.objects.filter(productId=productId)
        rate_dicts = [rate.to_dict() for rate in rates]
        return JsonResponse({"data": rate_dicts}, status=200)
    else:
        return JsonResponse({"status": "Erorr", "message": "No product found"},status=400)


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_rate_by_id(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if(id ==None):
            return JsonResponse({'status':'error','message':"error id"},status=400)
        try:
            obj = Rate.objects.get(id=id)
            obj.delete()
            return JsonResponse({'status':'success','message':"delete success"},status=200)
        except Rate.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy rate"},status=400)
    return JsonResponse({"status":"erorr","message":"method is not DELETE"},status=400)