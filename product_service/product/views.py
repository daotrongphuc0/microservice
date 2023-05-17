from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import *
# Create your views here.

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        name = data.get("name")
        picture = data.get("picture")
        description = data.get("description")
        price = data.get("price")
        brandId = data.get("brandId")
        categoryId = data.get("categoryId")
        supplierId = data.get("supplierId")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (name and picture and description and price and brandId and categoryId and supplierId ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{name} and {picture} and {description} and {price} and {brandId} and {categoryId} and {supplierId} "},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được
    try:
        obj_sup = Supplier.objects.get(id=supplierId)
    except Supplier.DoesNotExist:
        return JsonResponse({'status':'error','message':"không tim thấy supplier"},status=400)
    
    try:
        obj_brand = Brand.objects.get(id=brandId)
    except Supplier.DoesNotExist:
        return JsonResponse({'status':'error','message':"không tim thấy brand"},status=400)
    
    try:
        obj_category = Category.objects.get(id=categoryId)
    except Supplier.DoesNotExist:
        return JsonResponse({'status':'error','message':"không tim thấy category"},status=400)

    product = Product(
        name=name,
        picture=picture,
        description=description,
        price=price,
        brand=obj_brand,
        category= obj_category,
        supplier= obj_sup,
        isActive = 1
    )
    product.save()

    inventory = Inventory(
        product=product,
        quantity=0
    )
    inventory.save()
    # Trả về thông tin vừa tạo nếu thành công
    return JsonResponse({"status": "success", "message": "Tạo product thành công.", "product": product.to_dict()})


@csrf_exempt
def getall_product(request):
    products = Product.objects.all()
    products_dicts = [product.to_dict() for product in products]
    return JsonResponse({"data": products_dicts}, status=200)

@csrf_exempt
def getall_inventory(request):
    inventorys = Inventory.objects.all()
    inventorys_dicts = [inventory.to_dict() for inventory in inventorys]
    return JsonResponse({"data": inventorys_dicts}, status=200)

@csrf_exempt
def get_product_by_id(request):
    id = request.GET.get('id')
    if(id ==None):
        return JsonResponse({'status':'error','message':"error id"},status=400)
    try:
        obj = Product.objects.get(id=id)
        return JsonResponse({'data':obj.to_dict()},status=200)
    except Product.DoesNotExist:
        return JsonResponse({'status':'error','message':"không tim thấy product"},status=400)

@csrf_exempt
def upadte_product(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        id = data.get("id")
        name = data.get("name")
        picture = data.get("picture")
        description = data.get("description")
        price = data.get("price")
        brandId = data.get("brandId")
        categoryId = data.get("categoryId")
        supplierId = data.get("supplierId")
        isActive= data.get("isActive")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (id and name and picture and description and price and brandId and categoryId and supplierId ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{id} and {name} and {picture} and {description} and {price} and {brandId} and {categoryId} and {supplierId} and {isActive} "},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được
    if id:
        try:
            obj_product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return JsonResponse({'status':'error','message':"không tim thấy product"},status=400)
    else:
        return JsonResponse({'status':'error','message':"vui long them thuoc tinh id"},status=400)

    try:
        obj_sup = Supplier.objects.get(id=supplierId)
    except Supplier.DoesNotExist:
        return JsonResponse({'status':'error','message':"không tim thấy supplier"},status=400)
    
    try:
        obj_brand = Brand.objects.get(id=brandId)
    except Supplier.DoesNotExist:
        return JsonResponse({'status':'error','message':"không tim thấy brand"},status=400)
    
    try:
        obj_category = Category.objects.get(id=categoryId)
    except Supplier.DoesNotExist:
        return JsonResponse({'status':'error','message':"không tim thấy category"},status=400)
    

    obj_product.name=name
    obj_product.picture=picture
    description=description
    obj_product.price=price
    obj_product.brand=obj_brand
    obj_product.category= obj_category
    obj_product.supplier= obj_sup
    obj_product.isActive = isActive
    obj_product.save()
    # Trả về thông tin vừa tạo nếu thành công
    return JsonResponse({"status": "success", "message": "update product thành công.", "product": obj_product.to_dict()})


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_product_by_id(request):
    if request.method == 'DELETE':
        id = request.GET.get('id')
        if(id ==None):
            return JsonResponse({'status':'error','message':"error id"},status=400)
        try:
            obj = Product.objects.get(id=id)
            inventory =Inventory.objects.get(product=obj)
            inventory.delete()
            obj.delete()
            return JsonResponse({'status':'success','message':"delete success"},status=200)
        except Product.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy product"},status=400)
        except Inventory.DoesNotExist:
            return JsonResponse({'status':'error','message':"không timg thấy Inventory"},status=400)
    return JsonResponse({"status":"erorr","message":"method is not DELETE"},status=400)


@csrf_exempt
def update_inventory(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        # Parse dữ liệu thành đối tượng Python
        data = json.loads(raw_data)
        id = data.get("productId")
        quantity= data.get("quantity")
    else:
        return JsonResponse({"status":"error",
                             "mesage":"method is not POST"},status =400)
    # Kiểm tra các thông tin bắt buộc có đầy đủ hay không
    if not (id and quantity  ):
        return JsonResponse({"status": "error", "message": "Vui lòng điền đầy đủ thông tin.",
                             "data":f"{id} and {quantity} "},
                               status=400)

    # Tạo một đối tượng user dựa trên thông tin đã nhận được
    if id:
        try:
            obj_product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return JsonResponse({'status':'error','message':"không tim thấy product"},status=400)
    else:
        return JsonResponse({'status':'error','message':"vui long them thuoc tinh id"},status=400)

    try:
        obj_Inven = Inventory.objects.get(product=obj_product)
    except Inventory.DoesNotExist:
        return JsonResponse({'status':'error','message':"không tim thấy Inventory"},status=400)
    obj_Inven.quantity = quantity
    obj_Inven.save()

   
    # Trả về thông tin vừa tạo nếu thành công
    return JsonResponse({"status": "success", "message": "update inventory product thành công.", "inventory": obj_Inven.to_dict()})
