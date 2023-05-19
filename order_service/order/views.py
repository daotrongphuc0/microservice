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
def create_order(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        customerId = data.get("customerId")
        list_item = data.get("list_item")
        comapnyId = data.get("comapnyId")
        paying_typeId =  data.get("paying_typeId")
    else:
        print("method is not POST")
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (customerId and list_item):
        print()
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{customerId} and {list_item} "},
                               status=400)
    
    response = requests.post(f'http://127.0.0.1:8000/customerinfo/',data=json.dumps({"customerId":customerId}))
    if response.status_code != 200:
        print()
        return JsonResponse({'status':'error','message':"không tim thấy customer"},status=400)
    
    response_cart = requests.get(f'http://127.0.0.1:8002/getallbycustomer/?customerId={customerId}')
    if response_cart.status_code != 200:
        print()
        return JsonResponse({'status':'error','message':"không tim thấy list item cart"},status=400)
    
    carts = response_cart.json().get('data')
    res = []
    res_total_price =0
    for item in list_item:
        check =0
        for cart in carts:
            if item == cart.get("id"):
                check =1
                res.append(cart)
                res_total_price = res_total_price + cart.get('price')
        if(not check):
            print()
            return JsonResponse({'status':'error','message':f"không tim thấy item: {item}"},status=400)    
    current_time = timezone.now()
    formatted_time = current_time.strftime("%M-%H %d/%m/%Y")
    order = Order(
        customerId= customerId,
        time = formatted_time,
        status = 'unfinished',
        total=res_total_price
    )
    order.save()

    response_ship = requests.post('http://127.0.0.1:8003/shipping/create/',data=json.dumps({
        "customerId":customerId,
        "orderId":order.id,
        "comapnyId":comapnyId
    }))
    if response_ship.status_code != 200:
        print()
        return JsonResponse({'status':'error','message':f"không tao duoc ship"},status=400)  
    order.shippingId = response_ship.json().get('data').get('id')
    # Trả về thông tin vừa tạo nếu thành công

    response_pay = requests.post('http://127.0.0.1:8004/payment/create/',data=json.dumps({
        "customerId":customerId,
        "orderId":order.id,
        "status":"unfinished",
        "paying_typeId":paying_typeId,
        "amount":res_total_price
    }))
    if response_pay.status_code != 200:
        print()
        return JsonResponse({'status':'error','message':f"không tao duoc pay"},status=400)  
    order.paymentId = response_ship.json().get('data').get('id')
    order.save()

    for item in res:
        item_order = Item(
            productId = item.get("productId"),
            quantity = item.get("quantity"),
            price = item.get("price"),
            order = order,
        )
        item_order.save()
        response_item_cart = requests.delete(f'http://127.0.0.1:8002/delete_cart_item/?productId={item_order.productId}&customerId={customerId}')

        if response_item_cart.status_code != 200:
            return JsonResponse({f"status": "erorr", "message": "lỗi xoá cart item product: {item_order.productId}"},status= 400)

    return JsonResponse({"status": "success", "message": "Tạo order thành công.", "data": order.to_dict()},status=200)


@csrf_exempt
def getall_order(request):
    orders = Order.objects.all()
    order_dicts = [order.to_dict() for order in orders]
    return JsonResponse({"data": order_dicts}, status=200)

@csrf_exempt
def get_order_by_id(request):
    id = request.GET.get('id')
    if(id ==None):
        return JsonResponse({'status':'error','message':"error id"},status=400)
    try:
        obj = Order.objects.get(id=id)
        return JsonResponse({'data':obj.to_dict()},status=200)
    except Order.DoesNotExist:
        return JsonResponse({'status':'error','message':"không timg thấy order"},status=400)
    
@csrf_exempt
def get_order_by_customerId_and_productId(request):
    customerId = request.GET.get('customerId')
    productId = request.GET.get('productId')
    if(customerId ==None or productId== None ):
        return JsonResponse({'status':'error','message':f"error id: {customerId} and {productId}"},status=400)
    obj = Order.objects.filter(customerId=customerId)
    if len(obj) ==0:
        return JsonResponse({'status':'error','message':f"khong tim thay oder của customer: {customerId} "},status=400)
    for order in obj:
        try:
            items = Item.objects.get(order=order,productId=productId)
            return JsonResponse({'status':'success','message':"co order"},status=200)
        except Item.DoesNotExist:
            print("not found item")
    return JsonResponse({'status':'error','message':"not found"},status=400) 


@csrf_exempt
def update_finish(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        orderId = data.get("orderId")
        status = data.get("status")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (orderId and status):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{orderId} and {status} "},
                               status=400)
    
    try:
        obj = Order.objects.get(id=orderId)
    except Order.DoesNotExist:
        return JsonResponse({'status':'error','message':"không timg thấy order"},status=400)
    
    if status == 'shipment_finish':
        if obj.status == 'unfinished' or  obj.status == 'shipment_finish' :
            obj.status = status
        else :
            obj.status = 'finish'

    if status == 'payment_finish':
        if obj.status == 'unfinished'  or  obj.status == 'payment_finish' :
            obj.status = status
        else :
            obj.status = 'finish'

    obj.save()
    return JsonResponse({'data':obj.to_dict()},status=200)

