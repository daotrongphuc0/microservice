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
def create_pay(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        customerId = data.get("customerId")
        orderId = data.get("orderId")
        status = data.get("status")
        paying_typeId = data.get("paying_typeId")
        amount = data.get("amount")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (customerId and orderId and status and amount and paying_typeId):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{customerId} and {orderId} and {status} and {amount} and {paying_typeId}"},
                               status=400)

    
    response = requests.post(f'http://127.0.0.1:8000/customerinfo/',data=json.dumps({"customerId":customerId}))
    if response.status_code != 200:
        return JsonResponse({'status':'error','message':"không tim thấy customer"},status=400)
    
    try:
        paying_type = Paying_type.objects.get(id=paying_typeId)
    except Paying_type.DoesNotExist:
        return JsonResponse({'status':'error','message':"không tim thấy Paying type"},status=400)
    
    current_time = timezone.now()
    formatted_time = current_time.strftime("%M-%H %d/%m/%Y")
    pay = Payment(
        customerId= customerId,
        orderId=orderId,
        status = status,
        amount = amount,
        paying_type = paying_type,
        time = formatted_time
    )
    pay.save()
    # Trả về thông tin vừa tạo nếu thành công
    return JsonResponse({"status": "success", "message": "Tao payment thành công.", "data": pay.to_dict()})


@csrf_exempt
def getall_pay(request):
    pays = Payment.objects.all()
    pay_dicts = [pay.to_dict() for pay in pays]
    return JsonResponse({"data": pay_dicts}, status=200)

@csrf_exempt
def get_pay_by_id(request):
    id = request.GET.get('id')
    if(id ==None):
        return JsonResponse({'status':'error','message':"error id"},status=400)
    try:
        obj = Payment.objects.get(id=id)
        return JsonResponse({'data':obj.to_dict()},status=200)
    except Payment.DoesNotExist:
        return JsonResponse({'status':'error','message':"không tim thấy payment"},status=400)

@csrf_exempt
def update_finish(request):
    id = request.GET.get('id')
    if(id ==None):
        return JsonResponse({'status':'error','message':"error id"},status=400)
    try:
        obj = Payment.objects.get(id=id)
    except Payment.DoesNotExist:
        return JsonResponse({'status':'error','message':"không timg thấy payment"},status=400)
    obj.status ='complete'
    # goi API update order
    respons = requests.post('http://127.0.0.1:8005/order/update_finish/',data=json.dumps({
        "orderId":obj.orderId,
        'status':"payment_finish"
    }))
    if respons.status_code !=200:
        return JsonResponse({'status':'error','message':"không update duoc payment"},status=400)

    obj.save()
    return JsonResponse({'data':obj.to_dict()},status=200)
