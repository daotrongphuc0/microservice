from django.db import models

# Create your models here.
class Order(models.Model):
    shippingId = models.IntegerField(null=True)
    customerId = models.IntegerField()
    paymentId = models.IntegerField(null=True)
    status = models.CharField(max_length=255)
    total = models.BigIntegerField()
    time = models.CharField(max_length=255)

    def __str__(self) :
        return f"{self.customerId} - {self.id}"
    
    def to_dict(self):
        items = Item.objects.filter(order=self)
        order_dict = {
            "shippingId": self.shippingId,
            "customerId": self.customerId,
            "paymentId": self.paymentId,
            "status": self.status,
            "total": self.total,
            "time":self.time,
            'item':[item.to_dict() for item in items]
        }
        return order_dict
    

class Item(models.Model):
    productId = models.IntegerField()
    quantity = models.IntegerField()
    price = models.BigIntegerField()
    order = models.ForeignKey(Order,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order} -{self.id} "
    
    def to_dict(self):
        return  {
            "productId": self.productId,
            "quantity": self.quantity,
            "price": self.price
        }