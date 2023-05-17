from django.db import models

# Create your models here.
class Cart(models.Model):
    customerId = models.IntegerField()

    def __str__(self) :
        return f"Customer ID: {self.customerId}"
    
    def to_dict(self):
        return {
            "id":self.id,
            "customerId":self.customerId
        }
    

class Item(models.Model):
    productId = models.IntegerField()
    quantity = models.IntegerField()
    price = models.BigIntegerField()
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)

    def __str__(self) :
        return f"Item of customer: {self.cart.customerId}"
    
    def to_dict(self):
        return {
            "id":self.id,
            "productId":self.productId,
            "quantity":self.quantity,
            "price":self.price,
            "cart":self.cart.to_dict()
        }
    