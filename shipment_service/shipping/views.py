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
def create_ship(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        customerId = data.get("customerId")
        orderId = data.get("orderId")
        comapnyId = data.get("comapnyId")
    else:
        print("method is not POST")
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (customerId and orderId and comapnyId  ):
        print(f"Vui lòng điền đầy đủ thông tin.: {customerId} and {orderId} and {comapnyId}")
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{customerId} and {orderId} and {comapnyId}"},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được

    try:
        obj = Company.objects.get(id=comapnyId)
    except Company.DoesNotExist:
        print("không timg thấy company")
        return JsonResponse({'status':'error','message':"không timg thấy company"},status=400)
    
    response = requests.post(f'http://127.0.0.1:8000/customerinfo/',data=json.dumps({"customerId":customerId}))
    if response.status_code != 200:
        print("không tim thấy customer")
        return JsonResponse({'status':'error','message':"không tim thấy customer"},status=400)
    
    current_time = timezone.now()
    formatted_time = current_time.strftime("%M-%H %d/%m/%Y")
    ship = Shipping(
        customerId= customerId,
        orderId=orderId,
        company =obj,
        intendTime = None,
        startTime = formatted_time,
        status = 'dang van chuyen'
    )
    ship.save()
    stage =Stage(
        time = formatted_time,
        location = "shop",
        comment  = "Bat dau lay hang",
        shipping = ship
    )
    stage.save()
    # Trả về thông tin vừa tạo nếu thành công
    return JsonResponse({"status": "success", "message": "Đăng ký ship thành công.", "data": ship.to_dict()},status=200)


@csrf_exempt
def getall_ship(request):
    ships = Shipping.objects.all()
    ship_dicts = [ship.to_dict() for ship in ships]
    return JsonResponse({"data": ship_dicts}, status=200)

@csrf_exempt
def get_ship_by_id(request):
    id = request.GET.get('id')
    if(id ==None):
        return JsonResponse({'status':'error','message':"error id"},status=400)
    try:
        obj = Shipping.objects.get(id=id)
        return JsonResponse({'data':obj.to_dict()},status=200)
    except Shipping.DoesNotExist:
        return JsonResponse({'status':'error','message':"không timg thấy Shipment"},status=400)

@csrf_exempt
def update_finish(request):
    id = request.GET.get('id')
    if(id ==None):
        return JsonResponse({'status':'error','message':"error id"},status=400)
    try:
        obj = Shipping.objects.get(id=id)
    except Shipping.DoesNotExist:
        return JsonResponse({'status':'error','message':"không timg thấy Shipment"},status=400)
    obj.status ='complete'
    # goi API update order
    respons = requests.post('http://127.0.0.1:8005/order/update_finish/',data=json.dumps({
        "orderId":obj.orderId,
        'status':"shipment_finish"
    }))
    if respons.status_code !=200:
        return JsonResponse({'status':'error','message':"không update duoc Shipment"},status=400)

    obj.save()
    return JsonResponse({'data':obj.to_dict()},status=200)

@csrf_exempt
def add_stage(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        location = data.get("location")
        comment = data.get("comment")
        shippingId = data.get("shippingId")

    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (location and comment and shippingId ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{location} and {comment} and {shippingId} "},
                               status=400)

    try:
        obj = Shipping.objects.get(id=shippingId)
    except Company.DoesNotExist:
        return JsonResponse({'status':'error','message':"không timg thấy Shipping"},status=400)
    
    if obj.status == 'complete':
        return JsonResponse({'status':'error','message':"Don hang da hoan thanh"},status=400)
    current_time = timezone.now()
    formatted_time = current_time.strftime("%M-%H %d/%m/%Y")

    stage =Stage(
        time = formatted_time,
        location = location,
        comment  = comment,
        shipping = obj
    )
    stage.save()
    # Trả về thông tin vừa tạo nếu thành công
    return JsonResponse({"status": "success", "message": "thêm stage thành công.", "data": stage.to_dict()})

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_stage(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if(id ==None):
            return JsonResponse({'status':'error','message':"error id"},status=400)
        try:
            obj = Stage.objects.get(id=id)
            obj.delete()
            return JsonResponse({'status':'success','message':"delete success"},status=200)
        except Stage.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy stage"},status=400)
    return JsonResponse({"status":"erorr","message":"method is not DELETE"},status=400)
