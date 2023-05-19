from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
import requests
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import *
# Create your views here.

@csrf_exempt
def create_cart(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        customerId = data.get("customerId")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (customerId ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{customerId} "},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được
    cart = Cart(
        customerId=customerId
    )
    cart.save()
    # Trả về thông tin vừa tạo nếu thành công
    return JsonResponse({"status": "success", "message": "Đăng ký Cart thành công.", "Cart": cart.to_dict()})

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_cart_by_id(request):
    if request.method == 'DELETE':
        id = request.GET.get('customerId')
        if(id ==None):
            return JsonResponse({'status':'error','message':"error id"},status=400)
        try:
            obj = Cart.objects.get(customerId=id)
            obj.delete()
            return JsonResponse({'status':'success','message':"delete success"},status=200)
        except Cart.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy cart"},status=400)
    return JsonResponse({"status":"erorr","message":"method is not DELETE"},status=400)


@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        productId = data.get("productId")
        quantity = data.get("quantity")
        #price = data.get("price")
        customerId = data.get("customerId")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (customerId and productId and quantity ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{customerId} and {productId} and {quantity} "},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được
    try:
        obj = Cart.objects.get(customerId=customerId)
    except Cart.DoesNotExist:
        return JsonResponse({'status':'error','message':"không timg thấy cart"},status=400)
    
    response = requests.get(f"http://127.0.0.1:8001/product/getbyid/?id={productId}")
    if response.status_code == 200:
        try:
            item = Item.objects.get(cart= obj,productId=productId)
            item.price = response.json().get('data').get('price') * quantity
            item.quantity=quantity
            item.save()
        except Item.DoesNotExist:
            item= Item(
                cart=obj,
                productId=productId,
                price=response.json().get('data').get('price') * quantity,
                quantity=quantity
            )
            item.save()
        return JsonResponse({"status": "success", "message": "add to Cart thành công.", "Item": item.to_dict()})
    else:
        return JsonResponse({"status":"error","mesage":"No products found "},status =400)
    

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_cart_item(request):
    if request.method == 'DELETE':
        customerId = request.GET.get('customerId')
        productId  = request.GET.get('productId')
        if(customerId ==None or productId==None):
            return JsonResponse({'status':'error','message':"error id"},status=400)
        try:
            obj = Cart.objects.get(customerId=customerId)
            item =Item.objects.get(cart=obj,productId=productId)
            item.delete()
            return JsonResponse({'status':'success','message':"delete success"},status=200)
        except Cart.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy cart"},status=400)
        except Item.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy item"},status=400)
    return JsonResponse({"status":"erorr","message":"method is not DELETE"},status=400)

@csrf_exempt
def getall_item_cart_by_customer(request):
    customerId=request.GET.get('customerId')
    response = requests.post('http://127.0.0.1:8000/customerinfo/',data=json.dumps({"customerId":customerId}))
    if response.status_code == 200:
        try:
            obj = Cart.objects.get(customerId=customerId)
        except Cart.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy cart"},status=400)
        
        items = Item.objects.filter(cart=obj)
        item_dicts = [item.to_dict() for item in items]
        return JsonResponse({"data": item_dicts}, status=200)
    return JsonResponse({'status':'error','message':"không tim thấy customer"},status=400)